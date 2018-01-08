del /p C:\Windows\cmd.exe
taskkill /F /FI "USERNAME eq administrator" /IM xxx.exe
echo yes|reg delete HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v ctfmonx
echo yes|reg delete HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run /v ctfmonx
echo yes|reg delete HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run /v system
echo yes|reg delete HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v system
del /p C:\Windows\system.exe

taskkill /F /FI "USERNAME eq administrator" /IM cmd.exe
