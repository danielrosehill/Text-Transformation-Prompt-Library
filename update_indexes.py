#!/usr/bin/env python3
"""
Unified script to update both JSON and Markdown indexes for the Text Transformation Prompt Library.
This script:
1. Fixes any duplicated names in source JSON files
2. Consolidates all JSON prompt files into a single prompts.json file
3. Generates a markdown index (index.md) from the consolidated JSON
"""

import json
import os
import glob
import logging
from pathlib import Path

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

def consolidate_prompts(json_dir, output_file):
    """
    Consolidate all JSON prompt files into a single JSON file.
    
    Args:
        json_dir (str): Path to directory containing JSON prompt files
        output_file (str): Path to output JSON file
    
    Returns:
        int: Number of prompts processed
    """
    # Get a list of all JSON files in the directory
    json_files = glob.glob(os.path.join(json_dir, "*.json"))
    logging.info(f"Found {len(json_files)} JSON files in {json_dir}")
    
    # Initialize prompts list
    all_prompts = []
    
    # Load existing prompts if the file exists
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                all_prompts = json.load(f)
            logging.info(f"Loaded {len(all_prompts)} existing prompts from {output_file}")
        except json.JSONDecodeError:
            logging.warning(f"Error reading existing {output_file}. Starting fresh.")
            all_prompts = []
    
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
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_prompts, f, indent=2, ensure_ascii=False)
        logging.info(f"Successfully wrote {len(all_prompts)} prompts to {output_file}")
        logging.info(f"Added {new_count} new prompts, updated {updated_count} existing prompts")
    except Exception as e:
        logging.error(f"Error writing to {output_file}: {str(e)}")
        return 0
    
    return len(all_prompts)

def generate_markdown_index(json_file, output_file):
    """
    Generate a markdown index from the consolidated prompts.json file.
    
    Args:
        json_file (str): Path to the consolidated JSON file
        output_file (str): Path to the output markdown file
    
    Returns:
        int: Number of prompts processed
    """
    # Check if JSON file exists
    if not os.path.exists(json_file):
        logging.error(f"JSON file not found: {json_file}")
        return 0
    
    # Load prompts from JSON file
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            prompts = json.load(f)
        logging.info(f"Loaded {len(prompts)} prompts from {json_file}")
    except json.JSONDecodeError:
        logging.error(f"Error parsing JSON from {json_file}")
        return 0
    except Exception as e:
        logging.error(f"Error reading {json_file}: {str(e)}")
        return 0
    
    # Sort prompts alphabetically by name
    prompts.sort(key=lambda x: x.get('name', '').lower())
    
    # Generate markdown content
    markdown_content = "# Text Transformation Prompt Library Index\n\n"
    markdown_content += f"*This index contains {len(prompts)} prompts, sorted alphabetically.*\n\n"
    markdown_content += "---\n\n"
    
    # Process each prompt
    for prompt in prompts:
        name = prompt.get('name', 'Unnamed Prompt')
        description = prompt.get('description', 'No description provided.')
        system_prompt_text = prompt.get('system_prompt_text', 'No prompt text available.')
        
        # Determine if the prompt delivers structured output
        delivers_structured = prompt.get('delivers_structured_output', '')
        structured_output = "Yes" if delivers_structured and delivers_structured.lower() == "yes" else "No"
        
        # Get expected output format
        output_format = prompt.get('expected_output_format', 'Not specified')
        
        # Format the markdown for this prompt
        markdown_content += f"## {name}\n\n"
        
        markdown_content += "### Description\n\n"
        markdown_content += f"{description if description else 'No description provided.'}\n\n"
        
        markdown_content += "### Prompt Text\n\n"
        markdown_content += f"```\n{system_prompt_text}\n```\n\n"
        
        markdown_content += "### Details\n\n"
        markdown_content += f"- **Structured Output**: {structured_output}\n"
        markdown_content += f"- **Output Format**: {output_format if output_format else 'Not specified'}\n"
        
        # Add source file information if available
        if 'source_file' in prompt:
            markdown_content += f"- **Source**: {prompt['source_file']}\n"
        
        # Add conversion date if available
        if 'converted_at' in prompt:
            markdown_content += f"- **Converted**: {prompt['converted_at']}\n"
        
        markdown_content += "\n---\n\n"
    
    # Write markdown content to output file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        logging.info(f"Successfully wrote markdown index for {len(prompts)} prompts to {output_file}")
    except Exception as e:
        logging.error(f"Error writing to {output_file}: {str(e)}")
        return 0
    
    return len(prompts)

if __name__ == "__main__":
    # Get repository root directory
    repo_root = Path(__file__).parent
    
    # Directory containing JSON prompt files
    JSON_DIR = repo_root / "prompts" / "json"
    
    # Output files
    JSON_INDEX = repo_root / "prompts.json"
    MARKDOWN_INDEX = repo_root / "index.md"
    
    print("=== Text Transformation Prompt Library Index Updater ===")
    
    # Step 1: Fix source prompts
    print("\nStep 1: Fixing source prompts with duplicated names...")
    fixed_count = fix_source_prompts(JSON_DIR)
    print(f"Fixed {fixed_count} JSON files with duplicated names")
    
    # Step 2: Consolidate JSON prompts
    print("\nStep 2: Consolidating JSON prompts...")
    # If we're starting fresh, remove the existing JSON index
    if os.path.exists(JSON_INDEX) and fixed_count > 0:
        os.remove(JSON_INDEX)
        print(f"Removed existing {JSON_INDEX} to create a fresh index")
    
    prompt_count = consolidate_prompts(JSON_DIR, JSON_INDEX)
    print(f"Consolidated {prompt_count} prompts into {JSON_INDEX}")
    
    # Step 3: Generate markdown index
    print("\nStep 3: Generating markdown index...")
    markdown_count = generate_markdown_index(JSON_INDEX, MARKDOWN_INDEX)
    print(f"Generated markdown index for {markdown_count} prompts in {MARKDOWN_INDEX}")
    
    print("\n=== Index update complete ===")
    print(f"JSON index: {JSON_INDEX}")
    print(f"Markdown index: {MARKDOWN_INDEX}")
    print("\nRun this script anytime to update both indexes as your prompt library grows.")
