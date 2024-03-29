; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Kiara"
#define MyAppVersion "1.0.3"
#define MyAppPublisher "Sobhan Bose"
#define MyAppExeName "Kiara.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{5F61A453-7A0F-4459-9E13-99FEA6881D0F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
OutputBaseFilename=mysetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "E:\Programs\Kiara Project\Kiara Project\EXE\exe.win-amd64-3.8\Kiara.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "E:\Programs\Kiara Project\Kiara Project\EXE\exe.win-amd64-3.8\Intro_Images\*"; DestDir: "{app}\Intro_Images"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "E:\Programs\Kiara Project\Kiara Project\EXE\exe.win-amd64-3.8\lib\*"; DestDir: "{app}\lib"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "E:\Programs\Kiara Project\Kiara Project\EXE\exe.win-amd64-3.8\Screens\*"; DestDir: "{app}\Screens"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "E:\Programs\Kiara Project\Kiara Project\EXE\exe.win-amd64-3.8\System_Files\*"; DestDir: "{app}\System_Files"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "E:\Programs\Kiara Project\Kiara Project\EXE\exe.win-amd64-3.8\python38.dll"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Dirs]
Name: "{app}\Notes"
Name: "{app}\Screenshots"

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

