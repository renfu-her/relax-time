"""構建 MSI 安裝程式的腳本 - 使用 WiX Toolset"""
import os
import sys
import subprocess
from pathlib import Path
import shutil

def print_step(step_name):
    """打印步驟名稱"""
    print("\n" + "="*60)
    print(f" {step_name}")
    print("="*60)

def find_wix_toolset():
    """查找 WiX Toolset 編譯器"""
    # WiX Toolset 的常見安裝位置
    possible_paths = [
        r"C:\Program Files (x86)\WiX Toolset v3.11\bin\candle.exe",
        r"C:\Program Files\WiX Toolset v3.11\bin\candle.exe",
        r"C:\Program Files (x86)\WiX Toolset v3.14\bin\candle.exe",
        r"C:\Program Files\WiX Toolset v3.14\bin\candle.exe",
    ]
    
    # 也可以從環境變量中查找
    wix_bin = os.environ.get("WIX", "")
    if wix_bin:
        candle_path = os.path.join(wix_bin, "bin", "candle.exe")
        if os.path.exists(candle_path):
            return os.path.dirname(candle_path)
    
    # 檢查常見路徑
    for path in possible_paths:
        if os.path.exists(path):
            return os.path.dirname(path)
    
    return None

def build_msi():
    """構建 MSI 安裝程式"""
    print_step("構建 MSI 安裝程式")
    
    # 檢查 exe 文件是否存在
    exe_path = Path("dist/RelaxTime.exe")
    if not exe_path.exists():
        print("錯誤: 找不到 dist/RelaxTime.exe")
        print("請先運行: uv run pyinstaller pyinstaller.spec")
        return False
    
    # 查找 WiX Toolset
    wix_bin_dir = find_wix_toolset()
    if not wix_bin_dir:
        print("錯誤: 找不到 WiX Toolset")
        print("請先安裝 WiX Toolset: https://wixtoolset.org/releases/")
        print("安裝後，將 WiX 的 bin 目錄添加到 PATH 環境變量，或設置 WIX 環境變量")
        return False
    
    candle_exe = os.path.join(wix_bin_dir, "candle.exe")
    light_exe = os.path.join(wix_bin_dir, "light.exe")
    
    if not os.path.exists(candle_exe) or not os.path.exists(light_exe):
        print(f"錯誤: 在 {wix_bin_dir} 中找不到 candle.exe 或 light.exe")
        return False
    
    print(f"使用 WiX Toolset: {wix_bin_dir}")
    
    # 確保輸出目錄存在
    os.makedirs("installer", exist_ok=True)
    
    # 步驟 1: 編譯 WXS 文件（生成 .wixobj）
    print("\n步驟 1: 編譯 WXS 文件...")
    wixobj_file = "installer\\setup.wixobj"
    
    try:
        result = subprocess.run(
            [candle_exe, "setup.wxs", "-out", wixobj_file],
            check=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"錯誤: 編譯 WXS 失敗")
        print(e.stderr)
        return False
    except Exception as e:
        print(f"錯誤: {e}")
        return False
    
    # 步驟 2: 鏈接生成 MSI（從 .wixobj 生成 .msi）
    print("\n步驟 2: 鏈接生成 MSI 文件...")
    msi_file = "installer\\RelaxTime-Setup-0.2.0.msi"
    
    try:
        result = subprocess.run(
            [light_exe, wixobj_file, "-out", msi_file, "-ext", "WixUIExtension"],
            check=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        
        # 檢查 MSI 文件是否生成
        if os.path.exists(msi_file):
            file_size = os.path.getsize(msi_file) / (1024 * 1024)  # MB
            print(f"\n✓ MSI 安裝程式構建成功: {msi_file} ({file_size:.2f} MB)")
            
            # 清理中間文件
            if os.path.exists(wixobj_file):
                os.remove(wixobj_file)
            
            return True
        else:
            print("錯誤: MSI 文件生成失敗")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"錯誤: 鏈接失敗")
        print(e.stderr)
        return False
    except Exception as e:
        print(f"錯誤: {e}")
        return False

def main():
    """主函數"""
    print("="*60)
    print(" Relax Time - 構建 MSI 安裝程式")
    print("="*60)
    
    if not build_msi():
        print("\n❌ MSI 構建失敗")
        sys.exit(1)
    
    print("\n" + "="*60)
    print(" ✓ 構建完成！")
    print("="*60)
    print(f"\nMSI 安裝程式: installer\\RelaxTime-Setup-0.2.0.msi")
    print("\n注意: MSI 文件需要先構建 exe 文件")
    print("如果還沒有 exe 文件，請先運行: uv run pyinstaller pyinstaller.spec")

if __name__ == "__main__":
    main()

