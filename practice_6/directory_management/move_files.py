from math import log
import shutil
from pathlib import Path

current_dir = Path(__file__).parent

source_file = current_dir / "my_folder" / "data" / "logs" / "app.log"

backup_dir = current_dir / "backups"
backup_dir.mkdir(exist_ok=True)


if source_file.exists():
    copy_dest = backup_dir / "app_backup.log"
    shutil.copy(source_file, copy_dest)
    print(f"File copied in: {copy_dest.relative_to(current_dir)}")
    
    move_dest = backup_dir / "app_moved.log"
    source_file.replace(move_dest)
    print(f"File was moved in: {move_dest.relative_to(current_dir)}")
    
    error_file = current_dir / "my_folder" / "data" / "logs" / "error.txt"
    if error_file.exists():
        error_file.unlink()
        
    logs_dir = current_dir / "my_folder" / "data" / "logs"
    if logs_dir.exists():
        logs_dir.rmdir()
        print(f"Empty folder {logs_dir.name} was deleted")

else:
    print(f"Initial file does not find")

print("\nCurrent content of folder backups:")
for i in backup_dir.iterdir():
    print(f" - {i.name}")