"""Windows 視窗管理工具 - 用於最小化所有視窗"""
import ctypes
from ctypes import wintypes
import time


class WindowManager:
    """Windows 視窗管理器 - 用於最小化所有視窗"""
    
    # Windows API 常量
    VK_LWIN = 0x5B  # Left Windows key
    VK_M = 0x4D     # M key
    KEYEVENTF_KEYUP = 0x0002
    
    @staticmethod
    def minimize_all_windows():
        """
        最小化所有視窗（使用 Win+M 快捷鍵）
        
        Returns:
            bool: 操作是否成功
        """
        try:
            user32 = ctypes.windll.user32
            
            # 模擬按下 Win+M 快捷鍵
            # 按下 Win 鍵
            user32.keybd_event(
                WindowManager.VK_LWIN,
                0,
                0,
                0
            )
            time.sleep(0.05)  # 短暫延遲以確保鍵被按下
            
            # 按下 M 鍵
            user32.keybd_event(
                WindowManager.VK_M,
                0,
                0,
                0
            )
            time.sleep(0.05)
            
            # 釋放 M 鍵
            user32.keybd_event(
                WindowManager.VK_M,
                0,
                WindowManager.KEYEVENTF_KEYUP,
                0
            )
            time.sleep(0.05)
            
            # 釋放 Win 鍵
            user32.keybd_event(
                WindowManager.VK_LWIN,
                0,
                WindowManager.KEYEVENTF_KEYUP,
                0
            )
            
            return True
        except Exception as e:
            print(f"最小化視窗時發生錯誤: {e}")
            return False
    
    @staticmethod
    def restore_all_windows():
        """
        恢復所有視窗（使用 Win+Shift+M 快捷鍵）
        
        Returns:
            bool: 操作是否成功
        """
        try:
            user32 = ctypes.windll.user32
            
            VK_LSHIFT = 0xA0  # Left Shift key
            
            # 模擬按下 Win+Shift+M 快捷鍵
            # 按下 Win 鍵
            user32.keybd_event(
                WindowManager.VK_LWIN,
                0,
                0,
                0
            )
            time.sleep(0.05)
            
            # 按下 Shift 鍵
            user32.keybd_event(
                VK_LSHIFT,
                0,
                0,
                0
            )
            time.sleep(0.05)
            
            # 按下 M 鍵
            user32.keybd_event(
                WindowManager.VK_M,
                0,
                0,
                0
            )
            time.sleep(0.05)
            
            # 釋放所有鍵
            user32.keybd_event(
                WindowManager.VK_M,
                0,
                WindowManager.KEYEVENTF_KEYUP,
                0
            )
            time.sleep(0.05)
            
            user32.keybd_event(
                VK_LSHIFT,
                0,
                WindowManager.KEYEVENTF_KEYUP,
                0
            )
            time.sleep(0.05)
            
            user32.keybd_event(
                WindowManager.VK_LWIN,
                0,
                WindowManager.KEYEVENTF_KEYUP,
                0
            )
            
            return True
        except Exception as e:
            print(f"恢復視窗時發生錯誤: {e}")
            return False

