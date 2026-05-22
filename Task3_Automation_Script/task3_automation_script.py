"""
Task 3: Automation Script
Intern: Nikhil Singh | Application: NJ-KABGLTK
Automates real-world file management: organise, rename, sort, and log files.
"""

import os
import shutil
import json
from datetime import datetime

# ─────────────────────────────────────────
#  Configuration
# ─────────────────────────────────────────

CATEGORIES = {
    "Images"    : [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Videos"    : [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
    "Audio"     : [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "Documents" : [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".csv"],
    "Code"      : [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".ts", ".json", ".xml"],
    "Archives"  : [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Others"    : []
}

LOG_FILE = "automation_log.txt"

# ─────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────

def log(message: str, entries: list):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print("  " + line)
    entries.append(line)

def write_log(entries: list):
    with open(LOG_FILE, "a") as f:
        f.write("\n" + "=" * 60 + "\n")
        f.write(f"  Session: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n")
        for e in entries:
            f.write(e + "\n")
    print(f"\n  Log saved to '{LOG_FILE}'")

def get_category(ext: str) -> str:
    ext = ext.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"

def print_header():
    print("=" * 55)
    print("   FILE AUTOMATION SCRIPT")
    print("   Intern: Nikhil Singh | NJ-KABGLTK")
    print("=" * 55)

def print_menu():
    print("\n  AUTOMATION MENU")
    print("  ─────────────────────────────────────────")
    print("  1. Organise files by type into folders")
    print("  2. Batch rename files with a prefix")
    print("  3. Sort & list files by size or date")
    print("  4. Find files by extension")
    print("  5. Delete empty folders")
    print("  0. Exit")
    print("  ─────────────────────────────────────────")

# ─────────────────────────────────────────
#  Feature 1: Organise Files by Type
# ─────────────────────────────────────────

def organise_files(folder: str, log_entries: list):
    if not os.path.isdir(folder):
        print(f"  '{folder}' is not a valid directory.")
        return

    moved = 0
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if not os.path.isfile(filepath):
            continue

        _, ext = os.path.splitext(filename)
        category = get_category(ext)
        dest_dir = os.path.join(folder, category)
        os.makedirs(dest_dir, exist_ok=True)

        dest_path = os.path.join(dest_dir, filename)
        base, extension = os.path.splitext(filename)
        counter = 1
        while os.path.exists(dest_path):
            dest_path = os.path.join(dest_dir, f"{base}_{counter}{extension}")
            counter += 1

        shutil.move(filepath, dest_path)
        log(f"Moved '{filename}' -> {category}/", log_entries)
        moved += 1

    print(f"\n  Organised {moved} file(s) into category folders.")

# ─────────────────────────────────────────
#  Feature 2: Batch Rename Files
# ─────────────────────────────────────────

def batch_rename(folder: str, log_entries: list):
    if not os.path.isdir(folder):
        print(f"  '{folder}' is not a valid directory.")
        return

    prefix = input("  Enter prefix to add (e.g. 'nikhil_'): ").strip()
    if not prefix:
        print("  Prefix cannot be empty.")
        return

    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    if not files:
        print("  No files found in the directory.")
        return

    print(f"\n  Found {len(files)} file(s). Renaming preview:")
    for f in files[:5]:
        print(f"    {f}  ->  {prefix}{f}")
    if len(files) > 5:
        print(f"    ... and {len(files) - 5} more")

    confirm = input("\n  Proceed with rename? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("  Rename cancelled.")
        return

    renamed = 0
    for filename in files:
        old_path = os.path.join(folder, filename)
        new_name = prefix + filename
        new_path = os.path.join(folder, new_name)
        if not os.path.exists(new_path):
            os.rename(old_path, new_path)
            log(f"Renamed '{filename}' -> '{new_name}'", log_entries)
            renamed += 1
        else:
            log(f"SKIP '{filename}': target '{new_name}' already exists", log_entries)

    print(f"\n  Renamed {renamed} file(s).")

# ─────────────────────────────────────────
#  Feature 3: Sort & List Files
# ─────────────────────────────────────────

def sort_files(folder: str, log_entries: list):
    if not os.path.isdir(folder):
        print(f"  '{folder}' is not a valid directory.")
        return

    sort_by = input("  Sort by (size / date): ").strip().lower()
    if sort_by not in ("size", "date"):
        print("  Invalid option.")
        return

    files = []
    for f in os.listdir(folder):
        fp = os.path.join(folder, f)
        if os.path.isfile(fp):
            size  = os.path.getsize(fp)
            mtime = os.path.getmtime(fp)
            files.append((f, size, mtime))

    if not files:
        print("  No files found.")
        return

    if sort_by == "size":
        files.sort(key=lambda x: x[1], reverse=True)
        print(f"\n  {'File':<35} {'Size':>12}")
        print("  " + "-" * 50)
        for name, size, _ in files:
            size_str = f"{size / 1024:.2f} KB" if size >= 1024 else f"{size} B"
            print(f"  {name:<35} {size_str:>12}")
    else:
        files.sort(key=lambda x: x[2], reverse=True)
        print(f"\n  {'File':<35} {'Last Modified'}")
        print("  " + "-" * 60)
        for name, _, mtime in files:
            mod_time = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            print(f"  {name:<35} {mod_time}")

    log(f"Listed {len(files)} files sorted by {sort_by} in '{folder}'", log_entries)

# ─────────────────────────────────────────
#  Feature 4: Find Files by Extension
# ─────────────────────────────────────────

def find_by_extension(folder: str, log_entries: list):
    if not os.path.isdir(folder):
        print(f"  '{folder}' is not a valid directory.")
        return

    ext = input("  Enter file extension (e.g. .py, .txt): ").strip().lower()
    if not ext.startswith("."):
        ext = "." + ext

    matches = []
    for root, _, files in os.walk(folder):
        for f in files:
            if f.lower().endswith(ext):
                full_path = os.path.join(root, f)
                size = os.path.getsize(full_path)
                matches.append((full_path, size))

    if matches:
        print(f"\n  Found {len(matches)} '{ext}' file(s):\n")
        for path, size in matches:
            size_str = f"{size / 1024:.2f} KB" if size >= 1024 else f"{size} B"
            print(f"  {path}  ({size_str})")
        log(f"Found {len(matches)} '{ext}' file(s) in '{folder}'", log_entries)
    else:
        print(f"  No '{ext}' files found.")

# ─────────────────────────────────────────
#  Feature 5: Delete Empty Folders
# ─────────────────────────────────────────

def delete_empty_folders(folder: str, log_entries: list):
    if not os.path.isdir(folder):
        print(f"  '{folder}' is not a valid directory.")
        return

    removed = 0
    for root, dirs, files in os.walk(folder, topdown=False):
        for d in dirs:
            dir_path = os.path.join(root, d)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                log(f"Deleted empty folder: '{dir_path}'", log_entries)
                removed += 1

    if removed:
        print(f"\n  Removed {removed} empty folder(s).")
    else:
        print("\n  No empty folders found.")

# ─────────────────────────────────────────
#  Main
# ─────────────────────────────────────────

def main():
    print_header()
    log_entries = []

    folder = input("\n  Enter the target folder path\n  (or press Enter to use current directory): ").strip()
    if not folder:
        folder = os.getcwd()
    folder = os.path.abspath(folder)
    print(f"\n  Working directory: {folder}")

    while True:
        print_menu()
        choice = input("  Enter your choice: ").strip()

        if   choice == "1": organise_files(folder, log_entries)
        elif choice == "2": batch_rename(folder, log_entries)
        elif choice == "3": sort_files(folder, log_entries)
        elif choice == "4": find_by_extension(folder, log_entries)
        elif choice == "5": delete_empty_folders(folder, log_entries)
        elif choice == "0":
            if log_entries:
                write_log(log_entries)
            print("\n  Goodbye, Nikhil! Automation complete.\n")
            break
        else:
            print("  Invalid choice. Please enter 0-5.")

        input("\n  Press Enter to continue...")

if __name__ == "__main__":
    main()
