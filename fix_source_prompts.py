#!/usr/bin/env python3
"""
Script to fix duplicated names in source JSON prompt files.
This script will modify the source files directly.
"""

import json
import os
import glob
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def fix_source_prompts(json_dir):
    """
    Fix duplicated names in source JSON prompt files.
    
    Args:
        json_dir (str): Path to directory containing JSON prompt files
    
    Returns:
        int: Number of files fixed
    """
    # Get a list of all JSON files in the directory
    json_files = glob.glob(os.path.join(json_dir, "*.json"))
    logging.info(f"Found {len(json_files)} JSON files in {json_dir}")
    
    # Track fixed files
    fixed_count = 0
    
    # Process each JSON file
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                prompt_data = json.load(f)
            
            # Skip if the prompt doesn't have a name
            if 'name' not in prompt_data:
                logging.warning(f"Skipping {file_path} - missing 'name' field")
                continue
            
            # Check if name is duplicated
            if '\n' in prompt_data['name']:
                original_name = prompt_data['name']
                prompt_data['name'] = prompt_data['name'].split('\n')[0].strip()
                
                # Write fixed data back to file
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(prompt_data, f, indent=2, ensure_ascii=False)
                
                logging.info(f"Fixed {file_path}: '{original_name}' -> '{prompt_data['name']}'")
                fixed_count += 1
                
        except json.JSONDecodeError:
            logging.error(f"Error parsing JSON from {file_path}")
        except Exception as e:
            logging.error(f"Error processing {file_path}: {str(e)}")
    
    logging.info(f"Fixed {fixed_count} files")
    return fixed_count

if __name__ == "__main__":
    # Directory containing JSON prompt files
    JSON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts", "json")
    
    # Run the fix
    fixed_count = fix_source_prompts(JSON_DIR)
    
    print(f"Fixed {fixed_count} JSON files with duplicated names")
