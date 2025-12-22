"""全螢幕倒數遮罩視窗"""
import tkinter as tk
from typing import Optional, Callable, List
import threading
import time
import ctypes
from ctypes import wintypes


class CountdownOverlay:
    """全螢幕透明黑色遮罩，顯示倒數 5, 4, 3, 2, 1，支援多螢幕"""
    
    def __init__(self, parent_root: Optional[tk.Tk] = None):
        """
        初始化遮罩視窗
        
        Args:
            parent_root: 父視窗（tk.Tk），用於創建 Toplevel
        """
        self.parent_root = parent_root
        self.overlay_windows: List[tk.Toplevel] = []  # 多個螢幕的遮罩視窗
        self.countdown_labels: List[tk.Label] = []  # 每個螢幕的倒數標籤
        self.is_showing = False
        self.on_countdown_complete: Optional[Callable[[], None]] = None
        self._countdown_thread: Optional[threading.Thread] = None
    
    def show(self, on_complete: Optional[Callable[[], None]] = None):
        """
        顯示全螢幕遮罩並開始倒數
        
        Args:
            on_complete: 倒數完成後的回調函數
        """
        if self.is_showing:
            return
        
        self.on_countdown_complete = on_complete
        self.is_showing = True
        
        # 在主線程中創建視窗
        self._create_overlay()
        
        # 在獨立線程中執行倒數
        self._countdown_thread = threading.Thread(target=self._countdown_loop, daemon=True)
        self._countdown_thread.start()
    
    def _get_all_monitors(self):
        """獲取所有顯示器的信息"""
        monitors = []
        
        # 定義 Windows API 結構和函數
        class RECT(ctypes.Structure):
            _fields_ = [("left", ctypes.c_long),
                       ("top", ctypes.c_long),
                       ("right", ctypes.c_long),
                       ("bottom", ctypes.c_long)]
        
        def monitor_enum_proc(hmonitor, hdc, lprect, lparam):
            """監視器枚舉回調函數"""
            rect = lprect.contents
            monitors.append({
                'left': rect.left,
                'top': rect.top,
                'right': rect.right,
                'bottom': rect.bottom,
                'width': rect.right - rect.left,
                'height': rect.bottom - rect.top
            })
            return True
        
        # 設置回調函數類型
        MonitorEnumProc = ctypes.WINFUNCTYPE(
            ctypes.c_int,
            ctypes.c_ulong,
            ctypes.c_ulong,
            ctypes.POINTER(RECT),
            ctypes.c_ulong
        )
        
        # 調用 EnumDisplayMonitors
        user32 = ctypes.windll.user32
        callback = MonitorEnumProc(monitor_enum_proc)
        user32.EnumDisplayMonitors(None, None, callback, 0)
        
        return monitors
    
    def _create_overlay(self):
        """創建全螢幕遮罩視窗（支援多螢幕）"""
        if not self.parent_root:
            # 如果沒有父視窗，創建一個臨時的
            self.parent_root = tk.Tk()
            self.parent_root.withdraw()  # 隱藏父視窗
        
        # 獲取所有顯示器
        monitors = self._get_all_monitors()
        
        if not monitors:
            # 如果無法獲取顯示器信息，使用主螢幕
            temp_root = tk.Tk()
            temp_root.withdraw()
            screen_width = temp_root.winfo_screenwidth()
            screen_height = temp_root.winfo_screenheight()
            monitors = [{'left': 0, 'top': 0, 'width': screen_width, 'height': screen_height}]
            temp_root.destroy()
        
        # 為每個顯示器創建遮罩視窗
        for monitor in monitors:
            overlay = tk.Toplevel(self.parent_root)
            overlay.title("")
            
            # 移除標題欄
            overlay.overrideredirect(True)
            
            # 設置置頂
            overlay.attributes('-topmost', True)
            
            # 設置透明黑色背景
            overlay.configure(bg='black')
            overlay.attributes('-alpha', 0.7)  # 70% 透明度
            
            # 設置視窗位置和大小
            x = monitor['left']
            y = monitor['top']
            width = monitor['width']
            height = monitor['height']
            overlay.geometry(f"{width}x{height}+{x}+{y}")
            
            # 創建倒數標籤（只在主螢幕顯示，或每個螢幕都顯示）
            # 這裡選擇在主螢幕（第一個）顯示倒數，其他螢幕只顯示遮罩
            if len(self.countdown_labels) == 0:
                # 主螢幕顯示倒數數字
                label = tk.Label(
                    overlay,
                    text="5",
                    font=("Arial", 200, "bold"),
                    fg="white",
                    bg="black"
                )
                label.place(relx=0.5, rely=0.5, anchor="center")
                self.countdown_labels.append(label)
            else:
                # 其他螢幕不顯示數字，只顯示遮罩
                self.countdown_labels.append(None)
            
            # 更新視窗以確保所有設置生效
            overlay.update_idletasks()
            
            # 確保視窗置頂
            overlay.lift()
            
            self.overlay_windows.append(overlay)
        
        # 確保第一個視窗獲得焦點並捕獲輸入
        if self.overlay_windows:
            self.overlay_windows[0].focus_force()
            self.overlay_windows[0].grab_set()  # 捕獲所有輸入
        
        # 強制更新所有視窗
        for overlay in self.overlay_windows:
            overlay.update()
    
    def _countdown_loop(self):
        """倒數循環：5, 4, 3, 2, 1"""
        for i in range(5, 0, -1):
            if not self.is_showing:
                break
            
            # 在主線程中更新標籤（只更新主螢幕的標籤）
            if self.overlay_windows and self.countdown_labels and self.countdown_labels[0]:
                self.overlay_windows[0].after(0, lambda n=i: self.countdown_labels[0].config(text=str(n)))
            
            time.sleep(1)
        
        # 倒數完成後關閉遮罩
        if self.is_showing:
            self.hide()
            
            # 執行完成回調
            if self.on_countdown_complete:
                self.on_countdown_complete()
    
    def hide(self):
        """隱藏遮罩視窗（所有螢幕）"""
        if not self.is_showing:
            return
        
        self.is_showing = False
        
        # 關閉所有遮罩視窗
        for overlay in self.overlay_windows:
            try:
                if overlay == self.overlay_windows[0]:
                    overlay.grab_release()
                overlay.destroy()
            except:
                pass
        
        self.overlay_windows.clear()
        self.countdown_labels.clear()

