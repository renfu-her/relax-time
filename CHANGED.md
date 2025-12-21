# 更改記錄 (Change Log)

## 2025-12-21 16:37:37

### 版本更新
- 📦 **版本號升級至 0.2.0**
- 更新所有相關文件中的版本號引用

## 2025-12-21 16:34:33

### 新增功能
- 🔊 **倒數10秒提示音**：在計時器倒數最後10秒時播放美妙的提示音

### 技術改進
- 創建 `utils/audio_player.py`：音頻播放工具類，使用 pyglet 播放 MP3
- 添加音頻資源：`resources/countdown_alarm.mp3`（倒數提示音）
- 更新 `models/timer_model.py`：添加倒數10秒警告回調和播放狀態追蹤
- 更新 `controllers/timer_controller.py`：實現倒數10秒音頻播放
- 更新 `pyproject.toml`：添加 pyglet 依賴
- 更新 `pyinstaller.spec`：添加 pyglet 隱藏導入
- 更新 `setup.iss` 和 `setup.wxs`：包含音頻文件到安裝程式
- 更新 `README.md`：添加倒數10秒提示音功能說明

### 功能說明
- 當計時器倒數到最後10秒時，自動播放提示音
- 每個計時週期只播放一次（防止重複播放）
- 音頻在獨立線程中播放，不會阻塞 UI
- 支援打包後和開發環境的音頻文件路徑
- 使用 pyglet 庫，輕量且跨平台

## 2025-12-21 15:40:00

### 新增功能
- 📦 **MSI 安裝程式支援**：添加 WiX Toolset 配置，可創建 MSI 格式的 Windows 安裝程式

### 技術改進
- 創建 `setup.wxs`：WiX Toolset MSI 安裝腳本配置文件
- 創建 `build_msi.py`：自動化構建 MSI 安裝程式的腳本
- 創建 `MSI_BUILD.md`：MSI 安裝程式構建指南
- 更新 `build_release.py`：添加 MSI 構建支援
- 更新 `README.md`：添加 MSI 安裝程式說明

### MSI 安裝程式優點
- Windows 標準格式
- 支援靜默安裝（`msiexec /i file.msi /quiet`）
- 更好的企業環境支援
- 控制面板整合
- 支援升級和修補

## 2025-12-21 15:35:56

### 新增功能
- 📦 **發布構建工具**：添加自動化構建和發布腳本

### 技術改進
- 創建 `build_release.py`：自動化構建發布版本的腳本（包含 exe 和安裝程式）
- 創建 `RELEASE_NOTES.md`：發布說明文檔模板
- 創建 `RELEASE.md`：GitHub Release 創建指南
- 更新 `.gitignore`：添加 release 目錄（可選）

## 2025-12-21 15:15:00

### 新增功能
- 📦 **Windows 安裝程式支援**：添加 Inno Setup 配置，可創建專業的 Windows 安裝程式

### 技術改進
- 創建 `setup.iss`：Inno Setup 安裝腳本配置文件
- 創建 `build_installer.py`：自動化構建安裝程式的腳本
- 創建 `INSTALLER.md`：安裝程式構建指南文檔
- 更新 `README.md`：添加安裝程式構建說明

### 安裝程式功能
- 標準 Windows 安裝介面
- 選擇安裝目錄
- 桌面快捷方式（可選）
- 開始菜單快捷方式
- 開機自動啟動選項（可選）
- 繁體中文和英文介面支援
- 完整的卸載功能

## 2025-12-21 15:09:53

### 新增功能
- 🎨 **鬧鐘圖標**：視窗標題欄顯示鬧鐘圖標（`resources/alarm_clock.ico`）
- 🔄 **循環模式開關**：新增循環模式選項，啟用後休息結束自動重新開始計時
- 🚀 **開機自動啟動**：新增開機啟動選項，可設定 Windows 啟動時自動執行
- 📦 **打包支援**：添加 PyInstaller 配置，可打包為 Windows exe 文件

### 技術改進
- 創建 `utils/icon_generator.py`：自動生成鬧鐘圖標（多尺寸 ICO 格式）
- 創建 `utils/startup_manager.py`：Windows 註冊表開機啟動管理
- 更新 `views/main_window.py`：添加圖標設置、循環模式開關、開機啟動開關
- 更新 `models/timer_model.py`：添加 `loop_mode` 屬性和相關方法
- 更新 `controllers/timer_controller.py`：實現循環模式邏輯和開機啟動管理
- 創建 `pyinstaller.spec`：PyInstaller 打包配置文件
- 創建 `build_exe.py`：打包腳本
- 更新 `pyproject.toml`：添加 pyinstaller 依賴

### 使用說明
- 打包為 exe: `uv run pyinstaller pyinstaller.spec`
- 開機啟動通過 Windows 註冊表實現（HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run）
- 圖標在打包時自動包含在 exe 中

## 2025-12-21 12:04:35

### 依賴管理更新
- 改用 uv 作為包管理器
- 創建 `pyproject.toml` 文件，使用標準 Python 項目配置格式
- 更新 `README.md` 中的安裝說明，添加 `uv sync` 和 `uv run` 的使用說明
- 依賴項：pystray>=0.19.5, Pillow>=10.0.0
- 虛擬環境自動創建在 `.venv` 目錄

## 2025-12-21 12:02:50

### 新增功能
- 創建 Relax Time 時間管理工具專案
- 實現 MVC 架構設計
  - Model 層 (`models/timer_model.py`): 時間狀態管理和計時邏輯
  - View 層 (`views/main_window.py`, `views/tray_icon.py`): 主視窗和系統托盤圖標
  - Controller 層 (`controllers/timer_controller.py`): 業務邏輯控制

### 核心功能
- ⏱️ 可調整倒計時時間（以 5 分鐘為單位，預設 30 分鐘）
- 🎯 Start / Pause / Stop 時間控制
- 👁️ 時間到自動進入眼睛休息模式（5 分鐘）
- 🔄 休息結束後自動恢復工作時間
- 🔽 可隱藏到系統托盤（右下角）
- 📍 點擊托盤圖標可在螢幕中間顯示視窗
- 🪟 休息時自動最小化所有視窗（使用 Win+M 快捷鍵）

### 技術實現
- 使用 tkinter 作為 GUI 框架（Python 標準庫）
- 使用 pystray 實現系統托盤功能
- 使用 ctypes 調用 Windows API 實現視窗最小化功能
- 多線程設計：計時器在獨立線程中運行，不阻塞 UI

### 專案結構
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
│   └── window_manager.py   # 視窗管理工具（最小化所有視窗）
├── requirements.txt        # 依賴套件
├── README.md              # 專案說明
└── CHANGED.md             # 更改記錄
```

### 依賴套件
- pystray >= 0.19.5
- Pillow >= 10.0.0

### 使用說明
- 執行: `python main.py`
- 隱藏啟動: `python main.py --hidden` 或 `python main.py -h`
- 右鍵點擊托盤圖標可顯示視窗或退出程式

