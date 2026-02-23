#!/usr/bin/env sh
# Resize images in git worktree (staged or modified).
# Uses ImageMagick: -strip -auto-orient -resize 1000x1000>
# Ref: blog.alswl.com image compression management.

for i in $(git status | grep images | awk '{print $3}'); do
    echo resize "$i";
    magick "$i" -strip -auto-orient -resize 1000x1000\> "$i";
done
