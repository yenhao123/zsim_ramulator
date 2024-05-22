# Define the compiler and flags
CXX = g++
CXXFLAGS = `pkg-config --cflags --libs opencv4` -std=c++11
TARGET = canny_edge_detection
SRC = canny_evaluation.cpp
IMG = image.jpg
RES = res.jpg
GT = ground_truth.jpg
LOW_THRESH = 100
HIGH_THRESH = 200

# Default target to compile the program
all: $(TARGET)

# Rule to compile the program
$(TARGET): $(SRC)
	$(CXX) -o $(TARGET) $(SRC) $(CXXFLAGS)

# Rule to run the program
run: $(TARGET)
    ./$(TARGET) $(IMG) $(RES) $(GT) $(LOW_THRESH) $(HIGH_THRESH)

# Clean up the compiled executable
clean:
    rm -f $(TARGET)