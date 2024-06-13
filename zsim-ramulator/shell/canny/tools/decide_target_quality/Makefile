# Define the compiler and flags
CXX = g++
CXXFLAGS = `pkg-config --cflags --libs opencv`
TARGETS = canny
SRC = canny.cpp

# Default target to compile all programs
all: $(TARGETS)

# Rule to compile canny
canny: $(SRC)
	$(CXX) -o canny $(SRC) $(CXXFLAGS)

# Clean up the compiled executables
clean:
	rm -f $(TARGETS)
