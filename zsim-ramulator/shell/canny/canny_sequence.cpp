#include <opencv2/opencv.hpp>
#include "/root/ramulator-pim/zsim-ramulator/misc/hooks/zsim_hooks.h"
#include <iostream>
#include <cmath>
#include <string>  // 添加此行以确保使用 std::stod
#include <unistd.h>
#include <fstream>
#include <cstdio>

bool DEBUG_FLAG = false;
const char* mem_addr_file = "/root/ramulator-pim/zsim-ramulator/shell/canny/tmp/memory_addresses_sequence.csv";

void canny_edge_detection(const char* input_image, const char* output_image, const char* ground_truth_image, double low_threshold, double high_threshold, int image_idx) {
    // Load the input image
    cv::Mat src = cv::imread(input_image, cv::IMREAD_GRAYSCALE);
    if (src.empty()) {
        std::cerr << "Could not open or find the image\n";
        return;
    }
    
    if(DEBUG_FLAG){
        // record memory address
        std::ofstream outfile;
        outfile.open(mem_addr_file, std::ios::out | std::ios::app);
        for (int row = 0; row < src.rows; ++row) {
            for (int col = 0; col < src.cols; ++col) {
                // Calculate the memory address of the current pixel
                uchar* pixel_address = src.data + row * src.step + col;
                outfile << image_idx << "," << row << "," << col << "," << static_cast<void*>(pixel_address) << std::endl;
            }
        }
        outfile.close();
    }

    // Load the ground truth image
    cv::Mat ground_truth = cv::imread(ground_truth_image, cv::IMREAD_GRAYSCALE);
    if (ground_truth.empty()) {
        std::cerr << "Could not open or find the ground truth image\n";
        return;
    }

    cv::Mat blurred, edges;

    // Apply Gaussian Blur to reduce noise
    cv::GaussianBlur(src, blurred, cv::Size(5, 5), 1.4);

    // Apply Canny edge detection
    cv::Canny(blurred, edges, low_threshold, high_threshold);
    
    // Save the result
    cv::imwrite(output_image, edges);

    // Calculate RMSE
    if (edges.size() != ground_truth.size()) {
        std::cerr << "Error: Size of detected edges and ground truth image do not match\n";
        return;
    }

    double mse = 0;
    for (int y = 0; y < edges.rows; y++) {
        for (int x = 0; x < edges.cols; x++) {
            double diff = edges.at<uchar>(y, x) - ground_truth.at<uchar>(y, x);
            mse += diff * diff;
        }
    }
    mse /= (edges.rows * edges.cols);
    double rmse = std::sqrt(mse);

    std::cout << "Edge detection completed. Result saved as " << output_image << "\n";
    std::cout << "RMSE compared to ground truth: " << rmse << "\n";
}

int main(int argc, char** argv) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <sequence_number> <debug flag>" << std::endl;
        return 1;
    }
    const char* INPUT_DIR = "/root/ramulator-pim/zsim-ramulator/shell/canny/input/";
    const char* GD_DIR = "/root/ramulator-pim/zsim-ramulator/shell/canny/ground_truth/";
    const char* OUTPUT_DIR = "/root/ramulator-pim/zsim-ramulator/shell/canny/output/";
    int sequence = std::atoi(argv[1]);
    int sequence_size = 100;
    int start_n_sequence = sequence * sequence_size;
    int end_n_sequence = (sequence+1) * sequence_size;
    double low_threshold = 50;
    double high_threshold = 150;
    
    if(strcmp(argv[2], "true") == 0){
        DEBUG_FLAG = true;
        // INIT
        if (std::remove(mem_addr_file) != 0) {
            std::cerr << "Error deleting file: " << mem_addr_file << std::endl;
        } else {
            std::cout << "File successfully deleted: " << mem_addr_file << std::endl;
        }
    }

    // first round
    std::string input_image = std::string(INPUT_DIR) + std::to_string(start_n_sequence) + ".jpg";
    std::string output_image = std::string(OUTPUT_DIR) + std::to_string(start_n_sequence) + ".jpg";
    std::string gd_image = std::string(GD_DIR) + std::to_string(start_n_sequence) + ".jpg";
    canny_edge_detection(input_image.c_str(), output_image.c_str(), gd_image.c_str(), low_threshold, high_threshold, start_n_sequence);

    // start tracing
    zsim_roi_begin();
    zsim_PIM_function_begin();
    for (int i = (start_n_sequence+1); i < end_n_sequence; i++){
        std::string input_image = std::string(INPUT_DIR) + std::to_string(i) + ".jpg";
        std::string output_image = std::string(OUTPUT_DIR) + std::to_string(i) + ".jpg";
        std::string gd_image = std::string(GD_DIR) + std::to_string(i) + ".jpg";
        canny_edge_detection(input_image.c_str(), output_image.c_str(), gd_image.c_str(), low_threshold, high_threshold, i);
    }
    zsim_PIM_function_end();
    zsim_roi_end();
    return 0;
}
