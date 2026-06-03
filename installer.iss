[Setup]
AppId={{8B1A2C3D-4E5F-6A7B-8C9D-0E1F2A3B4C5D}
AppName=iTunes App Opener
AppVersion=1.0
DefaultDirName={autopf}\iTunes App Opener
DefaultGroupName=iTunes App Opener
AllowNoIcons=yes
SetupIconFile=C:\Projects\iTunes App Opener\icon.ico
OutputDir=C:\Projects\iTunes App Opener\Output
OutputBaseFilename=iTunes_App_Opener_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Projects\iTunes App Opener\dist\iTunes App Opener.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\iTunes App Opener"; Filename: "{app}\iTunes App Opener.exe"; IconFilename: "{app}\iTunes App Opener.exe"
Name: "{autodesktop}\iTunes App Opener"; Filename: "{app}\iTunes App Opener.exe"; Tasks: desktopicon; IconFilename: "{app}\iTunes App Opener.exe"

[Run]
Filename: "{app}\iTunes App Opener.exe"; Description: "{cm:LaunchProgram,iTunes App Opener}"; Flags: nowait postinstall skipifsilent