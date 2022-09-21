import pexpect
import argparse
import logging
import sys
import re
import os

parser = argparse.ArgumentParser()
parser.add_argument("--m5_out", type=str, required=True)
parser.add_argument("--gem5", type=str, default='/home/workspace/gem5/build/ARM/gem5.opt')
parser.add_argument("--m5_path", type=str, default='/home/')
parser.add_argument("--gem5_config_py", type=str, default='/home/workspace/gem5/configs/example/fs.py')
parser.add_argument("--cpu_type", type=str, default='TimingSimpleCPU')
parser.add_argument("--command", type=str, default='/libquantum.arm64 33 5')
parser.add_argument("--mem_size", type=str, default='8GB')
parser.add_argument("--num_cpu", type=str, default='1')
parser.add_argument("--m5_bootloader", type=str, default='/home/binaries/boot.arm64')
parser.add_argument("--disk_image", type=str, default='ubuntu-18.04-arm64-docker-add-spec.img')
parser.add_argument("--kernel", type=str, default='vmlinux-4.14')
parser.add_argument("--m5_term", type=str, default='m5term')
parser.add_argument("--m5_exit_command", type=str, default='m5 exit')
parser.add_argument("--caches", type=str, default='')
args = parser.parse_args()

# pexpect timeout 1000 days: 1000 * 24 * 60m * 60s/m
TIMEOUT = 86400000

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

GEM5_COMMAND = f'''
M5_PATH={args.m5_path} {args.gem5} \
    --outdir={args.m5_out} \
    {args.gem5_config_py} \
    --cpu-type={args.cpu_type} \
    --mem-size={args.mem_size} \
    -n {args.num_cpu} \
    --bootloader={args.m5_bootloader} \
    --disk-image={args.disk_image} \
    --caches {args.caches} \
    --kernel={args.kernel}
'''
M5_TERM_COMMAND = '''
m5term 127.0.0.1 {port}
'''

'''
gem5 log like 
build/ARM/sim/kernel_workload.cc:46: info: kernel located at: /home/binaries/vmlinux-4.14
system.vncserver: Listening for connections on port 5900
system.terminal: Listening for connections on port 3456
system.realview.uart1.device: Listening for connections on port 3457
system.realview.uart2.device: Listening for connections on port 3458
system.realview.uart3.device: Listening for connections on port 3459

extract the port number from log
'''
def run_gem5():
    logging.info('gem5 shell open ...')
    logging.info(f'gem5 command: {GEM5_COMMAND}' )
    child = pexpect.spawn('bash', ['-c', GEM5_COMMAND], timeout=TIMEOUT)
    re_port = re.compile(r'system.terminal: Listening for connections on port (\d+)')
    while(True) :
        child.expect('system.realview.uart1.device', timeout=TIMEOUT)
        gem5_log = child.before.decode('UTF8')
        logging.info(f'gem5_log: {gem5_log}')
        match_result = re.search(re_port, gem5_log)
        if match_result:
            logging.info(f'extract terminal port:{match_result.group(1)}')
            return match_result.group(1), child
        else:
            logging.error('extract terminal port failed!')
    return N, None

def run_m5_term(port):
    logging.info('m5term shell open ...')
    m5_term_command = M5_TERM_COMMAND.format(port=port)
    logging.info(f'm5 command: {m5_term_command}')
    child = pexpect.spawn('bash', ['-c', m5_term_command], timeout=TIMEOUT)
    try:
        child.expect('root@aarch64-gem5:~#')
        logging.info('get prompt success.')
        logging.info('outs are as follows:')
        logging.info(child.before.decode('UTF8'))
    except Exception as e:
        logging.error('error when expect a prompt!, out are as follows:')
        logging.error(child.before)
        exit()
    child.sendline(args.command)
    logging.info(f'run command: {args.command}')
    child.expect('#', timeout=TIMEOUT)
    logging.info(f'run command result: {child.before}')
    logging.info(f'send m5 quit command: {args.m5_exit_command}')
    child.sendline(args.m5_exit_command)
    child.expect(pexpect.EOF, timeout=TIMEOUT)
    logging.info('gem5 exit success. outs are as follows:')
    logging.info(child.before)
    child.close()
    logging.info('m5term shell closed.')

def get_gem5_stats():
    gem5_out_file = os.path.join(args.m5_out, 'stats.txt')
    logging.info(f'try open gem5 out stats.txt: {gem5_out_file}')
    if os.path.isfile(gem5_out_file):
        with open(gem5_out_file) as f:
            logging.info('gem5 outputs are as follow:')
            logging.info(f.read())

def main():
    logging.info('script start.')
    port, child_gem5 = run_gem5()
    run_m5_term(port=port)
    child_gem5.close()
    logging.info('gem5 shell closed.')
    get_gem5_stats()

if __name__ == '__main__':
    main()