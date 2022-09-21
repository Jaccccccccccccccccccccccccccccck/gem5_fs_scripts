# gem5_fs_scripts
## 脚本启动需使用python3

## 依赖
```
pip3 install pexpect
```
## 参数说明
### m5_out: gem5模拟统计信息输出文件目录，建议每次运行指定新的目录，防止与之前模拟的结果覆盖  
### cpu_type: 模拟的CPU类型，可选：TimingSimpleCPU/O3CPU/MinorCPU  
## 启动示例
```
nohup python3 gem5_fs.py \
    --m5_out=/home/testO3 \ 
    --cpu_type=O3CPU \
    >gem5_testO3_4.out 2>&1 &
```
## 启用L3 caches启动示例
```
nohup python3 gem5_fs.py \
    --m5_out=/home/test_o3_l3_parsec_4 \
    --cpu_type=O3CPU \
    --num_cpu=4 \
    --gem5_config_py=/home/workspace/gem5/configs/example/fsL3.py \
    --command='/streamcluster/inst/amd64-linux.gcc/bin/streamcluster 2 5 1 10 10 5 none output.txt 4' \
    --caches='--l1d_size=64kB --l1i_size=64kB --l2_size=512kB --l2cache --l3_size=4MB --l3cache' \
    >gem5_test_o3_l3_parserc_4.out 2>&1 &
```

## 使用ruby L3经典模型启动示例
```
nohup python3 gem5_fs.py \
    --m5_out=/home/test_o3_l3_ruby_parserc_1 \
    --cpu_type=O3CPU \
    --num_cpu=4 \
    --gem5_config_py=/home/workspace/gem5/configs/example/fsL3.py \
    --command='/streamcluster/inst/amd64-linux.gcc/bin/streamcluster 2 5 1 10 10 5 none output.txt 4' \
    --caches='--ruby --l1d_size=64kB --l1i_size=64kB --l2_size=512kB --l2cache --l3_size=4MB --l3cache --num-l3caches=1' \
    >gem5_test_o3_ruby_l3_parsec_1.out 2>&1 &
```