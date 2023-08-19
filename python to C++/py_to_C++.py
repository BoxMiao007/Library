import os
import shutil
import subprocess

def 列出指定后缀文件(directory, 后缀):
    return [file for file in os.listdir(directory) if file.endswith(后缀)]

def 选择文件(files, 提示信息):
    print(提示信息)
    for idx, file in enumerate(files, start=1):
        print(f"{idx}. {file}")
    choice = int(input("请输入您的选择编号: ")) - 1
    return files[choice]

def 处理脚本(源文件, 目标文件, 图标文件):
    try:
        with open(源文件, "r", encoding="utf-8") as f:
            内容 = f.read()
    except FileNotFoundError:
        内容 = ""
    
    if 'import sys' not in 内容:
        内容 = 'import sys\nimport os\n\n' + 内容
        with open(目标文件, "w", encoding="utf-8") as f_target:
            f_target.write(内容)
            print(f"已创建并修改 {目标文件}")

    打包命令 = f'nuitka --windows-icon-from-ico={图标文件} {目标文件}'
    subprocess.run(打包命令, shell=True, check=True)
    print(f"已使用 Nuitka 打包 {目标文件} 为可执行文件。")

def 删除文件夹或文件(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
            print(f"已删除 {path}")
        else:
            os.remove(path)
            print(f"已删除 {path}")

def 主函数():
    当前目录 = "."
    py文件列表 = 列出指定后缀文件(当前目录, ".py")
    ico文件列表 = 列出指定后缀文件(当前目录, ".ico")

    选择的py文件 = 选择文件(py文件列表, "请选择要打包的 Python 脚本:")
    选择的ico文件 = 选择文件(ico文件列表, "请选择一个图标文件:")

    目标脚本文件 = os.path.join(os.path.dirname(选择的py文件), os.path.basename(选择的py文件).replace(".py", "-to-c++.py"))
    shutil.copy(选择的py文件, 目标脚本文件)
    处理脚本(目标脚本文件, 目标脚本文件, 选择的ico文件)

    build文件夹 = os.path.splitext(目标脚本文件)[0] + ".build"
    cmd文件 = f"{os.path.splitext(目标脚本文件)[0]}.cmd"

    删除全部 = input("是否删除生成的 .build 文件夹和 .cmd 文件？(y/n): ")
    if 删除全部.lower() == "y":
        删除文件夹或文件(build文件夹)
        删除文件夹或文件(cmd文件)

    生成的exe文件 = os.path.splitext(目标脚本文件)[0] + ".exe"
    重命名exe文件 = 生成的exe文件.replace("-to-c++", "")
    os.rename(生成的exe文件, 重命名exe文件)
    print(f"已重命名 {生成的exe文件} 为 {重命名exe文件}")

if __name__ == "__main__":
    主函数()
