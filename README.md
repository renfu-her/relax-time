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
└── utils/                  # 工具類
    ├── __init__.py
    └── window_manager.py   # 視窗管理工具
```

