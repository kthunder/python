使用说明

1. 使用gen_memmap_conf.py生成配置文件MmeMapConfig.csv至工具根目录
2. 调用gen_memmap_fast.py生成相关memmap.h至memmap_include_headers文件夹下

注意：

    需要生成的模块名在gen_memmap_fast.py的module_list和module_list_safety中配置即可


使用示例（在工具根目录下打开命令行）

```shell
python -u .\memmap_gen\gen_memmap_conf.py
python -u .\memmap_gen\gen_memmap_fast.py
```
