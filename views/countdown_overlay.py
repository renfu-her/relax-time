"""全螢幕倒數遮罩視窗"""
import tkinter as tk
from typing import Optional, Callable
import threading
import time


class CountdownOverlay:
    """全螢幕透明黑色遮罩，顯示倒數 5, 4, 3, 2, 1"""
    
    def __init__(self, parent_root: Optional[tk.Tk] = None):
        """
        初始化遮罩視窗
        
        Args:
            parent_root: 父視窗（tk.Tk），用於創建 Toplevel
        """
        self.parent_root = parent_root
        self.overlay_root: Optional[tk.Toplevel] = None
        self.countdown_label: Optional[tk.Label] = None
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
    
    def _create_overlay(self):
        """創建全螢幕遮罩視窗"""
        if not self.parent_root:
            # 如果沒有父視窗，創建一個臨時的
            self.parent_root = tk.Tk()
            self.parent_root.withdraw()  # 隱藏父視窗
        
        # 創建頂層視窗
        self.overlay_root = tk.Toplevel(self.parent_root)
        self.overlay_root.title("")
        
        # 移除標題欄（必須在設置全螢幕之前）
        self.overlay_root.overrideredirect(True)
        
        # 設置置頂
        self.overlay_root.attributes('-topmost', True)
        
        # 手動設置全螢幕大小（因為 overrideredirect 和 -fullscreen 不能同時使用）
        screen_width = self.overlay_root.winfo_screenwidth()
        screen_height = self.overlay_root.winfo_screenheight()
        self.overlay_root.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # 設置透明黑色背景
        self.overlay_root.configure(bg='black')
        self.overlay_root.attributes('-alpha', 0.7)  # 70% 透明度
        
        # 創建倒數標籤
        self.countdown_label = tk.Label(
            self.overlay_root,
            text="5",
            font=("Arial", 200, "bold"),
            fg="white",
            bg="black"
        )
        self.countdown_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # 確保視窗獲得焦點
        self.overlay_root.focus_force()
        self.overlay_root.grab_set()  # 捕獲所有輸入
        
        # 更新視窗以確保顯示
        self.overlay_root.update()
    
    def _countdown_loop(self):
        """倒數循環：5, 4, 3, 2, 1"""
        for i in range(5, 0, -1):
            if not self.is_showing:
                break
            
            # 在主線程中更新標籤
            if self.overlay_root and self.countdown_label:
                self.overlay_root.after(0, lambda n=i: self.countdown_label.config(text=str(n)))
            
            time.sleep(1)
        
        # 倒數完成後關閉遮罩
        if self.is_showing:
            self.hide()
            
            # 執行完成回調
            if self.on_countdown_complete:
                self.on_countdown_complete()
    
    def hide(self):
        """隱藏遮罩視窗"""
        if not self.is_showing:
            return
        
        self.is_showing = False
        
        if self.overlay_root:
            try:
                self.overlay_root.grab_release()
                self.overlay_root.destroy()
            except:
                pass
            finally:
                self.overlay_root = None
                self.countdown_label = None

