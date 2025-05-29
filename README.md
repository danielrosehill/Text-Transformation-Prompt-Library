# Text Transformation Prompt Library

A comprehensive collection of text transformation prompts for reformatting dictated text into various formats, styles, and structures.

## Quick Links

- [**Browse All Prompts (Markdown Index)**](./index.md) - Human-readable alphabetical index of all prompts
- [**JSON Index**](./prompts.json) - Machine-readable consolidated JSON of all prompts

## Repository Structure

### `/prompts/`
The main collection of text transformation prompts, populated by automation workflows.

- **`/prompts/md/`** - Markdown format prompts (130 prompts)
- **`/prompts/json/`** - JSON format equivalents of the markdown prompts
- **`.gitkeep`** - Placeholder file for automation

### `/to-integrate/`
Staging area for new prompts that will be processed by automation and added to the main collection.

### `/other-repos/`
Contains consolidated prompts from initial collections for manual review and integration.

- **`/other-repos/consolidated-prompts/`** - Flat structure containing 248 prompts from previous collections

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

### For Integration
1. Add new prompts to the `/to-integrate/` folder
2. Automation will process and move them to the main collection
3. Review consolidated prompts in `/other-repos/consolidated-prompts/` for missing items

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
