# 更改記錄 (Change Log)

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

