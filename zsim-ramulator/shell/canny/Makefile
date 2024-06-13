# Define the compiler and flags
CXX = g++
CXXFLAGS = `pkg-config --cflags --libs opencv`
TARGETS = canny_sequence canny_group canny_first_round
SRC_SEQUENCE = canny_sequence.cpp
SRC_BATCH = canny_group.cpp
SRC_FIRST_ROUND = canny_first_round.cpp
SEQUENCE_IDX = 0
GROUP_IDX = 0

# Default target to compile all programs
all: $(TARGETS)

# Rule to compile canny_sequence
canny_sequence: $(SRC_SEQUENCE)
	$(CXX) -o canny_sequence $(SRC_SEQUENCE) $(CXXFLAGS)

# Rule to compile canny_group
canny_group: $(SRC_BATCH)
	$(CXX) -o canny_group $(SRC_BATCH) $(CXXFLAGS)

# Rule to compile canny_first_run
canny_first_round: $(SRC_FIRST_ROUND)
	$(CXX) -o canny_first_rd $(SRC_BATCH) $(CXXFLAGS)

# Rule to run canny_sequence
run_sequence: canny_sequence
	./canny_sequence $(SEQUENCE_IDX) false

# Rule to run canny_group
run_group: canny_group
	./canny_group $(GROUP_IDX) false

# Rule to run canny_group
run_first_round: canny_first_rd
	./canny_first_rd alse

# Clean up the compiled executables
clean:
	rm -f $(TARGETS)
