taskkill /F /FI "USERNAME eq administrator" /IM client.exe
taskkill /F /FI "USERNAME eq administrator" /IM cmds.exe
echo yes|reg delete HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v RssWps
echo yes|reg delete HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v RssWps
echo yes|reg delete HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v Wps
echo yes|reg delete HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v Wps
del /Q /a:hs C:\Windows\cmds.exe

