# GitHub Release 創建指南

本指南將幫助您在 GitHub 上創建 Relax Time 的發布版本。

## 前置步驟

### 1. 構建發布文件

運行構建腳本：

```bash
uv run python build_release.py
```

這會自動：
- 構建 exe 文件
- 構建安裝程式（如果已安裝 Inno Setup）
- 將所有發布文件複製到 `release/` 目錄

### 2. 檢查發布文件

確保 `release/` 目錄包含：
- `RelaxTime.exe` - 可執行文件
- `RelaxTime-Setup-0.2.0.exe` - 安裝程式（如果已構建）
- `README.md` - 說明文檔
- `RELEASE_NOTES.md` - 發布說明

## 在 GitHub 創建 Release

### 步驟 1: 創建 Tag

```bash
# 創建並推送 tag
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0
```

或者使用 GitHub Web 界面：
- 前往 Releases 頁面
- 點擊 "Create a new release"
- 在 "Choose a tag" 中輸入 `v0.2.0`
- 選擇 "Create new tag: v0.2.0 on publish"

### 步驟 2: 填寫 Release 信息

**Release title（標題）：**
```
Relax Time v0.2.0
```

**Release notes（說明）：**

可以使用 `RELEASE_NOTES.md` 的內容，或者使用以下精簡版本：

```markdown
## 🎉 首次發布

Relax Time 是一個專為 Windows 設計的時間管理工具，幫助您管理工作時間和休息時間。

## ✨ 主要功能

- ⏱️ 智能計時器（可調整時間，預設 30 分鐘）
- 👁️ 自動眼睛休息模式（5 分鐘）
- 🔄 循環模式（自動重新開始）
- 🔽 系統托盤整合
- 🚀 開機自動啟動
- 🎨 現代化界面設計

## 📦 下載

### 推薦：安裝程式
下載 `RelaxTime-Setup-0.2.0.exe` 並執行安裝

### 便攜版
下載 `RelaxTime.exe` 直接執行（無需安裝）

## 🚀 快速開始

1. 設定工作時間（預設 30 分鐘）
2. 點擊「開始」按鈕
3. 時間到後自動進入休息模式
4. 可啟用循環模式自動繼續工作

## 📋 系統要求

- Windows 7 或更高版本
- 無需安裝 Python 或其他依賴

---

**完整文檔：** 請參考 README.md
```

### 步驟 3: 上傳文件

在 "Attach binaries" 區域：

1. 上傳 `RelaxTime-Setup-0.2.0.exe`（安裝程式）- **推薦**
2. 上傳 `RelaxTime.exe`（可執行文件）- 便攜版

**建議：**
- 將安裝程式作為主要下載選項
- 將 exe 文件作為 "Portable version" 或 "免安裝版" 標註

### 步驟 4: 發布

- 如果這是正式版本，點擊 "Publish release"
- 如果是預發布版本（測試用），勾選 "Set as a pre-release" 然後發布

## Release 後續步驟

1. **更新文檔**（可選）
   - 更新 README.md 中的下載鏈接
   - 更新版本號

2. **宣傳**（可選）
   - 在相關社群分享
   - 更新專案描述

3. **監控**
   - 關注 Issues 和反饋
   - 收集用戶意見用於下一版本

## 版本號規範

建議使用 [Semantic Versioning](https://semver.org/)：

- `主版本號.次版本號.修訂號`
- 例如：`0.2.0`, `0.3.0`, `1.0.0`

## 常見問題

### Q: 如果安裝程式構建失敗怎麼辦？
A: 可以只上傳 `RelaxTime.exe`，用戶可以直接執行無需安裝。

### Q: 如何更新 Release？
A: GitHub 不支援直接更新 Release，需要創建新的 Release 版本。

### Q: 可以在 Release 中包含源代碼嗎？
A: 通常不需要，因為源代碼已經在 GitHub 倉庫中。如果需要，可以上傳源代碼 zip 文件。

