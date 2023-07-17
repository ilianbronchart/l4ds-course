#!/bin/bash

# Set input and output directories
input_dir="./data"
output_dir='./csv'

# Create output directories if they don't exist
mkdir -p "$output_dir/anglo-saxon"
mkdir -p "$output_dir/european"

# Function to convert a value to Anglo-saxon format
function to_anglo {
  echo "$1" | tr ',' '.'
}

# Function to convert a value to European format
function to_european {
  echo "$1" | tr '.' ','
}

# Loop through all JSON files in the input directory
for file in $input_dir/*.json; do
  # Extract filename without extension
  filename=$(basename -- "$file")
  filename="${filename%.*}"

  # Add header to CSV files
  echo "date_stolen,description,frame_colors,frame_model,id,manufacturer_name,latitude,longitude,stolen_location,url,year" > $output_dir/anglo-saxon/$filename.csv
  echo "date_stolen;description;frame_colors;frame_model;id;manufacturer_name;latitude;longitude;stolen_location;url;year" > $output_dir/european/$filename.csv

  readarray -t object_array < <(jq -c '.[]' "$file")
  for object in "${object_array[@]}"; do
    # Extract necessary fields from JSON using jq
    date_stolen=$(echo $object | jq -r '.date_stolen // ""')
    description=$(echo $object | jq -r '.description // ""' | tr '\n' ' ' | tr -d '\r')
    frame_colors=$(echo $object | jq -r '.frame_colors | join(":") // ""')
    frame_model=$(echo $object | jq -r '.frame_model // ""')
    id=$(echo $object | jq -r '.id // ""')
    manufacturer_name=$(echo $object | jq -r '.manufacturer_name // ""')
    latitude=$(echo $object | jq -r '.stolen_coordinates[0] // ""')
    longitude=$(echo $object | jq -r '.stolen_coordinates[1] // ""')
    stolen_location=$(echo $object | jq -r '.stolen_location // ""')
    url=$(echo $object | jq -r '.url // ""')
    year=$(echo $object | jq -r '.year // ""')

    # Output data to Anglo-saxon CSV file
    echo "$date_stolen,\"$description\",\"$frame_colors\",\"$frame_model\",$id,\"$manufacturer_name\",$(to_anglo "$latitude"),$(to_anglo "$longitude"),\"$stolen_location\",\"$url\",\"$year\"" >> $output_dir/anglo-saxon/$filename.csv

    # Output data to European CSV file
    echo "$date_stolen,\"$description\";\"$frame_colors\";\"$frame_model\";$id;\"$manufacturer_name\";$(to_european "$latitude");$(to_european "$longitude");\"$stolen_location\";\"$url\";\"$year\"" >> $output_dir/european/$filename.csv
  done
done

