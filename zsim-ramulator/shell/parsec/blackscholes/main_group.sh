zsim_home_dir=/ramulator-pim/zsim-ramulator
ramulator_home_dir=/ramulator-pim/ramulator
group_idx=0
cfg_file="${zsim_home_dir}/tests/blackscholes/group/blackscholes_${group_idx}.cfg"
${zsim_home_dir}/build/opt/zsim ${cfg_file}
acc_file="${zsim_home_dir}/shell/parsec/blackscholes/tools/get_acc_group.py"
python3 ${acc_file} --group_idx ${group_idx}