#!/bin/bash

# Add sensitive files and directories to .gitignore
echo ".env" >> .gitignore
echo "config/auto_ai_key" >> .gitignore
echo ".local" >> .gitignore
echo ".python_history" >> .gitignore
echo ".cache" >> .gitignore
echo ".config" >> .gitignore
echo "notebook_secret" >> .gitignore

# Remove already cached files
git rm --cached -r .

# Add all files back to staging area
git add .

# Commit changes
git commit -m "Update .gitignore to ignore sensitive files"

# Push to remote repository
git push -u origin main

echo "Git setup completed successfully!"
