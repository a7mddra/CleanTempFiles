import os
import shutil
import ctypes
import winshell  # Requires "winshell" module to handle Recycle Bin

# Paths to the folders
temp_folders = [
    os.getenv('TEMP'),  # Windows Temp folder
    os.getenv('USERPROFILE') + '\\AppData\\Local\\Temp',  # %temp% folder
    os.getenv('USERPROFILE') + '\\AppData\\Roaming\\Microsoft\\Windows\\Recent',  # Recent folder
    'C:\\Windows\\Prefetch',  # Prefetch folder
    'C:\\Windows\\SoftwareDistribution\\Download',  # Windows Update Cache
    'C:\\ProgramData\\Microsoft\\Windows\\WER',  # Windows Error Reporting
    os.getenv('USERPROFILE') + '\\AppData\\Local\\Microsoft\\Windows\\INetCache',  # Temporary Internet Files
    'C:\\Windows\\Temp',  # System Temp folder
    os.getenv('USERPROFILE') + '\\AppData\\Local\\Microsoft\\Windows\\Explorer',  # Thumbnails Cache
    os.getenv('USERPROFILE') + '\\AppData\\Local\\Microsoft\\DirectX Shader Cache',  # DirectX Shader Cache
    'C:\\ProgramData\\Microsoft\\Windows\\DeliveryOptimization',  # Delivery Optimization
    'C:\\Windows\\Logs',  # Windows Logs
    'C:\\Windows\\System32\\DriverStore\\FileRepository'  # Old Driver Store
]

# Function to delete files and folders permanently (Shift+Delete)
def delete_files_permanently(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Skipping file {file_path}: {e}")
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            try:
                shutil.rmtree(dir_path)
                print(f"Deleted folder: {dir_path}")
            except Exception as e:
                print(f"Skipping folder {dir_path}: {e}")

# Function to empty Recycle Bin
def empty_recycle_bin():
    try:
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
        print("Recycle Bin emptied successfully.")
    except Exception as e:
        print(f"Error emptying Recycle Bin: {e}")

# Check if running as admin (needed to access certain folders)
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == "__main__":
    if is_admin():
        for folder in temp_folders:
            if folder and os.path.exists(folder):
                print(f"Cleaning: {folder}")
                delete_files_permanently(folder)
            else:
                print(f"Folder not found or invalid: {folder}")
        
        # Empty the Recycle Bin after deleting files
        empty_recycle_bin()

    else:
        print("Please run this script as Administrator.")
