from pathlib import Path

current_dir = Path(__file__).parent
file_path = current_dir / "sample.txt"

data = ["First row\n", "Second row\n", "Third row\n"]

with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(data)

print(f"File {file_path.name} was created and filled successfully")

with open(file_path, "a", encoding="utf-8") as f:
    f.write("Added row\n")