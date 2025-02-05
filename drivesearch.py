import os
import sys
import winreg

# Set the stdout encoding to UTF-8 to handle Unicode characters
sys.stdout.reconfigure(encoding='utf-8')

def get_installed_programs_from_registry():
    """
    Retrieves installed programs from the Windows Registry.
    """
    reg_keys = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]
    
    installed_programs = set()

    for reg_key in reg_keys:
        try:
            registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_key, 0, winreg.KEY_READ)
            for i in range(0, winreg.QueryInfoKey(registry_key)[0]):
                try:
                    subkey_name = winreg.EnumKey(registry_key, i)
                    subkey = winreg.OpenKey(registry_key, subkey_name)
                    
                    display_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                    if display_name:
                        installed_programs.add(display_name)
                except FileNotFoundError:
                    continue
                except OSError:
                    continue
            winreg.CloseKey(registry_key)
        except FileNotFoundError:
            continue
        except OSError:
            continue
    
    return installed_programs


def scan_common_install_directories():
    """
    Scans common installation directories for potential installed programs.
    """
    common_dirs = [
        r"C:\Program Files",
        r"C:\Program Files (x86)"
    ]

    installed_programs = set()

    for common_dir in common_dirs:
        if os.path.exists(common_dir):
            for folder in os.listdir(common_dir):
                installed_programs.add(folder)

    return installed_programs


def main():
    print("Searching for installed programs...")

    # Get programs from the Windows Registry
    registry_programs = get_installed_programs_from_registry()
    print("\nInstalled Programs from Registry:")
    for program in sorted(registry_programs):
        print(f" - {program}")

    # Scan common installation directories
    directory_programs = scan_common_install_directories()
    print("\nInstalled Programs from Common Directories:")
    for program in sorted(directory_programs):
        print(f" - {program}")


if __name__ == "__main__":
    main()