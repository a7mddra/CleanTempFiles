import os
import shutil
import ctypes

temp_folders = [
    os.getenv('TEMP'),
    os.path.join(os.getenv('USERPROFILE'), 'AppData\\Local\\Temp'),
    os.path.join(os.getenv('USERPROFILE'), 'AppData\\Roaming\\Microsoft\\Windows\\Recent'),
    'C:\\Windows\\Prefetch',
    'C:\\Windows\\SoftwareDistribution\\Download',
    'C:\\ProgramData\\Microsoft\\Windows\\WER',
    os.path.join(os.getenv('USERPROFILE'), 'AppData\\Local\\Microsoft\\Windows\\INetCache'),
    'C:\\Windows\\Temp',
    os.path.join(os.getenv('USERPROFILE'), 'AppData\\Local\\Microsoft\\Windows\\Explorer'),
    os.path.join(os.getenv('USERPROFILE'), 'AppData\\Local\\Microsoft\\DirectX Shader Cache'),
    'C:\\ProgramData\\Microsoft\\Windows\\DeliveryOptimization',
    'C:\\Windows\\Logs',
    'C:\\Windows\\System32\\DriverStore\\FileRepository'
]

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

def empty_recycle_bin():
    try:
        # Use ctypes to empty the recycle bin
        ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0x00000001)
        print("Recycle Bin emptied successfully.")
    except Exception as e:
        print(f"Error emptying Recycle Bin: {e}")

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
        
        empty_recycle_bin()
    else:
        print("Please run this script as Administrator.")
