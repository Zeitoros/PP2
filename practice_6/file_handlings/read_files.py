from pathlib import Path

current_dir = Path(__file__).parent
file_path = current_dir / "sample.txt"

if file_path.exists():
    print(f"Reading content of {file_path.name}:\n" + "-"*20)
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        print(content)
    
    lines = file_path.read_text(encoding="utf-8").splitlines()
    print("-"*20)
    print(f"Total rows in file: {len(lines)}")
else:
    print("File does not find")
