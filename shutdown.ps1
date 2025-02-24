# Import the required assembly for screen settings
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

public class ScreenSettings {
    [DllImport("user32.dll")]
    public static extern int EnumDisplaySettings(string deviceName, int modeNum, ref DEVMODE devMode);
    
    [DllImport("user32.dll")]
    public static extern int ChangeDisplaySettings(ref DEVMODE devMode, int flags);

    [StructLayout(LayoutKind.Sequential)]
    public struct DEVMODE {
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
        public string dmDeviceName;
        public short dmSpecVersion;
        public short dmDriverVersion;
        public short dmSize;
        public short dmDriverExtra;
        public int dmFields;
        public int dmPositionX;
        public int dmPositionY;
        public int dmDisplayOrientation;
        public int dmDisplayFixedOutput;
        public short dmColor;
        public short dmDuplex;
        public short dmYResolution;
        public short dmTTOption;
        public short dmCollate;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
        public string dmFormName;
        public short dmLogPixels;
        public int dmBitsPerPel;
        public int dmPelsWidth;
        public int dmPelsHeight;
        public int dmDisplayFlags;
        public int dmDisplayFrequency;
        public int dmICMMethod;
        public int dmICMIntent;
        public int dmMediaType;
        public int dmDitherType;
        public int dmReserved1;
        public int dmReserved2;
        public int dmPanningWidth;
        public int dmPanningHeight;
    }
}
"@

# Create DEVMODE structure
$mode = New-Object ScreenSettings+DEVMODE
$mode.dmSize = [System.Runtime.InteropServices.Marshal]::SizeOf($mode)

# Get current display settings
[ScreenSettings]::EnumDisplaySettings($null, -1, [ref]$mode)

# Set refresh rate to 240Hz
$mode.dmDisplayFrequency = 240

# Apply the new settings
$result = [ScreenSettings]::ChangeDisplaySettings([ref]$mode, 0)

if ($result -eq 0) {
    Write-Host "Successfully changed refresh rate to 240Hz"
    # Wait 5 seconds before shutdown
    Start-Sleep -Seconds 5
    # Shutdown the computer
    Stop-Computer -Force
} else {
    Write-Host "Failed to change refresh rate. Your monitor may not support 240Hz"
}
