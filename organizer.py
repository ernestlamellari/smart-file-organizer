import os
import shutil
from pathlib import Path

FILE_CATEGORIES = {
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".csv", ".pptx"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".json", ".sql", ".cpp", ".java"],
}

def get_category(extension: str) -> str:
    ext = extension.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return "Other"

def organize_folder(target_dir: str, dry_run: bool = False) -> None:
    folder_path = Path(target_dir).expanduser().resolve()

    if not folder_path.exists() or not folder_path.is_dir():
        print(f"Error: '{folder_path}' is not a valid directory.")
        return

    moved_count = 0

    for item in folder_path.iterdir():
        if item.is_dir() or item.name.startswith("."):
            continue

        category = get_category(item.suffix)
        dest_dir = folder_path / category
        dest_file = dest_dir / item.name

        counter = 1
        while dest_file.exists():
            dest_file = dest_dir / f"{item.stem}_{counter}{item.suffix}"
            counter += 1

        if dry_run:
            print(f"[DRY RUN] Would move: {item.name} -> {category}/{dest_file.name}")
        else:
            dest_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(dest_file))
            print(f"Moved: {item.name} -> {category}/{dest_file.name}")

        moved_count += 1

    action = "scanned" if dry_run else "organized"
    print(f"\nDone! Total files {action}: {moved_count}")


if __name__ == "__main__":
    print("=== Smart Folder Organizer ===")
    path_input = input("Enter the full folder path to organize: ").strip()
    mode_input = input("Run in dry-run preview mode first? (y/n): ").strip().lower()
    organize_folder(path_input, dry_run=(mode_input == "y"))
