#!/bin/bash
#
# Format script for en.blog.alswl.com (aligned with reference blog)
# Matches the logic of hooks/pre-commit, but also accepts file arguments

# Function to format files
format_files() {
    local files="$1"
    if [ "$files" = "" ]; then
        echo "No Markdown files to format"
        return 0
    fi

    echo "Running format..."

    # Format each Markdown file
    for file in $files; do
        if [ -f "$file" ]; then
            echo "Formatting: $file"
            npx prettier "$file" --write
            # Stage the formatted file if it was staged
            if git diff --cached --name-only 2>/dev/null | grep -q "^${file}$"; then
                git add "$file"
            fi
        fi
    done

    echo "Formatting complete"
}

# If arguments are provided, format those files
if [ $# -gt 0 ]; then
    # Filter to only Markdown files
    md_files=""
    for arg in "$@"; do
        if [ -f "$arg" ] && [[ "$arg" == *.md ]]; then
            md_files="$md_files $arg"
        fi
    done
    format_files "$md_files"
    exit 0
fi

# No arguments provided, use pre-commit logic

# Get the reference for git diff
if git rev-parse --verify HEAD >/dev/null 2>&1; then
    against=HEAD
else
    # Initial commit: diff against an empty tree object
    against=4b825dc642cb6eb9a060e54bf8d69288fbee4904
fi

# Check for non-ASCII filenames (same as pre-commit hook)
allownonascii=$(git config hooks.allownonascii)
if [ "$allownonascii" != "true" ]; then
    if test $(git diff --cached --name-only --diff-filter=A -z $against | LC_ALL=C tr -d '[ -~]\0' | wc -c) != 0; then
        echo "Error: Attempt to add a non-ascii file name." >&2
        echo >&2
        echo "This can cause problems if you want to work" >&2
        echo "with people on other platforms." >&2
        echo >&2
        echo "To be portable it is advisable to rename the file ..." >&2
        echo >&2
        echo "If you know what you are doing you can disable this" >&2
        echo "check using:" >&2
        echo >&2
        echo "  git config hooks.allownonascii true" >&2
        echo >&2
        exit 1
    fi
fi

# Redirect output to stderr
exec 1>&2

# Get staged Markdown files (same as pre-commit hook)
staged_md_files=$(git diff --cached --name-only --diff-filter=ACMR | grep '.md$' || true)

# Format the staged files
format_files "$staged_md_files"
