需要安装 python3
需要安装 vgame 库

```
pip install vgame==0.1.10
```

直接用 python main.py 命令就能运行游戏


如果想要打包成 exe 请先安装 pyinstaller 然后在 main.py 文件路径下使用下面命令即可
执行命令成功后就可以在 dist 文件夹内看到生成好的游戏文件

```
pyinstaller -F -w --add-data "./source;source" main.py
```