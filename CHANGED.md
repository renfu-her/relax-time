# 更改記錄 (Change Log)

## 2025-12-22 14:39:05

### 版本更新
- 📦 **版本號升級至 0.4.0**
- 更新所有相關文件中的版本號引用（pyproject.toml, setup.iss, build_release.py, README.md, RELEASE.md, RELEASE_NOTES.md, GITHUB_RELEASE.md）

### 新增功能
- 🎬 **全螢幕倒數遮罩（多螢幕支援）**：在倒數計時剩下 5 秒時顯示全螢幕透明黑色遮罩
  - 支援多螢幕環境（Extend 模式），自動檢測所有顯示器
  - 為每個螢幕創建獨立的遮罩視窗，確保所有螢幕都被覆蓋
  - 主螢幕顯示大號倒數數字：5, 4, 3, 2, 1
  - 其他螢幕只顯示遮罩（不顯示數字）
  - 使用 Windows API (`EnumDisplayMonitors`) 檢測所有顯示器
  - 倒數完成後自動關閉遮罩並執行相應操作

### 功能調整
- 🚫 **移除休息時間的遮罩**：從休息返回工作時不再顯示倒數計時和遮罩
  - 休息時間結束後直接恢復視窗，無需等待倒數
  - 提供更流暢的用戶體驗

### 技術改進
- 更新 `views/countdown_overlay.py`：
  - 使用 `ctypes` 調用 Windows API 獲取所有顯示器信息
  - 支援為多個螢幕創建遮罩視窗
  - 改進視窗創建和顯示邏輯
- 更新 `models/timer_model.py`：移除休息時間倒數 5 秒的遮罩邏輯
- 更新 `controllers/timer_controller.py`：移除休息時間顯示遮罩的調用

## 2025-12-21 20:15:00

### 新增功能
- 🎬 **全螢幕倒數遮罩**：在倒數計時剩下 5 秒時顯示全螢幕透明黑色遮罩
- 遮罩上顯示倒數數字 5, 4, 3, 2, 1
- 倒數完成後自動關閉遮罩並執行相應操作（進入休息或恢復視窗）
- 支援工作時間和休息時間的倒數遮罩

### 技術改進
- 創建 `views/countdown_overlay.py`：全螢幕倒數遮罩視窗類
- 更新 `models/timer_model.py`：添加 `on_final_countdown` 回調和 `final_countdown_shown` 標記
- 更新 `controllers/timer_controller.py`：整合倒數遮罩邏輯
- 更新 `views/__init__.py`：導出 `CountdownOverlay` 類

## 2025-12-21 19:56:42

### 移除功能
- 🗑️ **移除 MSI 安裝程式支援**：由於 MSI 版本未提供，移除所有 MSI 相關文件和引用
- 刪除 `setup.wxs`、`build_msi.py`、`MSI_BUILD.md` 文件
- 從 `build_release.py` 中移除 MSI 構建相關代碼
- 從所有文檔（README.md、RELEASE.md）中移除 MSI 相關說明

## 2025-12-21 19:42:14

### 版本更新
- 📦 **版本號升級至 0.3.0**
- 更新所有相關文件中的版本號引用

## 2025-12-21 19:45:00

### UI 改進
- 📋 **設定視窗整合**：將「最小化到托盤」功能移到設定視窗中
- 🎨 **主視窗簡化**：移除主視窗中的「最小化到托盤」按鈕，所有設定統一在設定視窗管理

## 2025-12-21 16:50:00

### 新增功能
- ⚙️ **設定選單和設定視窗**：創建統一的設定界面
  - 在主視窗選單欄添加「設定」選單
  - 在主視窗添加「設定」按鈕
  - 創建獨立的設定視窗（`views/settings_window.py`）

### 功能改進
- 🔧 **休息時間設定**：可在設定視窗中調整休息時間（預設 5 分鐘，以 5 分鐘為單位）
- 📋 **設定項目整合**：將循環模式、開機自動啟動、休息時間設定整合到設定視窗
- 🎨 **UI 優化**：移除主視窗中的循環模式和開機啟動開關，簡化主界面

### 技術改進
- 創建 `views/settings_window.py`：設定視窗類，使用 Toplevel 創建模態對話框
- 更新 `models/timer_model.py`：添加 `set_rest_duration()` 和 `get_rest_duration()` 方法
- 更新 `controllers/timer_controller.py`：添加 `change_rest_duration()` 和 `show_settings()` 方法
- 更新 `views/main_window.py`：添加選單欄和設定按鈕，移除舊的設定 UI 元素
- 更新 `views/__init__.py`：導出 SettingsWindow 類

### 使用說明
- 點擊主視窗選單欄的「設定」或主視窗中的「設定」按鈕打開設定視窗
- 在設定視窗中可以調整：循環模式、開機自動啟動、休息時間（以 5 分鐘為單位）

## 2025-12-21 16:37:37

### 版本更新
- 📦 **版本號升級至 0.3.0**
- 更新所有相關文件中的版本號引用

## 2025-12-21 19:50:00

### 功能調整
- ⏰ **倒數提示音時間調整**：將倒數提示音從最後10秒改為最後18秒
- 更新所有相關文檔和代碼註釋

## 2025-12-21 16:34:33

### 新增功能
- 🔊 **倒數18秒提示音**：在計時器倒數最後18秒時播放美妙的提示音

### 技術改進
- 創建 `utils/audio_player.py`：音頻播放工具類，使用 pyglet 播放 MP3
- 添加音頻資源：`resources/countdown_alarm.mp3`（倒數提示音）
- 更新 `models/timer_model.py`：添加倒數18秒警告回調和播放狀態追蹤
- 更新 `controllers/timer_controller.py`：實現倒數18秒音頻播放
- 更新 `pyproject.toml`：添加 pyglet 依賴
- 更新 `pyinstaller.spec`：添加 pyglet 隱藏導入
- 更新 `setup.iss` 和 `setup.wxs`：包含音頻文件到安裝程式
- 更新 `README.md`：添加倒數18秒提示音功能說明

### 功能說明
- 當計時器倒數到最後18秒時，自動播放提示音
- 每個計時週期只播放一次（防止重複播放）
- 音頻在獨立線程中播放，不會阻塞 UI
- 支援打包後和開發環境的音頻文件路徑
- 使用 pyglet 庫，輕量且跨平台

## 2025-12-21 20:00:00

### 移除功能
- 🗑️ **移除 MSI 安裝程式支援**：由於 MSI 版本未提供，移除所有 MSI 相關文件和引用
- 刪除 `setup.wxs`、`build_msi.py`、`MSI_BUILD.md` 文件
- 從所有文檔中移除 MSI 相關說明

## 2025-12-21 15:40:00

### 歷史記錄（已移除）
- 📦 **MSI 安裝程式支援**：此功能已移除（v0.3.0）

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

