program_dir=/ramulator-pim/zsim-ramulator/shell/parsec/blackscholes
blackshcoles_exe=${program_dir}/blackscholes
input_dir=${program_dir}/input
ground_truth_dir=${program_dir}/ground_truth
n_groups=100

for ((i=0; i<n_groups; i++))
do
    input_path=$input_dir/parsec_option_data_${i}.csv
    gd_path=$ground_truth_dir/parsec_option_data_${i}.csv
    $blackshcoles_exe 1 $input_path $gd_path false
done