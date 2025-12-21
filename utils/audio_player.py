"""音頻播放工具 - 用於播放提示音"""
import os
import sys
import threading
from typing import Optional


class AudioPlayer:
    """音頻播放器類 - 用於播放 MP3 音頻文件"""
    
    @staticmethod
    def get_audio_path(filename: str) -> str:
        """
        獲取音頻文件路徑
        
        Args:
            filename: 音頻文件名
            
        Returns:
            音頻文件的完整路徑
        """
        # 如果是打包後的 exe
        if getattr(sys, 'frozen', False):
            if hasattr(sys, '_MEIPASS'):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(sys.executable)
            audio_path = os.path.join(base_path, "resources", filename)
        else:
            # 開發環境路徑
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            audio_path = os.path.join(base_path, "resources", filename)
        
        return audio_path
    
    @staticmethod
    def play_countdown_alarm():
        """
        播放倒數提示音（18秒倒數）
        
        Returns:
            bool: 播放是否成功
        """
        try:
            import pyglet
            
            audio_path = AudioPlayer.get_audio_path("countdown_alarm.mp3")
            
            if not os.path.exists(audio_path):
                print(f"警告: 找不到音頻文件: {audio_path}")
                return False
            
            # 在獨立線程中播放音頻，避免阻塞
            def play_in_thread():
                try:
                    # 創建音頻播放器
                    source = pyglet.media.load(audio_path, streaming=False)
                    player = pyglet.media.Player()
                    player.queue(source)
                    player.play()
                    
                    # 等待播放完成（最多10秒）
                    import time
                    start_time = time.time()
                    max_duration = min(source.duration or 10, 10)
                    
                    while player.playing and (time.time() - start_time) < max_duration:
                        time.sleep(0.1)
                        # 需要在線程中處理 pyglet 事件（如果需要）
                        # 但對於非流式播放，通常不需要
                    
                    # 清理資源
                    player.pause()
                    player.delete()
                except Exception as e:
                    print(f"播放音頻時發生錯誤: {e}")
            
            thread = threading.Thread(target=play_in_thread, daemon=True)
            thread.start()
            return True
            
        except ImportError:
            print("警告: pyglet 未安裝，無法播放音頻")
            print("請運行: uv sync")
            return False
        except Exception as e:
            print(f"播放音頻時發生錯誤: {e}")
            return False

