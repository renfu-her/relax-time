"""使用 PyInstaller 打包為 exe 的腳本"""
import PyInstaller.__main__
import os

# 專案根目錄
project_root = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'main.py',
    '--name=RelaxTime',
    '--onefile',
    '--windowed',  # 不顯示控制台視窗
    '--icon=resources/alarm_clock.ico',
    '--add-data=resources;resources',  # 包含資源文件夾
    '--hidden-import=pystray',
    '--hidden-import=PIL',
    '--hidden-import=PIL._tkinter_finder',
    '--clean',
    '--noconfirm',
])

