; Inno Setup 安裝腳本
; 需要先安裝 Inno Setup: https://jrsoftware.org/isinfo.php

#define MyAppName "Relax Time"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "Relax Time Team"
#define MyAppURL "https://github.com/yourusername/relax-time"
#define MyAppExeName "RelaxTime.exe"
#define MyAppDescription "Windows 時間管理工具 - 幫助您管理工作時間和休息時間"

[Setup]
; 注意: AppId 的值用於標識此應用程式
; 請勿在其他安裝程式中使用相同的 AppId 值
AppId={{A1B2C3D4-E5F6-4A5B-8C9D-0E1F2A3B4C5D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
; 卸載資訊
UninstallDisplayIcon={app}\{#MyAppExeName}
; 壓縮設定
Compression=lzma
SolidCompression=yes
WizardStyle=modern
; 輸出設定
OutputDir=installer
OutputBaseFilename=RelaxTime-Setup-{#MyAppVersion}
SetupIconFile=resources\alarm_clock.ico
; 許可證和資訊
LicenseFile=
InfoBeforeFile=
InfoAfterFile=
; 管理員權限（如需要）
PrivilegesRequired=lowest
; 語言
LanguageDetectionMethod=locale

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
; 繁體中文語言文件（需要下載 ChineseTraditional.isl 到 Inno Setup 的 Languages 目錄）
; 下載地址: https://jrsoftware.org/files/istrans/
Name: "chinesetraditional"; MessagesFile: "compiler:Languages\ChineseTraditional.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode
Name: "startup"; Description: "開機自動啟動"; GroupDescription: "選項"; Flags: unchecked

[Files]
; 主程式文件
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
; 資源文件（如果需要）
Source: "resources\alarm_clock.ico"; DestDir: "{app}\resources"; Flags: ignoreversion
; 注意: 不要在任何共享系統文件上使用 "Flags: ignoreversion"

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\resources\alarm_clock.ico"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{app}\resources\alarm_clock.ico"
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon; IconFilename: "{app}\resources\alarm_clock.ico"

[Run]
; 安裝後運行程式選項
Filename: "{app}\{#MyAppExeName}"; Description: "啟動 {#MyAppName}"; Flags: nowait postinstall skipifsilent unchecked

[Registry]
; 開機自動啟動（如果用戶選擇了該任務）
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "RelaxTime"; ValueData: """{app}\{#MyAppExeName}"" --hidden"; Tasks: startup; Flags: uninsdeletevalue

[Code]
// 自定義函數：檢查是否已安裝
function InitializeSetup(): Boolean;
begin
  Result := True;
end;

// 自定義函數：卸載時清理
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usUninstall then
  begin
    // 可以在這裡添加清理邏輯，例如刪除註冊表項
  end;
end;

