zsim_home_dir=/ramulator-pim/zsim-ramulator
ramulator_home_dir=/ramulator-pim/ramulator
n_groups=2
for ((i=0; i<n_groups; i++))
do
    cfg_file="${zsim_home_dir}/tests/blackscholes/group/blackscholes_${i}.cfg"
    ${zsim_home_dir}/build/opt/zsim ${cfg_file}
done