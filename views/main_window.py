"""主視窗 View - 使用 tkinter 創建 GUI"""
import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable
import os
import sys


class MainWindow:
    """主視窗類 - 顯示計時器界面"""
    
    def __init__(self, root: Optional[tk.Tk] = None):
        """
        初始化主視窗
        
        Args:
            root: tkinter root 視窗，如果為 None 則創建新的
        """
        self.root = root if root else tk.Tk()
        self.root.title("Relax Time - 時間管理工具")
        self.root.resizable(False, False)
        
        # 設置視窗圖標（鬧鐘圖標）
        self._set_icon()
        
        # 回調函數
        self.on_start: Optional[Callable[[], None]] = None
        self.on_pause: Optional[Callable[[], None]] = None
        self.on_stop: Optional[Callable[[], None]] = None
        self.on_duration_change: Optional[Callable[[int], None]] = None
        self.on_minimize_to_tray: Optional[Callable[[], None]] = None
        self.on_loop_mode_change: Optional[Callable[[bool], None]] = None
        
        self._setup_ui()
        self._center_window()
    
    def _set_icon(self):
        """設置視窗圖標"""
        # 如果是打包後的 exe
        if getattr(sys, 'frozen', False):
            # PyInstaller 打包後的臨時文件夾
            if hasattr(sys, '_MEIPASS'):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(sys.executable)
            icon_path = os.path.join(base_path, "resources", "alarm_clock.ico")
        else:
            # 開發環境路徑
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            icon_path = os.path.join(base_path, "resources", "alarm_clock.ico")
        
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception as e:
                print(f"無法載入圖標: {e}")
    
    def _setup_ui(self):
        """設置 UI 元件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 時間顯示標籤
        self.time_label = tk.Label(
            main_frame,
            text="30:00",
            font=("Arial", 48, "bold"),
            fg="#2c3e50"
        )
        self.time_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 狀態標籤
        self.status_label = tk.Label(
            main_frame,
            text="準備就緒",
            font=("Arial", 12),
            fg="#7f8c8d"
        )
        self.status_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # 時間調整框架
        time_frame = ttk.LabelFrame(main_frame, text="時間設定（分鐘）", padding="10")
        time_frame.grid(row=2, column=0, columnspan=3, pady=(0, 20), sticky=(tk.W, tk.E))
        
        # 減少時間按鈕
        self.decrease_btn = ttk.Button(
            time_frame,
            text="−5",
            width=5,
            command=self._decrease_time
        )
        self.decrease_btn.grid(row=0, column=0, padx=(0, 10))
        
        # 時間顯示（可調整）
        self.duration_var = tk.StringVar(value="30")
        self.duration_entry = ttk.Entry(
            time_frame,
            textvariable=self.duration_var,
            width=10,
            font=("Arial", 14),
            justify="center"
        )
        self.duration_entry.grid(row=0, column=1, padx=5)
        self.duration_entry.bind("<Return>", self._on_duration_entry_change)
        self.duration_entry.bind("<FocusOut>", self._on_duration_entry_change)
        
        # 增加時間按鈕
        self.increase_btn = ttk.Button(
            time_frame,
            text="+5",
            width=5,
            command=self._increase_time
        )
        self.increase_btn.grid(row=0, column=2, padx=(10, 0))
        
        # 控制按鈕框架
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=3, pady=(0, 20))
        
        # Start 按鈕
        self.start_btn = ttk.Button(
            control_frame,
            text="開始",
            width=10,
            command=self._on_start
        )
        self.start_btn.grid(row=0, column=0, padx=5)
        
        # Pause 按鈕
        self.pause_btn = ttk.Button(
            control_frame,
            text="暫停",
            width=10,
            command=self._on_pause
        )
        self.pause_btn.grid(row=0, column=1, padx=5)
        
        # Stop 按鈕
        self.stop_btn = ttk.Button(
            control_frame,
            text="停止",
            width=10,
            command=self._on_stop
        )
        self.stop_btn.grid(row=0, column=2, padx=5)
        
        # 循環模式開關
        loop_frame = ttk.Frame(main_frame)
        loop_frame.grid(row=4, column=0, columnspan=3, pady=(0, 10))
        
        self.loop_mode_var = tk.BooleanVar(value=False)
        self.loop_checkbox = ttk.Checkbutton(
            loop_frame,
            text="循環模式（休息結束後自動重新開始）",
            variable=self.loop_mode_var,
            command=self._on_loop_mode_change
        )
        self.loop_checkbox.grid(row=0, column=0)
        
        # 開機啟動開關
        startup_frame = ttk.Frame(main_frame)
        startup_frame.grid(row=5, column=0, columnspan=3, pady=(0, 10))
        
        self.startup_var = tk.BooleanVar(value=False)
        self.startup_checkbox = ttk.Checkbutton(
            startup_frame,
            text="開機自動啟動",
            variable=self.startup_var,
            command=self._on_startup_toggle
        )
        self.startup_checkbox.grid(row=0, column=0)
        
        # 最小化到托盤按鈕
        self.tray_btn = ttk.Button(
            main_frame,
            text="最小化到托盤",
            command=self._on_minimize_to_tray
        )
        self.tray_btn.grid(row=6, column=0, columnspan=3)
        
        # 綁定視窗關閉事件
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _center_window(self):
        """將視窗置於螢幕中央"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def _decrease_time(self):
        """減少時間（5分鐘）"""
        try:
            current = int(self.duration_var.get())
            new_value = max(5, current - 5)
            self.duration_var.set(str(new_value))
            if self.on_duration_change:
                self.on_duration_change(new_value)
        except ValueError:
            self.duration_var.set("30")
    
    def _increase_time(self):
        """增加時間（5分鐘）"""
        try:
            current = int(self.duration_var.get())
            new_value = current + 5
            self.duration_var.set(str(new_value))
            if self.on_duration_change:
                self.on_duration_change(new_value)
        except ValueError:
            self.duration_var.set("30")
    
    def _on_duration_entry_change(self, event=None):
        """當時間輸入框改變時"""
        try:
            value = int(self.duration_var.get())
            if value < 5:
                value = 5
            # 向下取整到 5 的倍數
            value = (value // 5) * 5
            self.duration_var.set(str(value))
            if self.on_duration_change:
                self.on_duration_change(value)
        except ValueError:
            self.duration_var.set("30")
    
    def _on_start(self):
        """開始按鈕點擊"""
        if self.on_start:
            self.on_start()
    
    def _on_pause(self):
        """暫停按鈕點擊"""
        if self.on_pause:
            self.on_pause()
    
    def _on_stop(self):
        """停止按鈕點擊"""
        if self.on_stop:
            self.on_stop()
    
    def _on_loop_mode_change(self):
        """循環模式開關改變"""
        if self.on_loop_mode_change:
            self.on_loop_mode_change(self.loop_mode_var.get())
    
    def _on_startup_toggle(self):
        """開機啟動開關改變"""
        if self.on_startup_toggle:
            self.on_startup_toggle(self.startup_var.get())
    
    def _on_minimize_to_tray(self):
        """最小化到托盤"""
        if self.on_minimize_to_tray:
            self.on_minimize_to_tray()
    
    def _on_close(self):
        """視窗關閉事件 - 隱藏而非關閉"""
        if self.on_minimize_to_tray:
            self.on_minimize_to_tray()
    
    def set_loop_mode(self, enabled: bool):
        """設置循環模式狀態"""
        self.loop_mode_var.set(enabled)
    
    def get_loop_mode(self) -> bool:
        """取得循環模式狀態"""
        return self.loop_mode_var.get()
    
    def set_startup_enabled(self, enabled: bool):
        """設置開機啟動狀態"""
        self.startup_var.set(enabled)
    
    def update_time_display(self, seconds: int):
        """
        更新時間顯示
        
        Args:
            seconds: 剩餘秒數
        """
        minutes = seconds // 60
        secs = seconds % 60
        self.time_label.config(text=f"{minutes:02d}:{secs:02d}")
    
    def update_status(self, status: str):
        """
        更新狀態標籤
        
        Args:
            status: 狀態文字
        """
        self.status_label.config(text=status)
    
    def set_duration(self, minutes: int):
        """
        設定時間顯示
        
        Args:
            minutes: 分鐘數
        """
        self.duration_var.set(str(minutes))
    
    def update_button_states(self, state: str):
        """
        更新按鈕狀態
        
        Args:
            state: 狀態 ("idle", "running", "paused", "resting")
        """
        if state == "idle":
            self.start_btn.config(state="normal")
            self.pause_btn.config(state="disabled")
            self.stop_btn.config(state="disabled")
        elif state == "running":
            self.start_btn.config(state="disabled")
            self.pause_btn.config(state="normal")
            self.stop_btn.config(state="normal")
        elif state == "paused":
            self.start_btn.config(state="normal")
            self.pause_btn.config(state="disabled")
            self.stop_btn.config(state="normal")
        elif state == "resting":
            self.start_btn.config(state="disabled")
            self.pause_btn.config(state="disabled")
            self.stop_btn.config(state="disabled")
    
    def show(self):
        """顯示視窗"""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self._center_window()
    
    def hide(self):
        """隱藏視窗"""
        self.root.withdraw()
    
    def is_visible(self) -> bool:
        """檢查視窗是否可見"""
        return self.root.winfo_viewable()
    
    def run(self):
        """運行視窗主迴圈"""
        self.root.mainloop()

