"""Timer Controller - 連接 Model 和 View 的控制器"""
import threading
import time
from typing import Optional

from models.timer_model import TimerModel, TimerState
from views.main_window import MainWindow
from views.tray_icon import TrayIcon
from views.settings_window import SettingsWindow
from views.countdown_overlay import CountdownOverlay
from utils.window_manager import WindowManager
from utils.startup_manager import StartupManager
from utils.audio_player import AudioPlayer
from utils.settings_db import get_settings_db


class TimerController:
    """計時器控制器 - 協調 Model 和 View 之間的交互"""
    
    def __init__(self):
        """初始化控制器"""
        # 初始化設定資料庫
        self.settings_db = get_settings_db()
        
        # 從資料庫載入設定
        default_duration = self.settings_db.get_int('default_duration', 30)
        rest_duration = self.settings_db.get_int('rest_duration', 5)
        
        # 初始化 Model
        self.model = TimerModel(default_duration=default_duration, rest_duration=rest_duration)
        
        # 載入循環模式設定
        loop_mode = self.settings_db.get_bool('loop_mode', False)
        self.model.set_loop_mode(loop_mode)
        
        # 初始化 View
        self.root = None
        self.view: Optional[MainWindow] = None
        self.tray: Optional[TrayIcon] = None
        
        # 計時器線程
        self.timer_thread: Optional[threading.Thread] = None
        self.running = False
        
        # 視窗管理器
        self.window_manager = WindowManager()
        
        # 倒數遮罩
        self.countdown_overlay: Optional[CountdownOverlay] = None
        
        # 設置 Model 回調
        self._setup_model_callbacks()
    
    def _setup_model_callbacks(self):
        """設置 Model 的回調函數"""
        self.model.on_time_update = self._on_time_update
        self.model.on_state_change = self._on_state_change
        self.model.on_timer_complete = self._on_timer_complete
        self.model.on_rest_complete = self._on_rest_complete
        self.model.on_countdown_warning = self._on_countdown_warning
        self.model.on_final_countdown = self._on_final_countdown
    
    def _on_countdown_warning(self):
        """倒數18秒警告回調 - 播放提示音"""
        print("倒數18秒，播放提示音...")
        AudioPlayer.play_countdown_alarm()
    
    def _on_final_countdown(self):
        """倒數5秒回調 - 顯示全螢幕遮罩（僅在工作時間）"""
        print("倒數5秒，顯示全螢幕遮罩...")
        
        # 只在工作時間顯示遮罩，休息時間不需要
        if self.model.state != TimerState.RUNNING:
            return
        
        # 確保在主線程中執行（tkinter 視窗必須在主線程中創建）
        if self.root:
            # 工作時間倒數5秒，完成後進入休息
            self.root.after(0, self._show_countdown_overlay, self._on_countdown_complete_for_rest)
        else:
            print("警告: 無法創建遮罩，root 視窗尚未初始化")
    
    def _show_countdown_overlay(self, on_complete):
        """在主線程中顯示遮罩"""
        # 確保遮罩已初始化
        if not self.countdown_overlay:
            if self.root:
                self.countdown_overlay = CountdownOverlay(parent_root=self.root)
            else:
                print("警告: 無法創建遮罩，root 視窗尚未初始化")
                return
        
        # 顯示遮罩
        self.countdown_overlay.show(on_complete=on_complete)
    
    def _on_countdown_complete_for_rest(self):
        """倒數完成後進入休息模式"""
        print("倒數完成，準備進入休息模式...")
        
        # 遮罩會在倒數完成後自動關閉
        # 視窗縮小和進入休息的邏輯將在 _on_timer_complete 中處理
        # 這裡只是確保倒數已完成
    
    def _on_countdown_complete_for_restore(self):
        """倒數完成後恢復視窗"""
        print("倒數完成，恢復視窗...")
        
        # 嘗試恢復所有視窗
        self.window_manager.restore_all_windows()
        
        # 顯示主視窗
        if self.view:
            self.view.show()
    
    def _on_time_update(self, seconds: int):
        """時間更新回調"""
        if self.view:
            self.view.update_time_display(seconds)
        
        # 更新托盤圖標提示
        if self.tray:
            minutes = seconds // 60
            secs = seconds % 60
            status_text = "準備就緒"
            if self.model.state == TimerState.RUNNING:
                status_text = f"工作中: {minutes:02d}:{secs:02d}"
            elif self.model.state == TimerState.PAUSED:
                status_text = f"已暫停: {minutes:02d}:{secs:02d}"
            elif self.model.state == TimerState.RESTING:
                status_text = f"休息中: {minutes:02d}:{secs:02d}"
            self.tray.update_tooltip(f"Relax Time - {status_text}")
    
    def _on_state_change(self, state: TimerState):
        """狀態改變回調"""
        if self.view:
            state_str = state.value
            self.view.update_button_states(state_str)
            
            # 更新狀態文字
            status_map = {
                TimerState.IDLE: "準備就緒",
                TimerState.RUNNING: "工作中...",
                TimerState.PAUSED: "已暫停",
                TimerState.RESTING: "休息中..."
            }
            self.view.update_status(status_map.get(state, "未知狀態"))
    
    def _on_timer_complete(self):
        """計時完成回調 - 進入休息模式"""
        print("工作時間到，進入休息模式...")
        
        # 最小化所有視窗
        self.window_manager.minimize_all_windows()
        
        # 隱藏主視窗（如果可見）
        if self.view:
            self.view.hide()
        
        # 開始休息時間
        self.model.start_rest()
    
    def _on_rest_complete(self):
        """休息完成回調"""
        print("休息時間到，恢復正常工作...")
        
        # 如果遮罩還在顯示，先關閉它
        if self.countdown_overlay and self.countdown_overlay.is_showing:
            self.countdown_overlay.hide()
        
        # 嘗試恢復所有視窗（使用 Win+Shift+M）
        # 注意: 這可能無法完美恢復所有視窗，但可以嘗試
        self.window_manager.restore_all_windows()
        
        # 顯示主視窗
        if self.view:
            self.view.show()
        
        # 如果循環模式開啟，自動重新開始
        if self.model.loop_mode:
            print("循環模式：自動重新開始計時...")
            # 重置為 IDLE 狀態後立即重新開始
            self.model.stop()
            # 稍微延遲後自動開始
            import threading
            threading.Timer(1.0, self.start_timer).start()
        else:
            # 重置為 IDLE 狀態，可以重新開始
            self.model.stop()
    
    def _timer_loop(self):
        """計時器主迴圈（在獨立線程中運行）"""
        while self.running:
            self.model.update()
            time.sleep(1)
    
    def initialize_ui(self):
        """初始化 UI"""
        import tkinter as tk
        
        self.root = tk.Tk()
        self.view = MainWindow(self.root)
        
        # 設置 View 回調
        self.view.on_start = self.start_timer
        self.view.on_pause = self.pause_timer
        self.view.on_stop = self.stop_timer
        self.view.on_duration_change = self.change_duration
        self.view.on_show_settings = self.show_settings
        
        # 創建設定視窗
        self.settings = SettingsWindow(self.root)
        self.settings.on_loop_mode_change = self.set_loop_mode
        self.settings.on_startup_toggle = self.toggle_startup
        self.settings.on_rest_duration_change = self.change_rest_duration
        self.settings.on_minimize_to_tray = self.minimize_to_tray
        
        # 初始化設定視窗狀態
        # 從資料庫載入開機啟動設定，如果資料庫沒有則從系統讀取
        startup_enabled = self.settings_db.get_bool('startup_enabled', None)
        if startup_enabled is None:
            # 如果資料庫沒有，從系統讀取
            startup_enabled = StartupManager.is_startup_enabled()
            # 保存到資料庫
            self.settings_db.set_bool('startup_enabled', startup_enabled)
        else:
            # 如果資料庫有設定，同步到系統
            if startup_enabled:
                StartupManager.enable_startup()
            else:
                StartupManager.disable_startup()
        
        self.settings.set_startup_enabled(startup_enabled)
        self.settings.set_loop_mode(self.model.get_loop_mode())
        self.settings.set_rest_duration(self.model.get_rest_duration())
        
        # 初始化托盤圖標
        self.tray = TrayIcon()
        self.tray.on_show_window = self.show_window
        self.tray.on_exit = self.exit_app
        self.tray.start()
        
        # 初始化倒數遮罩（需要 root 視窗）
        self.countdown_overlay = CountdownOverlay(parent_root=self.root)
        
        # 初始化顯示
        self.view.set_duration(self.model.get_current_duration())
        self.view.update_time_display(self.model.remaining_seconds)
        self._on_state_change(self.model.state)
    
    def start_timer(self):
        """開始計時"""
        self.model.start()
        
        # 啟動計時器線程（如果還沒啟動）
        if not self.running:
            self.running = True
            self.timer_thread = threading.Thread(target=self._timer_loop, daemon=True)
            self.timer_thread.start()
    
    def pause_timer(self):
        """暫停計時"""
        self.model.pause()
    
    def stop_timer(self):
        """停止計時"""
        self.model.stop()
    
    def change_duration(self, minutes: int):
        """改變時間設定"""
        self.model.set_duration(minutes)
        # 保存到資料庫
        self.settings_db.set_int('default_duration', minutes)
        if self.model.state == TimerState.IDLE:
            self.view.update_time_display(self.model.remaining_seconds)
    
    def set_loop_mode(self, enabled: bool):
        """設置循環模式"""
        self.model.set_loop_mode(enabled)
        # 保存到資料庫
        self.settings_db.set_bool('loop_mode', enabled)
    
    def toggle_startup(self, enabled: bool):
        """切換開機啟動"""
        if enabled:
            StartupManager.enable_startup()
        else:
            StartupManager.disable_startup()
        # 保存到資料庫
        self.settings_db.set_bool('startup_enabled', enabled)
    
    def change_rest_duration(self, minutes: int):
        """改變休息時間設定"""
        self.model.set_rest_duration(minutes)
        # 保存到資料庫
        self.settings_db.set_int('rest_duration', minutes)
    
    def show_settings(self):
        """顯示設定視窗"""
        if self.settings:
            self.settings.show()
    
    def minimize_to_tray(self):
        """最小化到托盤"""
        if self.view:
            self.view.hide()
    
    def show_window(self):
        """顯示視窗"""
        if self.view:
            self.view.show()
    
    def exit_app(self):
        """退出應用程式"""
        self.running = False
        if self.tray:
            self.tray.stop()
        if self.root:
            self.root.quit()
            self.root.destroy()
    
    def run(self, start_hidden: bool = False):
        """
        運行應用程式
        
        Args:
            start_hidden: 是否啟動時隱藏
        """
        self.initialize_ui()
        
        if start_hidden:
            self.minimize_to_tray()
        
        # 啟動計時器線程（持續運行以更新時間）
        self.running = True
        self.timer_thread = threading.Thread(target=self._timer_loop, daemon=True)
        self.timer_thread.start()
        
        # 運行主視窗
        if self.root:
            self.root.mainloop()

