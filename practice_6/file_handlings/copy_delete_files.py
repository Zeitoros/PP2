import shutil
import os
from pathlib import Path


current_dir = Path(__file__).parent
original_file = current_dir / "sample.txt"
backup_file = current_dir / "sample_backup.txt"


if original_file.exists():
    shutil.copy(original_file, backup_file)
    print(f"Backup was created: {backup_file.name}")
else:
    print("There is no one file")
    
file_to_remove = current_dir / "temp_file.txt"
file_to_remove.touch()

print(f"Checking before removing: {file_to_remove.name} exists? {file_to_remove.exists()}")

if file_to_remove.exists():
    file_to_remove.unlink()
    print(f"File {file_to_remove.name} was removed")

print(f"Remained files: \n{os.listdir(current_dir)}")