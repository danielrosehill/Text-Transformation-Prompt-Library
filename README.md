# Text Transformation Prompt Library

A comprehensive collection of text transformation prompts for reformatting dictated text into various formats, styles, and structures.

## Quick Links

[![Markdown Index](https://img.shields.io/badge/Browse_All_Prompts-Markdown_Index-blue)](./index.md)
[![JSON Index](https://img.shields.io/badge/Machine_Readable-JSON_Index-green)](./prompts.json)

## Repository Structure

### `/prompts/`
The main collection of text transformation prompts.

- **`/prompts/md/`** - Markdown format prompts
- **`/prompts/json/`** - JSON format equivalents of the markdown prompts

## Prompt Structure

Each prompt follows a standardized markdown format:

```markdown
# [Prompt Name]

## Name
[Descriptive name]

## Description
[Optional description]

## System Prompt Text
```
[The actual prompt text that will be used by AI systems]
```

## Expected Output Format
[Optional format specifications]

## Delivers Structured Output?
[Yes/No indicator]
```

## Usage

### For AI Systems
Use the prompts in the `/prompts/md/` or `/prompts/json/` folders as system prompts for text transformation tasks.

### Updating Indexes
To update both the JSON and Markdown indexes as the library grows:

```bash
python3 update_indexes.py
```

This script:
1. Fixes any duplicated names in source JSON files
2. Consolidates all JSON prompt files into `prompts.json`
3. Generates a markdown index (`index.md`) from the consolidated JSON



## Categories

The library includes prompts for:

- **Business Communication** - Professional emails, meeting minutes, proposals
- **Documentation** - Technical docs, process documentation, README files
- **Content Creation** - Blog outlines, social media posts, newsletters
- **Task Management** - To-do lists, project plans, status updates
- **Format Conversion** - JSON output, HTML formatting, structured data
- **Style Transformation** - Formal/casual tone, clarity improvements
- **Specialized Formats** - RFPs, cover letters, testimonials

## Automation

This repository uses automated workflows to:
- Process prompts from `/to-integrate/` folder
- Generate standardized markdown format
- Create JSON equivalents
- Maintain consistent naming and structure

## Contributing

1. Add new prompts to the `/to-integrate/` folder
2. Follow the standard markdown format
3. Ensure prompts are practical and non-novelty focused
4. Automation will handle integration into the main collection

## File Naming Convention

Prompts are automatically named with the pattern:
`[descriptive_name]_[date].md`

Example: `business_email_270525.md`
