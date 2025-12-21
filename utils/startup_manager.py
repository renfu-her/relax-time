"""Windows 開機啟動管理工具"""
import os
import sys
import winreg
from pathlib import Path


class StartupManager:
    """Windows 開機啟動管理器"""
    
    REGISTRY_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
    APP_NAME = "RelaxTime"
    
    @staticmethod
    def get_exe_path() -> str:
        """取得 exe 檔案路徑"""
        if getattr(sys, 'frozen', False):
            # 如果是打包後的 exe
            return sys.executable
        else:
            # 開發環境，返回當前 Python 腳本路徑
            return sys.executable
    
    @staticmethod
    def get_startup_command() -> str:
        """取得啟動命令（帶 --hidden 參數）"""
        exe_path = StartupManager.get_exe_path()
        # 如果是 exe，直接執行；如果是開發環境，使用 python 執行
        if exe_path.endswith('.exe'):
            return f'"{exe_path}" --hidden'
        else:
            # 開發環境
            script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'main.py')
            return f'"{sys.executable}" "{script_path}" --hidden'
    
    @staticmethod
    def is_startup_enabled() -> bool:
        """檢查是否已設定開機啟動"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                StartupManager.REGISTRY_KEY,
                0,
                winreg.KEY_READ
            )
            try:
                value, _ = winreg.QueryValueEx(key, StartupManager.APP_NAME)
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
        except Exception as e:
            print(f"檢查開機啟動狀態時發生錯誤: {e}")
            return False
    
    @staticmethod
    def enable_startup():
        """啟用開機啟動"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                StartupManager.REGISTRY_KEY,
                0,
                winreg.KEY_WRITE
            )
            command = StartupManager.get_startup_command()
            winreg.SetValueEx(key, StartupManager.APP_NAME, 0, winreg.REG_SZ, command)
            winreg.CloseKey(key)
            print(f"已啟用開機啟動: {command}")
            return True
        except Exception as e:
            print(f"啟用開機啟動時發生錯誤: {e}")
            return False
    
    @staticmethod
    def disable_startup():
        """停用開機啟動"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                StartupManager.REGISTRY_KEY,
                0,
                winreg.KEY_WRITE
            )
            try:
                winreg.DeleteValue(key, StartupManager.APP_NAME)
                winreg.CloseKey(key)
                print("已停用開機啟動")
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                print("開機啟動未設定")
                return False
        except Exception as e:
            print(f"停用開機啟動時發生錯誤: {e}")
            return False


if __name__ == "__main__":
    # 測試
    print(f"開機啟動狀態: {StartupManager.is_startup_enabled()}")
    print(f"啟動命令: {StartupManager.get_startup_command()}")

