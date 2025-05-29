#!/usr/bin/env python3
"""
Script to generate a markdown index (index.md) from the consolidated prompts.json file.
The index will be ordered alphabetically by prompt name and follow the specified format.
This script supports incremental updates to the index.md file.
"""

import json
import os
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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
    
    # Input JSON file
    JSON_FILE = repo_root / "prompts.json"
    
    # Output markdown file
    OUTPUT_FILE = repo_root / "index.md"
    
    # Generate markdown index
    prompt_count = generate_markdown_index(JSON_FILE, OUTPUT_FILE)
    
    print(f"Generated markdown index for {prompt_count} prompts in index.md")
