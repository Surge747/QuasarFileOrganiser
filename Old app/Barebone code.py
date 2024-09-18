import os
from pathlib import Path

def list_directory_details(directory):
    """List details of all files and folders in the given directory."""
    directory_path = Path(directory)
    
    if not directory_path.exists() or not directory_path.is_dir():
        print(f"{directory} is not a valid directory.")
        return
    
    for item in directory_path.iterdir():
        # Get file or directory details
        item_type = "Folder" if item.is_dir() else "File"
        item_size = item.stat().st_size
        item_name = item.name
        item_modified = item.stat().st_mtime
        
        # Print the details
        print(f"{item_type}: {item_name}")
        print(f"  Size: {item_size} bytes")
        print(f"  Last Modified: {item_modified}")
        print()

# Example usage
directory_to_list = "C:\\Users\\Madhav Krishnan\\Desktop\\Madhav\\Projects\\Downloads fake"
list_directory_details(directory_to_list)
