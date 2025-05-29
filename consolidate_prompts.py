#!/usr/bin/env python3
"""
Script to consolidate all JSON prompt files from prompts/json directory into a single prompts.json file.
This script can be run repeatedly to incrementally update the prompts.json file as new prompts are added.
"""

import json
import os
import glob
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def consolidate_prompts(json_dir, output_file):
    """
    Consolidate all JSON prompt files into a single JSON file.
    
    Args:
        json_dir (str): Path to directory containing JSON prompt files
        output_file (str): Path to output JSON file
    
    Returns:
        int: Number of prompts processed
    """
    # Get the repository root directory
    repo_root = Path(json_dir).parent.parent
    
    # Full path to output file
    output_path = repo_root / output_file
    
    # Initialize prompts list
    all_prompts = []
    
    # Load existing prompts if the file exists
    if os.path.exists(output_path):
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                all_prompts = json.load(f)
            logging.info(f"Loaded {len(all_prompts)} existing prompts from {output_file}")
        except json.JSONDecodeError:
            logging.warning(f"Error reading existing {output_file}. Starting fresh.")
            all_prompts = []
    
    # Get a list of all JSON files in the directory
    json_files = glob.glob(os.path.join(json_dir, "*.json"))
    logging.info(f"Found {len(json_files)} JSON files in {json_dir}")
    
    # Create a set of existing prompt names for quick lookup
    existing_prompt_names = {prompt.get('name', ''): i for i, prompt in enumerate(all_prompts)}
    
    # Track new and updated prompts
    new_count = 0
    updated_count = 0
    
    # Process each JSON file
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                prompt_data = json.load(f)
            
            # Skip if the prompt doesn't have a name
            if 'name' not in prompt_data:
                logging.warning(f"Skipping {file_path} - missing 'name' field")
                continue
                
            # Fix duplicated names (e.g., "Business Email\nBusiness Email")
            if '\n' in prompt_data['name']:
                prompt_data['name'] = prompt_data['name'].split('\n')[0].strip()
            
            # Add filename as source
            prompt_data['source_file'] = os.path.basename(file_path)
            
            # Check if this prompt already exists
            if prompt_data['name'] in existing_prompt_names:
                # Update existing prompt
                index = existing_prompt_names[prompt_data['name']]
                all_prompts[index] = prompt_data
                updated_count += 1
            else:
                # Add new prompt
                all_prompts.append(prompt_data)
                existing_prompt_names[prompt_data['name']] = len(all_prompts) - 1
                new_count += 1
                
        except json.JSONDecodeError:
            logging.error(f"Error parsing JSON from {file_path}")
        except Exception as e:
            logging.error(f"Error processing {file_path}: {str(e)}")
    
    # Write consolidated prompts to output file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(all_prompts, f, indent=2, ensure_ascii=False)
        logging.info(f"Successfully wrote {len(all_prompts)} prompts to {output_file}")
        logging.info(f"Added {new_count} new prompts, updated {updated_count} existing prompts")
    except Exception as e:
        logging.error(f"Error writing to {output_file}: {str(e)}")
        return 0
    
    return len(all_prompts)

if __name__ == "__main__":
    # Directory containing JSON prompt files
    JSON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts", "json")
    
    # Output file name
    OUTPUT_FILE = "prompts.json"
    
    # Run the consolidation
    prompt_count = consolidate_prompts(JSON_DIR, OUTPUT_FILE)
    
    print(f"Consolidated {prompt_count} prompts into {OUTPUT_FILE}")
