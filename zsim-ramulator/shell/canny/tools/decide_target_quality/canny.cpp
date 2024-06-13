#include <opencv2/opencv.hpp>
#include "/root/ramulator-pim/zsim-ramulator/misc/hooks/zsim_hooks.h"
#include <iostream>
#include <cmath>
#include <string>  // 添加此行以确保使用 std::stod
#include <unistd.h>
#include <fstream>

bool DEBUG_FLAG = false;
void canny_edge_detection(const char* input_image, const char* output_image, const char* ground_truth_image, double low_threshold, double high_threshold) {
    // Load the input image
    cv::Mat src = cv::imread(input_image, cv::IMREAD_GRAYSCALE);
    if (src.empty()) {
        std::cerr << "Could not open or find the image\n";
        return;
    }
    if(DEBUG_FLAG){
        // record memory address
        std::ofstream outfile;
        outfile.open("/root/ramulator-pim/zsim-ramulator/shell/canny/tmp/memory_addresses_target_quality_decide.csv");
        for (int row = 0; row < src.rows; ++row) {
            for (int col = 0; col < src.cols; ++col) {
                // Calculate the memory address of the current pixel
                uchar* pixel_address = src.data + row * src.step + col;
                outfile << 0 << "," << row << "," << col << "," << static_cast<void*>(pixel_address) << std::endl;
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

    /*
    // 添加噪聲
    cv::Mat noise = cv::Mat::zeros(edges.size(), edges.type());
    double noise_amount = 0.6; // 噪聲比例
    cv::randn(noise, 0, 255 * noise_amount); // 生成正態分布噪聲
    edges += noise;
    */

    // Define the translation matrix for shifting the image
    // Shift 5 pixels to the right (x) and 5 pixels down (y)
    float dx = 1.0f; // x translation
    float dy = 1.0f; // y translation
    cv::Mat translation_matrix = (cv::Mat_<double>(2,3) << 1, 0, dx, 0, 1, dy);

    // Apply the translation to the detected edges
    cv::warpAffine(edges, edges, translation_matrix, edges.size());
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
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <debug_flag>" << std::endl;
        return -1;
    }

    std::string input_image = "/root/ramulator-pim/zsim-ramulator/shell/canny/tools/decide_target_quality/input.jpg";
    std::string output_image = "/root/ramulator-pim/zsim-ramulator/shell/canny/tools/decide_target_quality/output.jpg";
    std::string gd_image = "/root/ramulator-pim/zsim-ramulator/shell/canny/tools/decide_target_quality/ground_truth.jpg";
    double low_threshold = 50;
    double high_threshold = 150;
    if(strcmp(argv[1], "true") == 0){
        DEBUG_FLAG = true;
    }

    zsim_roi_begin();
    zsim_PIM_function_begin();
    canny_edge_detection(input_image.c_str(), output_image.c_str(), gd_image.c_str(), low_threshold, high_threshold);
    zsim_PIM_function_end();
    zsim_roi_end();
    return 0;
}
