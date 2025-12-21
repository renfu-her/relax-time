"""圖標生成工具 - 生成鬧鐘圖標"""
from PIL import Image, ImageDraw
import os


def create_alarm_clock_icon(output_path: str = "resources/alarm_clock.ico"):
    """
    創建鬧鐘圖標
    
    Args:
        output_path: 輸出路徑
    """
    # 確保目錄存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 創建多種尺寸的圖標（Windows 需要）
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    images = []
    
    for size in sizes:
        # 創建透明背景
        image = Image.new('RGBA', size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        
        width, height = size
        center_x, center_y = width // 2, height // 2
        radius = min(width, height) // 2 - 2
        
        # 繪製鬧鐘外框（圓形帶底盤）
        # 底盤
        draw.ellipse(
            [center_x - radius - 2, center_y - radius - 2, 
             center_x + radius + 2, center_y + radius + 2],
            fill=(70, 130, 180, 255),  # 鋼藍色
            outline=(50, 100, 150, 255),
            width=max(1, width // 32)
        )
        
        # 主要圓形
        draw.ellipse(
            [center_x - radius, center_y - radius,
             center_x + radius, center_y + radius],
            fill=(255, 255, 255, 255),  # 白色
            outline=(50, 100, 150, 255),
            width=max(1, width // 32)
        )
        
        # 繪製時鐘刻度（12, 3, 6, 9 點位置）
        tick_length = radius // 4
        for angle in [0, 90, 180, 270]:
            import math
            rad = math.radians(angle)
            x1 = center_x + (radius - tick_length) * math.cos(rad)
            y1 = center_y - (radius - tick_length) * math.sin(rad)
            x2 = center_x + radius * math.cos(rad)
            y2 = center_y - radius * math.sin(rad)
            draw.line([x1, y1, x2, y2], fill=(0, 0, 0, 255), width=max(1, width // 32))
        
        # 繪製時針和分針（指向 3 點方向，像鬧鐘鈴聲）
        # 時針（指向 3）
        hour_length = radius * 0.4
        draw.line(
            [center_x, center_y, center_x + hour_length, center_y],
            fill=(0, 0, 0, 255),
            width=max(1, width // 16)
        )
        # 分針（指向 3，稍長）
        minute_length = radius * 0.6
        draw.line(
            [center_x, center_y, center_x + minute_length, center_y],
            fill=(0, 0, 0, 255),
            width=max(1, width // 20)
        )
        
        # 繪製鬧鐘頂部的鈴鐺（兩個小圓）
        bell_size = radius // 3
        # 左鈴鐺
        draw.ellipse(
            [center_x - radius - bell_size // 2, center_y - radius - bell_size // 2,
             center_x - radius + bell_size // 2, center_y - radius + bell_size // 2],
            fill=(255, 200, 0, 255),  # 金色
            outline=(200, 150, 0, 255),
            width=max(1, width // 64)
        )
        # 右鈴鐺
        draw.ellipse(
            [center_x + radius - bell_size // 2, center_y - radius - bell_size // 2,
             center_x + radius + bell_size // 2, center_y - radius + bell_size // 2],
            fill=(255, 200, 0, 255),  # 金色
            outline=(200, 150, 0, 255),
            width=max(1, width // 64)
        )
        
        images.append(image)
    
    # 保存為 ICO 文件
    if len(images) > 0:
        images[0].save(output_path, format='ICO', sizes=[(img.width, img.height) for img in images])
        print(f"圖標已保存至: {output_path}")
    return output_path


if __name__ == "__main__":
    create_alarm_clock_icon()

