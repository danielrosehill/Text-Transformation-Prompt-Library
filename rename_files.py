#!/usr/bin/env python3
"""
Script to rename files in consolidated-prompts folder by moving prefixes to suffixes.
"""

import os
import re

def rename_files_in_directory(directory_path):
    """Rename files by moving prefixes to suffixes."""
    
    if not os.path.exists(directory_path):
        print(f"Directory {directory_path} does not exist")
        return
    
    files = [f for f in os.listdir(directory_path) if f.endswith('.md')]
    
    # Define the prefixes to look for
    prefixes = [
        'Text-Transformation-Prompts-2_',
        'text-transformation-system-prompts_'
    ]
    
    renamed_count = 0
    
    for filename in files:
        old_path = os.path.join(directory_path, filename)
        
        # Check if file starts with any of our prefixes
        prefix_found = None
        for prefix in prefixes:
            if filename.startswith(prefix):
                prefix_found = prefix
                break
        
        if prefix_found:
            # Remove the prefix and the trailing _prompt.md
            content_part = filename[len(prefix_found):]
            if content_part.endswith('_prompt.md'):
                content_part = content_part[:-11]  # Remove '_prompt.md'
            elif content_part.endswith('.md'):
                content_part = content_part[:-3]   # Remove '.md'
            
            # Create new filename: content_prefix.md
            # Clean up the prefix by removing trailing underscore
            clean_prefix = prefix_found.rstrip('_')
            new_filename = f"{content_part}_{clean_prefix}.md"
            
            new_path = os.path.join(directory_path, new_filename)
            
            # Rename the file
            try:
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_filename}")
                renamed_count += 1
            except OSError as e:
                print(f"Error renaming {filename}: {e}")
        else:
            print(f"No matching prefix found for: {filename}")
    
    print(f"\nTotal files renamed: {renamed_count}")

if __name__ == "__main__":
    directory_path = "/home/daniel/repos/myrepos/Text-Transformation-Prompt-Library/other-repos/consolidated-prompts"
    rename_files_in_directory(directory_path)
