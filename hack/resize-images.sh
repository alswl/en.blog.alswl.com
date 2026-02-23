#!/usr/bin/env sh

originDir="static/images"
resizedDir="static/img"


IFS=$(echo -en "\n\b"); 
for f in $(find "$originDir" -type f | grep -iE "(jpg|jpeg|png|gif|webp)$"); do
    newF=$(echo "$f" | sed "s#$originDir#$resizedDir#");
    newDir=$(dirname "$newF");
    # if not exist dir, create it
    if [ ! -d "$newDir" ]; then
      mkdir -p "$newDir";
    fi
    if [ -f "$newF" ]; then
        continue;
    fi
    echo "# resize $f";
    cp "$f" "$newF";
    mogrify -strip -auto-orient -resize 1000x1000 "$newF";
done

