# Inno Setup 繁體中文語言文件安裝指南

## 問題說明

如果編譯 `setup.iss` 時出現錯誤，提示找不到 `ChineseTraditional.isl` 文件，這是因為 Inno Setup 預設不包含繁體中文語言文件。

## 解決方法

### 方法 1: 下載並安裝語言文件（推薦）

1. **下載繁體中文語言文件**
   - 訪問 Inno Setup 官方翻譯頁面：https://jrsoftware.org/files/istrans/
   - 找到並下載 `ChineseTraditional.isl` 文件

2. **安裝語言文件**
   - 將下載的 `ChineseTraditional.isl` 文件複製到 Inno Setup 的 `Languages` 目錄
   - 通常路徑為：
     - `C:\Program Files (x86)\Inno Setup 6\Languages\`
     - 或 `C:\Program Files\Inno Setup 6\Languages\`

3. **驗證安裝**
   - 重新打開 Inno Setup Compiler
   - 打開 `setup.iss` 文件
   - 應該可以正常編譯，不會再出現找不到文件的錯誤

### 方法 2: 僅使用英文（簡單方案）

如果不需要繁體中文介面，可以修改 `setup.iss` 文件：

```ini
[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
```

移除繁體中文的配置行即可。

### 方法 3: 使用自定義語言文件

也可以將語言文件放在專案目錄中：

1. 創建 `languages` 目錄
2. 將 `ChineseTraditional.isl` 放在其中
3. 修改 `setup.iss`：

```ini
[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "chinesetraditional"; MessagesFile: "languages\ChineseTraditional.isl"
```

## 語言文件編碼注意事項

- 確保語言文件使用 **UTF-8 with BOM** 編碼
- 如果顯示亂碼，請檢查文件編碼格式

## 測試

編譯安裝程式後，執行生成的安裝程式，應該會根據系統語言自動選擇繁體中文或英文介面。

