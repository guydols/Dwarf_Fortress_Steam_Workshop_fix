import os
import shutil
import re
import argparse
import sys

def validate_directories(src_dir):
    if not os.path.exists(src_dir):
        print(f"Error: Source directory '{src_dir}' does not exist.")
        return False

    if not os.path.isdir(src_dir):
        print(f"Error: Source path '{src_dir}' is not a directory.")
        return False

    return True

def clear_destination(dest_dir):
    print(f"Clearing destination directory: {dest_dir}")
    if os.path.exists(dest_dir):
        for item in os.listdir(dest_dir):
            item_path = os.path.join(dest_dir, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
    else:
        os.makedirs(dest_dir)

def extract_mod_id(info_file_path, directory_name, failed_mods):
    try:
        with open(info_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            match = re.search(r'\[ID:([^\]]+)\]', content)
            if match:
                directory_id = match.group(1)
                print(f"Found ID: {directory_id} in directory {directory_name}")
                return directory_id
            else:
                error = "No ID pattern found in info.txt"
                failed_mods.append((directory_name, error))
                print(f"Warning: No ID pattern found in info.txt for directory {directory_name}, skipping.")
                return None
    except Exception as e:
        error = f"Error reading info.txt: {str(e)}"
        failed_mods.append((directory_name, error))
        print(f"Error reading info.txt in directory {directory_name}: {e}")
        return None

def copy_directory_contents(src_path, dest_path, directory_name, failed_mods):
    mod_error = None
    try:
        print(f"Copying contents from {directory_name} to {os.path.basename(dest_path)}")
        for item in os.listdir(src_path):
            source_item = os.path.join(src_path, item)
            dest_item = os.path.join(dest_path, item)

            try:
                if os.path.isdir(source_item):
                    shutil.copytree(source_item, dest_item)
                else:
                    shutil.copy2(source_item, dest_item)
            except Exception as e:
                mod_error = f"Failed to copy item '{item}': {str(e)}"
                failed_mods.append((directory_name, mod_error))
                print(f"Error copying {item} from {directory_name}: {e}")

        return mod_error is None
    except Exception as e:
        error = f"General error during copy: {str(e)}"
        failed_mods.append((directory_name, error))
        print(f"Error processing directory {directory_name}: {e}")
        return False

def print_summary(directories_processed, failed_mods):
    print(f"\nSynchronization completed! Processed {directories_processed} directories successfully.")

    if failed_mods:
        print(f"\nFAILED MODS SUMMARY ({len(failed_mods)} total):")
        print("=" * 80)
        for mod_name, error in failed_mods:
            print(f"Mod: {mod_name}")
            print(f"Error: {error}")
            print("-" * 80)
    else:
        print("\nAll mods were copied successfully!")

def process_directory(directory_path, directory_name, dest_dir, failed_mods):
    info_file_path = os.path.join(directory_path, "info.txt")
    if not os.path.exists(info_file_path):
        failed_mods.append((directory_name, "No info.txt found"))
        print(f"Warning: No info.txt found in directory {directory_name}, skipping.")
        return False

    directory_id = extract_mod_id(info_file_path, directory_name, failed_mods)
    if not directory_id:
        return False

    dest_directory_path = os.path.join(dest_dir, directory_id)
    os.makedirs(dest_directory_path, exist_ok=True)

    return copy_directory_contents(directory_path, dest_directory_path, directory_name, failed_mods)

def sync_directories(src_dir, dest_dir):
    if not validate_directories(src_dir):
        return False

    clear_destination(dest_dir)

    print(f"Processing source directory: {src_dir}")
    directories_processed = 0
    failed_mods = []

    for directory_name in os.listdir(src_dir):
        directory_path = os.path.join(src_dir, directory_name)

        if not os.path.isdir(directory_path):
            continue

        if process_directory(directory_path, directory_name, dest_dir, failed_mods):
            directories_processed += 1

    print_summary(directories_processed, failed_mods)
    return True

def main():
    parser = argparse.ArgumentParser(
        description='Synchronize directories based on IDs found in info.txt files.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('src', help='Full path of workshop content directory, example "/home/guy/.steam/steam/steamapps/workshop/content/975370"')
    parser.add_argument('dest', help='Full path of installed_mods directory, example "/home/guy/.steam/steam/steamapps/common/Dwarf Fortress/data/installed_mods"')

    args = parser.parse_args()

    success = sync_directories(args.src, args.dest)

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
