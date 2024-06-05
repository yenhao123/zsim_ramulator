# Define the compiler and flags
CXX = g++
CXXFLAGS = `pkg-config --cflags --libs opencv`
TARGET = canny_batch
SRC = canny_batch.cpp
GROUP_IDX = 0

# Default target to compile the program
all: $(TARGET)

# Rule to compile the program
$(TARGET): $(SRC)
	$(CXX) -o $(TARGET) $(SRC) $(CXXFLAGS)

# Rule to run the program
run: $(TARGET)
	./$(TARGET) $(GROUP_IDX)

# Clean up the compiled executable
clean:
	rm -f $(TARGET)
