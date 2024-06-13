zsim_home_dir=/ramulator-pim/zsim-ramulator
n_groups=1
for ((i=0; i<n_groups; i++))
do
    cfg_file="${zsim_home_dir}/tests/canny/group/canny_${i}.cfg"
    ${zsim_home_dir}/build/opt/zsim ${cfg_file}
done