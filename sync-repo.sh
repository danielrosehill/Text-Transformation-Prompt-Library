#!/bin/bash

# Text Transformation Prompt Library - Git Sync Script
# Automates the pull → rebase → push workflow

set -e  # Exit on any error

echo "🔄 Starting repository sync..."

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "📝 Uncommitted changes detected. Staging and committing..."
    git add .
    
    # Get current timestamp for commit message
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    git commit -m "Auto-commit: $timestamp"
    echo "✅ Changes committed"
else
    echo "✅ Working directory clean"
fi

# Pull with rebase
echo "⬇️  Pulling latest changes with rebase..."
if git pull --rebase origin main; then
    echo "✅ Rebase successful"
else
    echo "❌ Rebase failed. You may need to resolve conflicts manually."
    echo "💡 Run 'git status' to see conflicted files"
    echo "💡 After resolving conflicts, run 'git rebase --continue'"
    exit 1
fi

# Push changes
echo "⬆️  Pushing changes..."
if git push origin main; then
    echo "✅ Push successful"
else
    echo "❌ Push failed"
    exit 1
fi

echo "🎉 Repository sync completed successfully!"

# Show current status
echo ""
echo "📊 Current repository status:"
git log --oneline -3
