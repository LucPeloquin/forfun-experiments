Set objShell = CreateObject("Wscript.Shell")
' The second parameter "0" hides the window; "False" indicates the script does not wait for completion.
objShell.Run "powershell.exe -ExecutionPolicy Bypass -File ""C:\Users\lucpe\OneDrive\Desktop\scripts\resolutionswap.ps1""", 0, False
