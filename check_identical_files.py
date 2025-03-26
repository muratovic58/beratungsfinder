import os
from pathlib import Path

def are_files_identical():
    # Get the directory path
    dir_path = Path('scraped_firms')
    
    # Get all .txt files in the directory
    files = list(dir_path.glob('*.txt'))
    
    if not files:
        print("No files found in the directory")
        return False
    
    # Read the content of the first file
    with open(files[0], 'r', encoding='utf-8') as f:
        reference_content = f.read()
    
    print(f"Comparing all files against {files[0].name}...")
    print(f"Total files to check: {len(files)}")
    
    # Compare each file with the first file
    for file in files[1:]:
        with open(file, 'r', encoding='utf-8') as f:
            current_content = f.read()
            if current_content != reference_content:
                print(f"Found different content in {file.name}")
                # Print the first few characters of both files
                print("\nReference content starts with:")
                print(reference_content[:200])
                print("\nDifferent content starts with:")
                print(current_content[:200])
                return False
    
    print("All files are identical!")
    return True

if __name__ == "__main__":
    result = are_files_identical()
    print(f"\nResult: {result}")
