"""系統托盤圖標 View - 使用 pystray 創建托盤圖標"""
import threading
from PIL import Image, ImageDraw
import pystray
from typing import Optional, Callable


class TrayIcon:
    """系統托盤圖標類"""
    
    def __init__(self):
        """初始化托盤圖標"""
        self.icon: Optional[pystray.Icon] = None
        self.thread: Optional[threading.Thread] = None
        
        # 回調函數
        self.on_show_window: Optional[Callable[[], None]] = None
        self.on_exit: Optional[Callable[[], None]] = None
        
        self._create_icon()
    
    def _create_icon(self):
        """創建圖標圖像"""
        # 創建一個簡單的圖標（時鐘圖案）
        image = Image.new('RGB', (64, 64), color='white')
        draw = ImageDraw.Draw(image)
        
        # 繪製圓形外框
        draw.ellipse([8, 8, 56, 56], outline='black', width=3)
        
        # 繪製時針和分針（12點方向）
        center_x, center_y = 32, 32
        # 分針（指向12）
        draw.line([center_x, center_y, center_x, center_y - 20], fill='black', width=3)
        # 時針（指向12，稍短）
        draw.line([center_x, center_y, center_x, center_y - 15], fill='black', width=4)
        
        # 創建菜單
        menu = pystray.Menu(
            pystray.MenuItem('顯示視窗', self._on_show_window),
            pystray.MenuItem('退出', self._on_exit)
        )
        
        self.icon = pystray.Icon(
            "RelaxTime",
            image,
            "Relax Time - 時間管理工具",
            menu
        )
    
    def _on_show_window(self, icon: pystray.Icon, item: pystray.MenuItem):
        """顯示視窗菜單項點擊"""
        if self.on_show_window:
            self.on_show_window()
    
    def _on_exit(self, icon: pystray.Icon, item: pystray.MenuItem):
        """退出菜單項點擊"""
        if self.on_exit:
            self.on_exit()
    
    def run(self):
        """在背景執行托盤圖標"""
        if self.icon:
            self.icon.run()
    
    def start(self):
        """啟動托盤圖標（在獨立線程中）"""
        if self.thread and self.thread.is_alive():
            return
        
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()
    
    def stop(self):
        """停止托盤圖標"""
        if self.icon:
            self.icon.stop()
    
    def update_tooltip(self, text: str):
        """更新工具提示文字"""
        if self.icon:
            self.icon.title = text

