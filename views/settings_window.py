"""設定視窗 View - 使用 tkinter 創建設定對話框"""
import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable


class SettingsWindow:
    """設定視窗類 - 顯示應用程式設定"""
    
    def __init__(self, parent: tk.Tk):
        """
        初始化設定視窗
        
        Args:
            parent: 父視窗
        """
        self.parent = parent
        self.window: Optional[tk.Toplevel] = None
        
        # 回調函數
        self.on_loop_mode_change: Optional[Callable[[bool], None]] = None
        self.on_startup_toggle: Optional[Callable[[bool], None]] = None
        self.on_rest_duration_change: Optional[Callable[[int], None]] = None
        self.on_minimize_to_tray: Optional[Callable[[], None]] = None
        
        # 存儲初始值（在 UI 創建前設置的值）
        self._initial_loop_mode: Optional[bool] = None
        self._initial_startup_enabled: Optional[bool] = None
        self._initial_rest_duration: Optional[int] = None
        
        # UI 變數（在 _setup_ui 中初始化）
        self.loop_mode_var: Optional[tk.BooleanVar] = None
        self.startup_var: Optional[tk.BooleanVar] = None
        self.rest_duration_var: Optional[tk.StringVar] = None
        self.rest_duration_entry: Optional[ttk.Entry] = None
    
    def show(self):
        """顯示設定視窗"""
        if self.window and self.window.winfo_exists():
            # 如果視窗已經存在，則將其置於前台
            self.window.lift()
            self.window.focus_force()
            return
        
        # 創建新視窗
        self.window = tk.Toplevel(self.parent)
        self.window.title("設定 - Relax Time")
        self.window.resizable(False, False)
        self.window.transient(self.parent)  # 設置為父視窗的臨時視窗
        self.window.grab_set()  # 設置為模態對話框
        
        # 綁定關閉事件
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)
        
        self._setup_ui()
        self._center_window()
    
    def _setup_ui(self):
        """設置 UI 元件"""
        # 主框架
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 設定項目框架
        settings_frame = ttk.LabelFrame(main_frame, text="設定選項", padding="15")
        settings_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky=(tk.W, tk.E))
        
        row = 0
        
        # 循環模式
        initial_loop_mode = self._initial_loop_mode if self._initial_loop_mode is not None else False
        self.loop_mode_var = tk.BooleanVar(value=initial_loop_mode)
        loop_checkbox = ttk.Checkbutton(
            settings_frame,
            text="循環模式",
            variable=self.loop_mode_var,
            command=self._on_loop_mode_change
        )
        loop_checkbox.grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Label(
            settings_frame,
            text="休息結束後自動重新開始工作計時",
            foreground="gray"
        ).grid(row=row, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        row += 1
        
        # 開機自動啟動
        initial_startup = self._initial_startup_enabled if self._initial_startup_enabled is not None else False
        self.startup_var = tk.BooleanVar(value=initial_startup)
        startup_checkbox = ttk.Checkbutton(
            settings_frame,
            text="開機自動啟動",
            variable=self.startup_var,
            command=self._on_startup_toggle
        )
        startup_checkbox.grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Label(
            settings_frame,
            text="Windows 啟動時自動執行（隱藏模式）",
            foreground="gray"
        ).grid(row=row, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        row += 1
        
        # 分隔線
        ttk.Separator(settings_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10
        )
        row += 1
        
        # 休息時間設定
        rest_frame = ttk.Frame(settings_frame)
        rest_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(
            rest_frame,
            text="休息時間（分鐘）：",
            font=("Arial", 10)
        ).grid(row=0, column=0, sticky=tk.W)
        
        # 減少休息時間按鈕
        decrease_rest_btn = ttk.Button(
            rest_frame,
            text="−5",
            width=4,
            command=self._decrease_rest_time
        )
        decrease_rest_btn.grid(row=0, column=1, padx=(10, 5))
        
        # 休息時間顯示（可調整）
        initial_rest = self._initial_rest_duration if self._initial_rest_duration is not None else 5
        self.rest_duration_var = tk.StringVar(value=str(initial_rest))
        self.rest_duration_entry = ttk.Entry(
            rest_frame,
            textvariable=self.rest_duration_var,
            width=8,
            font=("Arial", 11),
            justify="center"
        )
        self.rest_duration_entry.grid(row=0, column=2, padx=5)
        self.rest_duration_entry.bind("<Return>", self._on_rest_duration_entry_change)
        self.rest_duration_entry.bind("<FocusOut>", self._on_rest_duration_entry_change)
        
        # 增加休息時間按鈕
        increase_rest_btn = ttk.Button(
            rest_frame,
            text="+5",
            width=4,
            command=self._increase_rest_time
        )
        increase_rest_btn.grid(row=0, column=3, padx=(5, 0))
        
        ttk.Label(
            settings_frame,
            text="設定工作時間結束後的休息時長（以 5 分鐘為單位）",
            foreground="gray",
            font=("Arial", 9)
        ).grid(row=row+1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        row += 2
        
        # 分隔線
        ttk.Separator(settings_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10
        )
        row += 1
        
        # 最小化到托盤按鈕
        minimize_btn = ttk.Button(
            settings_frame,
            text="最小化到托盤",
            command=self._on_minimize_to_tray
        )
        minimize_btn.grid(row=row, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        row += 1
        
        ttk.Label(
            settings_frame,
            text="將視窗隱藏到系統托盤",
            foreground="gray",
            font=("Arial", 9)
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        # 按鈕框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=(0, 0))
        
        # 確定按鈕
        ok_btn = ttk.Button(
            button_frame,
            text="確定",
            width=10,
            command=self._on_close
        )
        ok_btn.grid(row=0, column=0, padx=5)
        ok_btn.focus_set()  # 設置為默認按鈕
    
    def _center_window(self):
        """將視窗置於父視窗中央"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        
        # 相對於父視窗居中
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def _decrease_rest_time(self):
        """減少休息時間（5分鐘）"""
        try:
            current = int(self.rest_duration_var.get())
            new_value = max(5, current - 5)
            self.rest_duration_var.set(str(new_value))
            if self.on_rest_duration_change:
                self.on_rest_duration_change(new_value)
        except ValueError:
            self.rest_duration_var.set("5")
    
    def _increase_rest_time(self):
        """增加休息時間（5分鐘）"""
        try:
            current = int(self.rest_duration_var.get())
            new_value = current + 5
            self.rest_duration_var.set(str(new_value))
            if self.on_rest_duration_change:
                self.on_rest_duration_change(new_value)
        except ValueError:
            self.rest_duration_var.set("5")
    
    def _on_rest_duration_entry_change(self, event=None):
        """當休息時間輸入框改變時"""
        try:
            value = int(self.rest_duration_var.get())
            if value < 5:
                value = 5
            # 向下取整到 5 的倍數
            value = (value // 5) * 5
            self.rest_duration_var.set(str(value))
            if self.on_rest_duration_change:
                self.on_rest_duration_change(value)
        except ValueError:
            self.rest_duration_var.set("5")
    
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
            # 最小化後關閉設定視窗
            self._on_close()
    
    def _on_close(self):
        """關閉視窗"""
        if self.window:
            self.window.destroy()
            self.window = None
    
    def set_loop_mode(self, enabled: bool):
        """設置循環模式狀態"""
        if self.loop_mode_var is not None:
            self.loop_mode_var.set(enabled)
        else:
            self._initial_loop_mode = enabled
    
    def set_startup_enabled(self, enabled: bool):
        """設置開機啟動狀態"""
        if self.startup_var is not None:
            self.startup_var.set(enabled)
        else:
            self._initial_startup_enabled = enabled
    
    def set_rest_duration(self, minutes: int):
        """設置休息時間"""
        if self.rest_duration_var is not None:
            self.rest_duration_var.set(str(minutes))
        else:
            self._initial_rest_duration = minutes

