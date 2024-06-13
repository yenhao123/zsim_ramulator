import argparse
import subprocess

def modify_cfg_file(config):
    # 读取 cfg 文件内容
    with open('/root/ramulator-pim/common/DRAMPower/memspecs/MICRON_4Gb_DDR4-2400_8bit_A_sample.xml', 'r') as file:
        filedata = file.read()
    
    filedata = filedata.replace('$REFI_VALUE$', str(config[0]))
    filedata = filedata.replace('$RAS_VALUE$', str(config[1]))
    filedata = filedata.replace('$RRDL_VALUE$', str(config[2]))
    filedata = filedata.replace('$RRDS_VALUE$', str(config[3]))
    filedata = filedata.replace('$RP_VALUE$', str(config[4]))
    filedata = filedata.replace('$RCD_VALUE$', str(config[5]))

    with open('/root/ramulator-pim/common/DRAMPower/memspecs/MICRON_4Gb_DDR4-2400_8bit_A.xml', 'w') as file:
        file.write(filedata)


def execute_simualtor():
    # Command components
    #workload = '/root/ramulator-pim/zsim-ramulator/shell/canny/drampower_mem_trace/n_groups=2/dramsys_input_all.stl'
    workload = '/root/ramulator-pim/common/DRAMPower/traces/mediabench-epic.trace'
    command = [
        '/root/ramulator-pim/common/DRAMPower/drampower',
        '-m', '/root/ramulator-pim/common/DRAMPower/memspecs/MICRON_4Gb_DDR4-2400_8bit_A.xml',
        '-t', workload
    ]

    # Execute the command
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    # Check if there was an error
    if result.returncode != 0:
        print("Error in command execution!")
        print("Error:", result.stderr)
        return None
    print(result)
    # Process the output to find the total trace energy and average power
    for line in result.stdout.split('\n'):
        if "Total Trace Energy:" in line:
            energy_value = float(line.split(':')[1].strip().split(' ')[0])
        elif "Average Power:" in line:
            average_power = float(line.split(':')[1].strip().split(' ')[0])
    
    # Calculate and return latency if both values are found
    if energy_value is not None and average_power is not None:
        # Convert average power from mW to W for the calculation
        latency = (energy_value / 1000) / average_power  # Convert energy from pJ to J (1 pJ = 10^-12 J, 1 mW = 10^-3 W)
        return latency, energy_value
    else:
        print("Failed to find necessary energy or power data.")
        return None        

if __name__ == "__main__":
    # REFI、RAS、RRD_L、RRD_S、RP
    default_config = [4680, 39, 6, 4, 16, 16]
    modify_cfg_file(default_config)
    latency, energy = execute_simualtor()
    print("Default config, Total Trace Energy: {} pJ".format(energy))
    
    '''
    refi_values = [2340 * i for i in range(1, 10)]
    for refi_value in refi_values:
        config = [refi_value, 39, 6, 4]
        modify_cfg_file(config)
        energy = execute_simualtor()
        print("REFI: {}, Total Trace Energy: {} pJ".format(refi_value, energy))

    refi = 21060
    ras_values = [18, 24, 39, 49]
    for ras in ras_values:
        config = [refi, ras, 6, 4]
        modify_cfg_file(config)
        latency, energy = execute_simualtor()
        print("RAS: {}, Total Trace Energy: {} pJ".format(ras, energy))
        print("RAS: {}, Total Trace Latency: {} pJ".format(ras, latency))

    refi = 21060
    ras = 39
    rrdss = [2, 3, 4, 5, 6]
    for rrds in rrdss:
        config = [refi, ras, 6, rrds]
        modify_cfg_file(config)
        latency, energy = execute_simualtor()
        print("RRDS: {}, Total Trace Energy: {} pJ".format(rrds, energy))
        print("RRDS: {}, Total Trace Latency: {} pJ".format(rrds, latency))

    refi = 21060
    ras = 39
    rrds = 4
    rrdls = [2, 4, 6, 8, 50]
    for rrdl in rrdls:
        config = [refi, ras, rrdl, rrds]
        modify_cfg_file(config)
        latency, energy = execute_simualtor()
        print("RRDL: {}, Total Trace Energy: {} pJ".format(rrdl, energy))
        print("RRDL: {}, Total Trace Latency: {} pJ".format(rrdl, latency))

    refi = 21060
    ras = 39
    rrds = 4
    rrdl = 6
    rps = [8, 12, 16, 20, 24]
    for rp in rps:
        config = [refi, ras, rrdl, rrds, rp]
        modify_cfg_file(config)
        latency, energy = execute_simualtor()
        print("RP: {}, Total Trace Energy: {} pJ".format(rp, energy))
        print("RP: {}, Total Trace Latency: {} pJ".format(rp, latency))
    '''
    refi = 21060
    ras = 39
    rrds = 4
    rrdl = 6
    rp = 16
    rcds = [8, 12, 16, 20, 24]
    for rcd in rcds:
        config = [refi, ras, rrdl, rrds, rp, rcd]
        print(config)
        modify_cfg_file(config)
        latency, energy = execute_simualtor()
        print("RCD: {}, Total Trace Energy: {} pJ".format(rcd, energy))
        print("RCD: {}, Total Trace Latency: {} pJ".format(rcd, latency))
    refi = 21060
    ras = 39 # invairant
    rrds = 4 # invairant
    rrdl = 6 # invairant
    best_config = [refi, ras, rrdl, rrds]