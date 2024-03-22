#!/bin/bash
# create_new_project.sh

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <old_name> <new_name>"
    exit 1
fi

old_name="$1"
new_name="$2"

# Print the current working directory
echo "Current working directory: $(pwd)"

# Copy the template project to a new directory
cp -r "../$old_name" "../$new_name"

# Print the current working directory where new project is located
echo "Project built in: $(pwd)/$new_name"

# Remove non-essential base folders and files
cd ../$new_name
rm -rf $old_name.egg-info
rm -rf cache
rm -rf docker/secrets
rm docker/.env
rm -rf htmlcov
rm -rf logs
rm -rf .idea
rm -rf venv
rm -rf wheels
rm usr_vars

# Remove non-essential folders and files from each microservices

# Define the directories and files to delete
directories=("data" "docker" "docs" "logs" "__pycache__")
files=("usr_vars" ".yapfignore")

# Loop through each directory and file
for dir in "${directories[@]}"; do
    # Delete directories
    find "$old_name" -type d -name "$dir" -exec rm -rf {} +
done

for file in "${files[@]}"; do
    # Delete files
    find "$old_name" -type f -name "$file" -exec rm -f {} +
done

# Delete utils directories within specific subdirectories
find "$old_name" \( -path "$old_name/utils" -prune \) -o \( -path "*/utils" -exec rm -rf {} + \)

# Update file contents
mv $old_name $new_name
find . -type f -exec sed -i "s/$old_name/$new_name/g" {} +

# Removing git directory from template
rm -rf .git

echo "New project '$new_name' created successfully!"
