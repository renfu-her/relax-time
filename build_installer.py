"""構建安裝程式的腳本"""
import os
import subprocess
import sys
from pathlib import Path

def find_inno_setup():
    """查找 Inno Setup 編譯器"""
    # 常見的安裝路徑
    possible_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
        r"C:\Program Files\Inno Setup 5\ISCC.exe",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

def build_installer():
    """構建安裝程式"""
    # 檢查 exe 文件是否存在
    exe_path = Path("dist/RelaxTime.exe")
    if not exe_path.exists():
        print("錯誤: 找不到 dist/RelaxTime.exe")
        print("請先運行: uv run pyinstaller pyinstaller.spec")
        return False
    
    # 查找 Inno Setup
    iscc_path = find_inno_setup()
    if not iscc_path:
        print("錯誤: 找不到 Inno Setup 編譯器")
        print("請先安裝 Inno Setup: https://jrsoftware.org/isinfo.php")
        print("或手動運行 Inno Setup Compiler 打開 setup.iss 文件")
        return False
    
    # 確保輸出目錄存在
    os.makedirs("installer", exist_ok=True)
    
    # 運行 Inno Setup 編譯器
    print(f"使用 Inno Setup: {iscc_path}")
    print("正在編譯安裝程式...")
    
    try:
        result = subprocess.run(
            [iscc_path, "setup.iss"],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print("\n✓ 安裝程式構建成功！")
        print(f"輸出目錄: {os.path.abspath('installer')}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"錯誤: 編譯失敗")
        print(e.stderr)
        return False
    except Exception as e:
        print(f"錯誤: {e}")
        return False

if __name__ == "__main__":
    success = build_installer()
    sys.exit(0 if success else 1)

