zsim_home_dir=/ramulator-pim/zsim-ramulator
ramulator_home_dir=/ramulator-pim/ramulator
for i in {0..3}
do
    cfg_file="${zsim_home_dir}/tests/canny/canny_${i}.cfg"
    ${zsim_home_dir}/build/opt/zsim ${cfg_file}
done