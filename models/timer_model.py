"""Timer Model - 管理時間狀態和設定"""
from enum import Enum
from typing import Callable, Optional
import time


class TimerState(Enum):
    """計時器狀態"""
    IDLE = "idle"           # 閒置
    RUNNING = "running"     # 運行中
    PAUSED = "paused"       # 暫停
    RESTING = "resting"     # 休息中


class TimerModel:
    """計時器模型 - 管理時間邏輯和狀態"""
    
    def __init__(self, default_duration: int = 30, rest_duration: int = 5):
        """
        初始化計時器模型
        
        Args:
            default_duration: 預設工作時間（分鐘）
            rest_duration: 休息時間（分鐘）
        """
        self.default_duration = default_duration
        self.rest_duration = rest_duration
        self.current_duration = default_duration  # 當前設定時間（分鐘）
        self.remaining_seconds = default_duration * 60  # 剩餘秒數
        self.rest_remaining_seconds = rest_duration * 60
        self.state = TimerState.IDLE
        self.pause_time: Optional[float] = None
        self.start_time: Optional[float] = None
        self.elapsed_before_pause = 0  # 暫停前已過時間（秒）
        self.loop_mode = False  # 循環模式：休息結束後自動重新開始
        
        # 回調函數
        self.on_time_update: Optional[Callable[[int], None]] = None
        self.on_state_change: Optional[Callable[[TimerState], None]] = None
        self.on_timer_complete: Optional[Callable[[], None]] = None
        self.on_rest_complete: Optional[Callable[[], None]] = None
        self.on_countdown_warning: Optional[Callable[[], None]] = None  # 倒數18秒警告
        self.on_final_countdown: Optional[Callable[[], None]] = None  # 倒數5秒遮罩
    
    def set_loop_mode(self, enabled: bool):
        """設置循環模式"""
        self.loop_mode = enabled
    
    def get_loop_mode(self) -> bool:
        """取得循環模式狀態"""
        return self.loop_mode
    
    def set_rest_duration(self, minutes: int):
        """
        設定休息時間
        
        Args:
            minutes: 分鐘數（必須是 5 的倍數）
        """
        if minutes < 5:
            minutes = 5
        # 向下取整到 5 的倍數
        minutes = (minutes // 5) * 5
        self.rest_duration = minutes
        if self.state == TimerState.IDLE:
            self.rest_remaining_seconds = minutes * 60
    
    def get_rest_duration(self) -> int:
        """取得當前設定的休息時間（分鐘）"""
        return self.rest_duration
    
    def set_duration(self, minutes: int):
        """
        設定計時時間
        
        Args:
            minutes: 分鐘數（必須是 5 的倍數）
        """
        if minutes < 5:
            minutes = 5
        # 向下取整到 5 的倍數
        minutes = (minutes // 5) * 5
        self.current_duration = minutes
        if self.state == TimerState.IDLE:
            self.remaining_seconds = minutes * 60
    
    def adjust_duration(self, delta: int):
        """
        調整時間（以 5 分鐘為單位）
        
        Args:
            delta: 調整量（正數增加，負數減少）
        """
        new_duration = self.current_duration + (delta * 5)
        if new_duration < 5:
            new_duration = 5
        self.set_duration(new_duration)
    
    def start(self):
        """開始計時"""
        if self.state == TimerState.RUNNING:
            return
        
        if self.state == TimerState.PAUSED:
            # 從暫停恢復
            self.start_time = time.time()
            self.state = TimerState.RUNNING
        else:
            # 新開始
            self.remaining_seconds = self.current_duration * 60
            self.start_time = time.time()
            self.elapsed_before_pause = 0
            self.state = TimerState.RUNNING
            self.countdown_warning_played = False  # 重置警告音標記
            self.final_countdown_shown = False  # 重置倒數5秒遮罩標記
        
        if self.on_state_change:
            self.on_state_change(self.state)
    
    def pause(self):
        """暫停計時"""
        if self.state != TimerState.RUNNING:
            return
        
        self.elapsed_before_pause += time.time() - (self.start_time or time.time())
        self.pause_time = time.time()
        self.state = TimerState.PAUSED
        
        if self.on_state_change:
            self.on_state_change(self.state)
    
    def stop(self):
        """停止計時"""
        self.state = TimerState.IDLE
        self.remaining_seconds = self.current_duration * 60
        self.rest_remaining_seconds = self.rest_duration * 60
        self.start_time = None
        self.pause_time = None
        self.elapsed_before_pause = 0
        self.countdown_warning_played = False
        self.final_countdown_shown = False
        
        if self.on_state_change:
            self.on_state_change(self.state)
    
    def start_rest(self):
        """開始休息時間"""
        self.state = TimerState.RESTING
        self.rest_remaining_seconds = self.rest_duration * 60
        self.start_time = time.time()
        self.elapsed_before_pause = 0
        self.final_countdown_shown = False  # 重置倒數5秒遮罩標記
        
        if self.on_state_change:
            self.on_state_change(self.state)
    
    def update(self):
        """
        更新計時器（每秒調用一次）
        
        Returns:
            bool: 如果時間到返回 True
        """
        if self.state == TimerState.RUNNING:
            if self.start_time:
                elapsed = self.elapsed_before_pause + (time.time() - self.start_time)
                self.remaining_seconds = max(0, int(self.current_duration * 60 - elapsed))
                
                if self.on_time_update:
                    self.on_time_update(self.remaining_seconds)
                
                # 倒數18秒時播放提示音（只播放一次）
                if self.remaining_seconds == 18 and not self.countdown_warning_played:
                    self.countdown_warning_played = True
                    if self.on_countdown_warning:
                        self.on_countdown_warning()
                
                # 倒數5秒時顯示全螢幕遮罩（只顯示一次）
                if self.remaining_seconds == 5 and not self.final_countdown_shown:
                    self.final_countdown_shown = True
                    if self.on_final_countdown:
                        self.on_final_countdown()
                
                if self.remaining_seconds <= 0:
                    self.state = TimerState.IDLE
                    if self.on_timer_complete:
                        self.on_timer_complete()
                    return True
        
        elif self.state == TimerState.RESTING:
            if self.start_time:
                elapsed = self.elapsed_before_pause + (time.time() - self.start_time)
                self.rest_remaining_seconds = max(0, int(self.rest_duration * 60 - elapsed))
                
                if self.on_time_update:
                    self.on_time_update(self.rest_remaining_seconds)
                
                # 休息時間倒數5秒時顯示全螢幕遮罩（只顯示一次）
                if self.rest_remaining_seconds == 5 and not self.final_countdown_shown:
                    self.final_countdown_shown = True
                    if self.on_final_countdown:
                        self.on_final_countdown()
                
                if self.rest_remaining_seconds <= 0:
                    self.state = TimerState.IDLE
                    if self.on_rest_complete:
                        self.on_rest_complete()
                    return True
        
        return False
    
    def get_remaining_time_formatted(self) -> str:
        """取得格式化的剩餘時間字串 (MM:SS)"""
        if self.state == TimerState.RESTING:
            total_seconds = self.rest_remaining_seconds
        else:
            total_seconds = self.remaining_seconds
        
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def get_current_duration(self) -> int:
        """取得當前設定的時間（分鐘）"""
        return self.current_duration

