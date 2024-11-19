#!/bin/bash

# Run neofetch with the --off option and store the output
neofetchOutput=$(neofetch --off)

IMAGE_PATH=/home/dillion/Documents/GitHub/DillionRice-LinuxMint/sports.jpg
ASCII_PATH=/home/dillion/Documents/GitHub/DillionRice-LinuxMint/ascii_art_!neofetch.txt

lines=$(tput cols)

#imageOutput=$(cat $ASCII_PATH)
imageOutput=$(jp2a --color --background=dark --height=37 $IMAGE_PATH)

# Convert the output into arrays split by newline
IFS=$'\n' read -d '' -r -a neofetchLines <<< "$neofetchOutput"
IFS=$'\n' read -d '' -r -a imageLines <<< "$imageOutput"


bufferFromImageAndInfo=""
for i in {1..3}; do
  bufferFromImageAndInfo="$bufferFromImageAndInfo "
done

# Determine the length of the longer array
maxLines=${#neofetchLines[@]}
if [ ${#imageLines[@]} -gt $maxLines ]; then
    maxLines=${#imageLines[@]}
fi

# Loop through the arrays and print each line on the same line
for ((i = 0; i < maxLines; i++)); do
    output=""
    
    # If there is an image line, add it to the output
    if [ $i -lt ${#imageLines[@]} ]; then
        output="${imageLines[i]}"
    fi
    
    # If there is a neofetch line, add it to the output (without newline)
    if [ $i -lt ${#neofetchLines[@]} ]; then
        output="${output}$bufferFromImageAndInfo${neofetchLines[i]}"
    fi
    
    # Print the concatenated output with a newline if needed
    echo "$output"
done
