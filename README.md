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
python3 gem5_fs.py --m5_out=/home/testfs1 --cpu_type=TimingSimpleCPU
```
