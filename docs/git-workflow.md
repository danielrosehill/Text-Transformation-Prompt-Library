# Git Workflow Documentation

## Common Git Operations for Text Transformation Prompt Library

### Daily Workflow

#### 1. Sync with Remote (Rebase)
When you need to sync your local changes with remote updates:

```bash
git pull --rebase origin main
git push origin main
```

**Why rebase?** 
- Keeps a clean, linear commit history
- Avoids unnecessary merge commits
- Places your local commits on top of remote changes

#### 2. Quick Commit and Push
For routine updates (use the `gp` alias or script):

```bash
git add .
git commit -m "commit"
git pull --rebase origin main
git push origin main
```

### Handling Conflicts

If you encounter merge conflicts during rebase:

1. **View conflicted files:**
   ```bash
   git status
   ```

2. **Edit conflicted files** (remove conflict markers `<<<<<<<`, `=======`, `>>>>>>>`)

3. **Stage resolved files:**
   ```bash
   git add <filename>
   ```

4. **Continue rebase:**
   ```bash
   git rebase --continue
   ```

5. **If you want to abort:**
   ```bash
   git rebase --abort
   ```

### Repository Structure Maintenance

#### Moving Files to Integration Folder
When moving prompts from other collections to the main library:

```bash
# Move files to staging area
mv other-repos/collection-name/prompt.md to-integrate/

# Commit the move
git add .
git commit -m "Move prompt.md to integration staging"

# Sync and push
git pull --rebase origin main
git push origin main
```

#### Cleaning Up Consolidated Files
When removing duplicate/consolidated prompt files:

1. Delete files through IDE or command line
2. Commit deletions with descriptive message
3. Use rebase workflow to sync

### Useful Git Aliases

Add these to your `~/.gitconfig`:

```ini
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    rb = rebase
    lg = log --oneline --graph --decorate
```

### Troubleshooting

#### Push Rejected (Remote Changes)
**Error:** `Updates were rejected because the remote contains work that you do not have locally`

**Solution:** Use rebase workflow:
```bash
git pull --rebase origin main
git push origin main
```

#### Detached HEAD State
If you end up in detached HEAD:
```bash
git checkout main
git pull --rebase origin main
```

#### Accidental Commits
To undo last commit (keeping changes):
```bash
git reset --soft HEAD~1
```

To undo last commit (discarding changes):
```bash
git reset --hard HEAD~1
```

### Best Practices

1. **Always rebase instead of merge** for cleaner history
2. **Commit frequently** with descriptive messages
3. **Pull before starting work** to avoid conflicts
4. **Use the automated script** for routine operations
5. **Check status** before committing: `git status`

### Scripts

Use the provided `sync-repo.sh` script for automated rebase workflow:
```bash
./sync-repo.sh
```

This handles the complete pull → rebase → push cycle automatically.
