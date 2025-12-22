# Relax Time - 時間管理工具

一個 Windows 下的時間管理工具，幫助您管理工作時間和休息時間。

## 功能特色

- ⏱️ 可調整倒計時時間（以 5 分鐘為單位，預設 30 分鐘）
- 🎯 Start / Pause / Stop 時間控制
- 👁️ 時間到自動進入眼睛休息模式（5 分鐘）
- 🔄 休息結束後自動恢復工作時間
- 🔽 可隱藏到系統托盤（右下角）
- 📍 點擊托盤圖標可在螢幕中間顯示視窗
- 🪟 休息時自動最小化所有視窗

## 技術架構

- **語言**: Python 3.8+
- **GUI**: tkinter (標準庫)
- **系統托盤**: pystray
- **架構**: MVC (Model-View-Controller)
- **平台**: Windows

## 安裝

使用 uv 安裝依賴（會自動創建虛擬環境）：

```bash
uv sync
```

或者使用傳統方式：

```bash
uv pip install -r requirements.txt
```

## 執行

使用 uv 執行（推薦）：

```bash
uv run python main.py
```

或直接執行：

```bash
python main.py
```

使用 uv 隱藏啟動：

```bash
uv run python main.py --hidden
```

## 打包為 exe

使用 PyInstaller 打包為 Windows exe：

```bash
# 安裝 PyInstaller（如果還沒安裝）
uv sync

# 使用 spec 文件打包（推薦）
uv run pyinstaller pyinstaller.spec

# 或使用打包腳本
uv run python build_exe.py
```

打包後的 exe 文件會在 `dist/` 目錄中。

## 創建安裝程式

### 方式一：Inno Setup 安裝程式（推薦）

使用 Inno Setup 創建 exe 格式的安裝程式：

#### 1. 安裝 Inno Setup

下載並安裝 Inno Setup（免費）：
- 官方網站: https://jrsoftware.org/isinfo.php

#### 2. 構建安裝程式

```bash
# 方法 1: 使用自動化腳本（推薦）
uv run python build_installer.py

# 方法 2: 使用 Inno Setup Compiler GUI
# 打開 setup.iss 文件並編譯
```

安裝程式會生成在 `installer/RelaxTime-Setup-0.4.0.exe`

詳細說明請參考 [INSTALLER.md](INSTALLER.md)

## 新功能

### 循環模式
- 啟用循環模式後，休息時間結束會自動重新開始工作計時
- 可透過主視窗的「循環模式」選項開關控制

### 開機自動啟動
- 可在主視窗中勾選「開機自動啟動」選項
- 設定後會在 Windows 啟動時自動執行（隱藏模式）

### 鬧鐘圖標
- 視窗標題欄顯示鬧鐘圖標，更易識別

### 倒數18秒提示音
- 當計時器倒數到最後18秒時，自動播放美妙的提示音
- 幫助您提前準備，避免錯過休息時間

## 專案結構

```
relax-time/
├── main.py                 # 程式入口
├── models/                 # Model 層
│   ├── __init__.py
│   └── timer_model.py      # 時間狀態管理
├── views/                  # View 層
│   ├── __init__.py
│   ├── main_window.py      # 主視窗
│   └── tray_icon.py        # 系統托盤圖標
├── controllers/            # Controller 層
│   ├── __init__.py
│   └── timer_controller.py # 時間控制器
├── utils/                  # 工具類
│   ├── __init__.py
│   ├── window_manager.py   # 視窗管理工具
│   ├── startup_manager.py  # 開機啟動管理
│   └── icon_generator.py   # 圖標生成工具
├── resources/              # 資源文件
│   └── alarm_clock.ico     # 鬧鐘圖標
├── pyproject.toml          # 專案配置
├── pyinstaller.spec        # PyInstaller 打包配置
└── build_exe.py            # 打包腳本
```

