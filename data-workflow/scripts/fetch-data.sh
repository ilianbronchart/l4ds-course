#!/bin/bash

# Set variables
API_URL="https://bikeindex.org:443/api/v3"
SEARCH_ENDPOINT="/search"
COUNT_ENDPOINT="/search/count"
PAGE="1"
PER_PAGE="100"
STOLENNESS="stolen"
JSON_DIR="../data" # TODO env var?
JSON_FILE="$JSON_DIR/bikes-$(date +%Y:%m:%d-%H:%M:%S).json"
DATE_THRESHOLD=$(date -u -d "-24 hours" +%s) # Bikes stolen in the last 24 hours

# Create the data directory if it does not exist
mkdir -p "$JSON_DIR"

# Fetch count data
COUNT=$(curl -s "$API_URL$COUNT_ENDPOINT?page=$PAGE&per_page=$PER_PAGE&stolenness=$STOLENNESS" | jq -r '.stolen')

# Calculate number of pages
PAGES=$((($COUNT + $PER_PAGE - 1) / $PER_PAGE))

# Initialize an empty array to store filtered data
FETCHED_DATA=[]

# Pages are sorted from newest to oldest
for ((i=1; i<=$PAGES; i++)); do
  # Fetch data
  DATA=$(curl -s "$API_URL$SEARCH_ENDPOINT?page=$i&per_page=$PER_PAGE&stolenness=$STOLENNESS")

  # Filter data by date_stolen
  FILTERED_DATA=$(echo "$DATA" | jq --argjson threshold "$DATE_THRESHOLD" '[.bikes[] | select(.date_stolen >= $threshold)]')  
  FETCHED_DATA=$(echo "$FETCHED_DATA $FILTERED_DATA" | jq -s '.[0] + .[1]')

  if [ $(echo "$FILTERED_DATA" | jq 'length') -eq 0 ]; then
    # No more items in filtered data. Breaking loop.
    break
  fi
done

# Write the full array to the file
echo "$FETCHED_DATA" | jq '.' > "$JSON_FILE"
# Set the file permissions to read-only
chmod 400 "$JSON_FILE"