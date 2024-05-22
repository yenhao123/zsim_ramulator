#include <opencv2/opencv.hpp>
#include <iostream>
#include <cmath>
#include <string>  // 添加此行以确保使用 std::stod

void canny_edge_detection(const char* input_image, const char* output_image, const char* ground_truth_image, double low_threshold, double high_threshold) {
    // Load the input image
    cv::Mat src = cv::imread(input_image, cv::IMREAD_GRAYSCALE);
    if (src.empty()) {
        std::cerr << "Could not open or find the image\n";
        return;
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
    if (argc != 6) {
        std::cerr << "Usage: " << argv[0] << " <input_image> <output_image> <ground_truth_image> <low_threshold> <high_threshold>\n";
        return -1;
    }

    const char* input_image = argv[1];
    const char* output_image = argv[2];
    const char* ground_truth_image = argv[3];
    double low_threshold = std::stod(argv[4]);
    double high_threshold = std::stod(argv[5]);

    canny_edge_detection(input_image, output_image, ground_truth_image, low_threshold, high_threshold);

    return 0;
}
