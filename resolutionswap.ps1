# ============================================================
# This script monitors for valorant.exe and automatically
# sets the display resolution to 1280×882 when it is running.
# When Valorant is not running, it resets the resolution to
# the fallback value (default: 1920×1080).
# ============================================================

# ---------------------------
# Define target and fallback resolutions
# ---------------------------
$TargetResolution = [PSCustomObject]@{ Width = 1280; Height = 882 }
$FallbackResolution = [PSCustomObject]@{ Width = 1920; Height = 1080 }

# ---------------------------
# Add the necessary .NET type for display settings change via P/Invoke
# ---------------------------
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class DisplaySettings {
    public const int CDS_UPDATEREGISTRY = 0x01;
    public const int DISP_CHANGE_SUCCESSFUL = 0;
    public const int DM_PELSWIDTH = 0x80000;
    public const int DM_PELSHEIGHT = 0x100000;

    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi)]
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
        public int dmNup;
        public int dmDisplayFrequency;
    }

    [DllImport("user32.dll", CharSet = CharSet.Ansi)]
    public static extern int ChangeDisplaySettings(ref DEVMODE devMode, int flags);
}
"@

# ---------------------------
# Function: Set-DisplayResolution
# Changes the display resolution to the specified width and height.
# ---------------------------
function Set-DisplayResolution {
    param (
        [Parameter(Mandatory=$true)]
        [int]$Width,
        [Parameter(Mandatory=$true)]
        [int]$Height
    )

    # Retrieve the primary screen resolution
    Add-Type -AssemblyName System.Windows.Forms
    $currentScreen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds

    # Create a new DEVMODE structure instance
    $devMode = New-Object DisplaySettings+DEVMODE
    $devMode.dmDeviceName = New-Object -TypeName System.String("DISPLAY")
    $devMode.dmSize = [System.Runtime.InteropServices.Marshal]::SizeOf($devMode)
    $devMode.dmFields = [DisplaySettings]::DM_PELSWIDTH -bor [DisplaySettings]::DM_PELSHEIGHT

    # Set the desired resolution values
    $devMode.dmPelsWidth = $Width
    $devMode.dmPelsHeight = $Height

    # Attempt to change the display settings
    $result = [DisplaySettings]::ChangeDisplaySettings([ref]$devMode, [DisplaySettings]::CDS_UPDATEREGISTRY)

    if ($result -eq [DisplaySettings]::DISP_CHANGE_SUCCESSFUL) {
        Write-Output "Resolution successfully changed to $Width x $Height."
    }
    else {
        Write-Output "Failed to change resolution to $Width x $Height. Error code: $result"
    }
}

# ---------------------------
# Function: Get-CurrentResolution
# Retrieves the current resolution of the primary monitor.
# ---------------------------
function Get-CurrentResolution {
    Add-Type -AssemblyName System.Windows.Forms
    $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    return [PSCustomObject]@{
        Width  = $bounds.Width
        Height = $bounds.Height
    }
}

# ---------------------------
# Main Monitoring Loop
# ---------------------------
Write-Output "Starting Valorant resolution monitor..."
while ($true) {
    # Check if Valorant is running
    $valorantProcess = Get-Process -Name "valorant" -ErrorAction SilentlyContinue

    # Get current screen resolution
    $currentRes = Get-CurrentResolution

    if ($valorantProcess) {
        # If Valorant is running and the current resolution is not the target, change it.
        if (($currentRes.Width -ne $TargetResolution.Width) -or ($currentRes.Height -ne $TargetResolution.Height)) {
            Write-Output "Valorant detected. Changing resolution to $($TargetResolution.Width)x$($TargetResolution.Height)..."
            Set-DisplayResolution -Width $TargetResolution.Width -Height $TargetResolution.Height
        }
    }
    else {
        # If Valorant is not running and the current resolution is not the fallback, revert it.
        if (($currentRes.Width -ne $FallbackResolution.Width) -or ($currentRes.Height -ne $FallbackResolution.Height)) {
            Write-Output "Valorant is not running. Reverting resolution to $($FallbackResolution.Width)x$($FallbackResolution.Height)..."
            Set-DisplayResolution -Width $FallbackResolution.Width -Height $FallbackResolution.Height
        }
    }

    # Check every 5 seconds (adjust the sleep time if desired)
    Start-Sleep -Seconds 5
}
