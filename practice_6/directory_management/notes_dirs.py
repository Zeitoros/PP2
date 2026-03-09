from pathlib import Path

current_dir = Path(__file__).parent

base_path = current_dir / "my_folder" / "data" / "logs"

base_path.mkdir(parents=True, exist_ok=True)

(base_path / "app.log").touch()
(base_path / "error.txt").touch()

print(f"The structure was created successfully by path:\n{base_path}")


project_root = current_dir / "my_folder"
print(f"Content: {project_root.name}:")

for i in project_root.iterdir():
    type_item = "Folder" if i.is_dir() else "File"
    print(f"   [{type_item}] {i.name}")

for log in project_root.rglob("*.log"):
    print(f"   Log is found: {log.relative_to(current_dir)}")