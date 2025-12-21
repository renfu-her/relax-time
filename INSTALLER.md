# 構建安裝程式指南

本專案支援創建 Windows 安裝程式（.exe installer），讓用戶可以像安裝其他 Windows 軟體一樣安裝 Relax Time。

## 前置要求

### 1. 構建 exe 文件

首先需要將 Python 程式打包為 exe：

```bash
uv run pyinstaller pyinstaller.spec
```

這會生成 `dist/RelaxTime.exe` 文件。

### 2. 安裝 Inno Setup

下載並安裝 Inno Setup（免費開源）：

- 官方網站: https://jrsoftware.org/isinfo.php
- 下載頁面: https://jrsoftware.org/isdl.php

安裝時建議選擇完整安裝，包含所有組件。

## 構建安裝程式

### 方法 1: 使用自動化腳本（推薦）

```bash
uv run python build_installer.py
```

腳本會自動：
- 檢查 exe 文件是否存在
- 查找 Inno Setup 編譯器
- 編譯安裝腳本
- 生成安裝程式

### 方法 2: 使用 Inno Setup 編譯器（GUI）

1. 打開 Inno Setup Compiler
2. 點擊 "File" → "Open"
3. 選擇專案根目錄下的 `setup.iss` 文件
4. 點擊 "Build" → "Compile"（或按 F9）
5. 編譯完成後，安裝程式會在 `installer/` 目錄中

## 安裝程式功能

生成的安裝程式包含以下功能：

- ✅ 標準 Windows 安裝介面
- ✅ 選擇安裝目錄
- ✅ 建立桌面快捷方式（可選）
- ✅ 建立開始菜單快捷方式
- ✅ 開機自動啟動選項（可選）
- ✅ 支援繁體中文和英文介面
- ✅ 卸載功能
- ✅ 顯示應用程式圖標

## 輸出文件

編譯成功後，安裝程式會生成在：

```
installer/RelaxTime-Setup-0.1.0.exe
```

## 自定義安裝程式

可以編輯 `setup.iss` 文件來自定義：

- 應用程式名稱和版本
- 安裝目錄
- 快捷方式設定
- 安裝選項
- 許可證文件
- 安裝前/後資訊
- 等等

詳細文檔請參考 Inno Setup 官方文檔：https://jrsoftware.org/ishelp/

## 測試安裝程式

1. 運行生成的安裝程式
2. 按照安裝嚮導完成安裝
3. 測試應用程式是否正常運行
4. 測試卸載功能

## 分發

生成的安裝程式可以：

- 直接分發給用戶
- 上傳到軟體下載網站
- 放置在 GitHub Releases 中
- 通過其他方式分發

用戶只需雙擊安裝程式即可完成安裝，無需手動配置。

