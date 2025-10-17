import os
import pathlib
from datetime import datetime

def create_project_snapshot(root_dir=".", output_file="project_snapshot.txt", excluded_dirs=None, excluded_files=None):
    """
    Generates a single file with both the project's directory tree and the contents of each file.

    The script excludes common directories like __pycache__, .git, venv, and the output file itself.
    You can customize the excluded directories and files by passing sets to the function.
    
    Args:
        root_dir (str): The starting directory to traverse.
        output_file (str): The name of the output file.
        excluded_dirs (set): A set of directory names to exclude.
        excluded_files (set): A set of file names to exclude.
    """
    # Define default directories and files to exclude.
    default_excluded_dirs = {'.git', '__pycache__', '.venv', 'env', 'venv', 'clarityStreamEnv'}
    default_excluded_files = {output_file, '.env', '.gitignore'}
    excluded_extensions = {'.pyc', '.png', '.jpg', '.jpeg', '.gif', '.zip', '.tar.gz', '.log'}
    
    # Combine default exclusions with any user-provided ones.
    all_excluded_dirs = default_excluded_dirs.union(excluded_dirs or set())
    all_excluded_files = default_excluded_files.union(excluded_files or set())

    # Get the name of the root directory.
    root_name = os.path.basename(os.path.abspath(root_dir))
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # --- Section 1: Project Tree ---
        f.write("=== PROJECT DIRECTORY TREE ===\n\n")
        f.write(f"|-- {root_name}\n")
        
        # Walk the directory tree to create the visual representation.
        for root, dirs, files in os.walk(root_dir, topdown=True):
            # Exclude directories specified.
            dirs[:] = [d for d in dirs if d not in all_excluded_dirs]
            
            relative_path = os.path.relpath(root, start=root_dir)
            if relative_path == ".":
                # Process files in the root directory.
                for file in sorted(files):
                    if file not in all_excluded_files and pathlib.Path(file).suffix not in excluded_extensions:
                        f.write(f"|   |-- {file}\n")
                continue

            level = relative_path.count(os.sep)
            prefix = '|   ' * level + '|-- '
            f.write(f"{prefix}{os.path.basename(root)}\n")
            
            sub_prefix = '|   ' * (level + 1) + '|-- '
            for file in sorted(files):
                if file not in all_excluded_files and pathlib.Path(file).suffix not in excluded_extensions:
                    f.write(f"{sub_prefix}{file}\n")
        
        # --- Section 2: File Contents ---
        f.write("\n\n=== PROJECT FILE CONTENTS ===\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write(f"Root directory: {os.path.abspath(root_dir)}\n")
        f.write(f"Excluded file extensions: {', '.join(excluded_extensions)}\n\n")

        # Walk the directory tree again to capture file contents.
        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in all_excluded_dirs]
            
            relative_dir_path = os.path.relpath(root, start=root_dir)
            f.write(f"\n--- DIRECTORY: {relative_dir_path or '.'} ---\n")

            for file in sorted(files):
                file_path = pathlib.Path(root) / file
                
                # Skip excluded files and extensions.
                if (file in all_excluded_files or 
                    file_path.suffix in excluded_extensions):
                    continue
                
                f.write(f"\n--- FILE: {file_path.relative_to(root_dir)} ---\n")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as file_content:
                        content = file_content.read()
                        f.write(f"\n{content}\n")
                except UnicodeDecodeError:
                    f.write("\n[Binary content - not displayed]\n")
                except Exception as e:
                    f.write(f"\n[Error reading file: {str(e)}]\n")
                
                f.write("-" * 50 + "\n")
    
    print(f"Project snapshot saved to '{output_file}' successfully.")

if __name__ == "__main__":
    # Example usage:
    print("Creating a combined project snapshot...")
    # You can add custom excluded directories or files here.
    # For example: create_project_snapshot(excluded_dirs={'dist'}, excluded_files={'README.md'})
    create_project_snapshot()
    print("Combined snapshot generated successfully.")
