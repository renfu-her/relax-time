# MSI 安裝程式構建指南

本指南說明如何使用 WiX Toolset 創建 MSI 格式的 Windows 安裝程式。

## 什麼是 MSI？

MSI (Microsoft Installer) 是 Windows 的原生安裝格式，具有以下優點：

- ✅ Windows 標準格式，系統原生支援
- ✅ 支援靜默安裝：`msiexec /i RelaxTime-Setup.msi /quiet`
- ✅ 更好的 Windows 整合（控制面板、更新機制等）
- ✅ 企業環境友好
- ✅ 支援修補和升級

## 前置要求

### 1. 構建 exe 文件

首先需要將 Python 程式打包為 exe：

```bash
uv run pyinstaller pyinstaller.spec
```

這會生成 `dist/RelaxTime.exe` 文件。

### 2. 安裝 WiX Toolset

WiX Toolset 是微軟官方推薦的免費開源工具，用於創建 MSI 安裝程式。

#### 下載安裝

1. **訪問官方網站**：https://wixtoolset.org/
2. **下載最新版本**：https://wixtoolset.org/releases/
3. **執行安裝程式**並完成安裝

#### 驗證安裝

安裝完成後，驗證 WiX 是否正確安裝：

```bash
candle -?
light -?
```

如果命令不存在，需要將 WiX 的 `bin` 目錄添加到系統 PATH：

- 預設安裝路徑：`C:\Program Files (x86)\WiX Toolset v3.14\bin\`
- 或設置環境變量 `WIX` 指向 WiX 安裝目錄

## 構建 MSI

### 方法 1: 使用自動化腳本（推薦）

```bash
uv run python build_msi.py
```

腳本會自動：
- 檢查 exe 文件是否存在
- 查找 WiX Toolset 編譯器
- 編譯 WXS 文件
- 鏈接生成 MSI 文件

### 方法 2: 手動構建

#### 步驟 1: 編譯 WXS 文件

```bash
candle setup.wxs -out installer\setup.wixobj
```

#### 步驟 2: 鏈接生成 MSI

```bash
light installer\setup.wixobj -out installer\RelaxTime-Setup-0.2.0.msi -ext WixUIExtension
```

## MSI 安裝程式功能

生成的 MSI 安裝程式包含以下功能：

- ✅ 標準 Windows 安裝介面
- ✅ 安裝到用戶目錄（`%LOCALAPPDATA%\Relax Time`）
- ✅ 開始菜單快捷方式
- ✅ 桌面快捷方式（可選）
- ✅ 控制面板中的卸載入口
- ✅ 產品圖標
- ✅ 支援升級和降級處理

## 自定義 MSI

可以編輯 `setup.wxs` 文件來自定義：

- 安裝目錄位置
- 快捷方式設定
- 功能選項
- 安裝條件
- 自定義操作
- 等等

詳細文檔請參考 WiX Toolset 官方文檔：https://wixtoolset.org/documentation/

## MSI vs Inno Setup

| 特性 | MSI (WiX) | Inno Setup |
|------|-----------|------------|
| 格式 | Windows 標準格式 | 自定義格式 |
| 靜默安裝 | ✅ 原生支援 | ⚠️ 需要參數 |
| 企業部署 | ✅ 友好 | ⚠️ 較難 |
| 學習曲線 | 較陡 | 較平緩 |
| 文件大小 | 較小 | 較大 |
| 安裝速度 | 較快 | 較慢 |
| 控制面板整合 | ✅ 完整 | ⚠️ 部分 |

**建議：**
- 企業環境或需要靜默安裝：使用 MSI
- 個人用戶或簡單部署：使用 Inno Setup

## 測試 MSI

### 正常安裝

1. 雙擊 `RelaxTime-Setup-0.2.0.msi`
2. 按照安裝嚮導完成安裝
3. 驗證程式是否正常運行

### 靜默安裝

```bash
# 靜默安裝
msiexec /i RelaxTime-Setup-0.2.0.msi /quiet

# 靜默安裝（不顯示進度）
msiexec /i RelaxTime-Setup-0.2.0.msi /quiet /norestart

# 靜默卸載
msiexec /x RelaxTime-Setup-0.2.0.msi /quiet
```

### 日誌安裝（調試用）

```bash
msiexec /i RelaxTime-Setup-0.2.0.msi /l*v install.log
```

## 常見問題

### Q: 找不到 candle.exe 或 light.exe？

A: 確保 WiX Toolset 已正確安裝，並將 bin 目錄添加到 PATH，或設置 WIX 環境變量。

### Q: 編譯時出現錯誤？

A: 檢查 `setup.wxs` 文件中的路徑是否正確，確保 `dist/RelaxTime.exe` 和 `resources/alarm_clock.ico` 存在。

### Q: MSI 文件無法執行？

A: 檢查是否以管理員權限運行，或檢查 MSI 文件的數字簽名（如果需要）。

### Q: 如何修改安裝目錄？

A: 編輯 `setup.wxs` 文件，修改 `Directory` 元素的設置。例如改為 Program Files：

```xml
<Directory Id="ProgramFilesFolder">
  <Directory Id="INSTALLFOLDER" Name="Relax Time">
    ...
  </Directory>
</Directory>
```

## 進階功能

### 添加開機啟動選項

可以在 `setup.wxs` 中添加註冊表項來實現開機啟動：

```xml
<Component Id="StartupRegistry" Guid="...">
  <RegistryValue Root="HKCU" 
                Key="Software\Microsoft\Windows\CurrentVersion\Run" 
                Name="RelaxTime" 
                Type="string" 
                Value="[INSTALLFOLDER]RelaxTime.exe --hidden" 
                KeyPath="yes" />
</Component>
```

### 添加許可證文件

```xml
<WixVariable Id="WixUILicenseRtf" Value="license.rtf" />
```

詳細說明請參考 WiX Toolset 官方文檔。

