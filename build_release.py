"""構建發布版本的腳本 - 包含 exe 和安裝程式"""
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

def run_command(cmd, description):
    """運行命令並處理錯誤"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"錯誤: {e}")
        if e.stderr:
            print(e.stderr)
        return False
    except Exception as e:
        print(f"錯誤: {e}")
        return False

def build_exe():
    """構建 exe 文件"""
    print_step("步驟 1: 構建 exe 文件")
    
    # 檢查 pyinstaller 是否可用
    try:
        subprocess.run(["pyinstaller", "--version"], capture_output=True, check=True)
    except:
        print("錯誤: 找不到 pyinstaller")
        print("請先運行: uv sync")
        return False
    
    # 清理舊的構建文件
    if os.path.exists("build"):
        print("清理舊的構建文件...")
        shutil.rmtree("build")
    
    # 運行 pyinstaller
    success = run_command(
        "pyinstaller pyinstaller.spec",
        "使用 PyInstaller 打包"
    )
    
    if not success:
        return False
    
    # 檢查輸出文件
    exe_path = Path("dist/RelaxTime.exe")
    if not exe_path.exists():
        print("錯誤: exe 文件生成失敗")
        return False
    
    file_size = exe_path.stat().st_size / (1024 * 1024)  # MB
    print(f"\n✓ exe 文件構建成功: {exe_path} ({file_size:.2f} MB)")
    return True

def build_installer():
    """構建安裝程式"""
    print_step("步驟 2: 構建安裝程式")
    
    # 檢查 exe 是否存在
    if not Path("dist/RelaxTime.exe").exists():
        print("錯誤: 找不到 dist/RelaxTime.exe")
        print("請先運行步驟 1 構建 exe 文件")
        return False
    
    # 檢查 Inno Setup
    inno_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
        r"C:\Program Files\Inno Setup 5\ISCC.exe",
    ]
    
    iscc_path = None
    for path in inno_paths:
        if os.path.exists(path):
            iscc_path = path
            break
    
    if not iscc_path:
        print("警告: 找不到 Inno Setup 編譯器")
        print("請先安裝 Inno Setup: https://jrsoftware.org/isinfo.php")
        print("或跳過此步驟，僅使用 exe 文件")
        return False
    
    # 確保輸出目錄存在
    os.makedirs("installer", exist_ok=True)
    
    # 運行 Inno Setup 編譯器
    success = run_command(
        f'"{iscc_path}" setup.iss',
        "使用 Inno Setup 編譯安裝程式"
    )
    
    if not success:
        return False
    
    # 檢查輸出文件
    installer_path = Path("installer/RelaxTime-Setup-0.1.0.exe")
    if installer_path.exists():
        file_size = installer_path.stat().st_size / (1024 * 1024)  # MB
        print(f"\n✓ 安裝程式構建成功: {installer_path} ({file_size:.2f} MB)")
        return True
    else:
        print("警告: 找不到安裝程式輸出文件")
        return False

def prepare_release():
    """準備發布文件"""
    print_step("步驟 3: 準備發布文件")
    
    release_dir = Path("release")
    release_dir.mkdir(exist_ok=True)
    
    files_to_copy = [
        ("dist/RelaxTime.exe", "RelaxTime.exe"),
        ("installer/RelaxTime-Setup-0.1.0.exe", "RelaxTime-Setup-0.1.0.exe"),
        ("README.md", "README.md"),
        ("RELEASE_NOTES.md", "RELEASE_NOTES.md"),
    ]
    
    copied_files = []
    for src, dst in files_to_copy:
        src_path = Path(src)
        if src_path.exists():
            dst_path = release_dir / dst
            shutil.copy2(src_path, dst_path)
            copied_files.append(dst)
            print(f"✓ 複製: {dst}")
        else:
            print(f"⚠ 跳過（不存在）: {src}")
    
    if copied_files:
        print(f"\n✓ 發布文件準備完成，位於: {release_dir.absolute()}")
        print("\n發布文件列表:")
        for f in copied_files:
            print(f"  - {f}")
        return True
    else:
        print("錯誤: 沒有找到任何發布文件")
        return False

def main():
    """主函數"""
    print("="*60)
    print(" Relax Time - 構建發布版本")
    print("="*60)
    
    # 步驟 1: 構建 exe
    if not build_exe():
        print("\n❌ exe 構建失敗，停止構建")
        sys.exit(1)
    
    # 步驟 2: 構建安裝程式（可選）
    installer_built = build_installer()
    if not installer_built:
        print("\n⚠ 安裝程式構建失敗或跳過，將只包含 exe 文件")
    
    # 步驟 3: 準備發布文件
    if not prepare_release():
        print("\n❌ 發布文件準備失敗")
        sys.exit(1)
    
    print("\n" + "="*60)
    print(" ✓ 構建完成！")
    print("="*60)
    print("\n下一步:")
    print("1. 檢查 release/ 目錄中的文件")
    print("2. 在 GitHub 創建新的 Release")
    print("3. 上傳 release/ 目錄中的文件")
    print("4. 使用 RELEASE_NOTES.md 作為 Release 說明")

if __name__ == "__main__":
    main()

