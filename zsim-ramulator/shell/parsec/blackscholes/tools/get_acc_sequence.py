from pathlib import Path
import argparse

def read_floats(file_path):
    with file_path.open('r') as file:
        return [float(line.strip()) for line in file if line.strip()]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate the average relative error between output and ground truth data.")
    parser.add_argument("--n_groups", type=int, default=100, help="Number of groups to process")
    args = parser.parse_args()

    groundtruth_dir = Path("/ramulator-pim/zsim-ramulator/shell/parsec/blackscholes/ground_truth")
    output_dir = Path("/ramulator-pim/zsim-ramulator/shell/parsec/blackscholes/output")
    n_groups=args.n_groups
    for i in range(n_groups):
        output_path = output_dir / "parsec_option_data_{}.csv".format(str(i))
        groundtruth_path = groundtruth_dir / "parsec_option_data_{}.csv".format(str(i))
        
        # Read the numbers from both files
        output_values = read_floats(output_path)
        groundtruth_values = read_floats(groundtruth_path)
        
        # Compute relative errors where groundtruth is not zero to avoid division by zero
        relative_errors = []
        for output, groundtruth in zip(output_values, groundtruth_values):
            if groundtruth != 0:
                relative_error = abs((output - groundtruth) / groundtruth)
                relative_errors.append(relative_error)

        # Calculate the average relative error if there are any to calculate
        if relative_errors:
            avg_relative_error = sum(relative_errors) / len(relative_errors)
            print("Group {}: Average Relative Error = {}".format(i, avg_relative_error))
        else:
            print("Group {}: No valid data for error calculation.".format(i))