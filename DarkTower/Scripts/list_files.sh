#!/bin/bash

# CONFIGURATION
BASE_URL="http://j4of6jujfkedi3u66xexwwdlssmdebcdyxjharcmfewvbimnmhgkbmqd.onion/data/ioausa" # You can change this part for the link that you are working with. This is an example of one that worked. 
SOCKS_PROXY="127.0.0.1:9050"  # Tor’s local SOCKS5 proxy
OUTPUT_FILE="all_links.txt"

# Prepare output
: > "$OUTPUT_FILE"

crawl_index() {
  local url="$1"
  echo "Crawling: $url/"

  # Try fetching the page (fail gracefully)
  local html
  if ! html=$(curl -s --proxy "socks5h://$SOCKS_PROXY" "$url/"); then
    echo "Failed to fetch $url/ – skipping" >&2
    return
  fi

  # Extract href="..." values (portable grep + sed)
  echo "$html" \
    | grep -oE 'href="[^"]+"' \
    | sed -e 's/^href="//' -e 's/"$//' \
    | while IFS= read -r link; do
        [[ "$link" == "../" ]] && continue

        if [[ "${link: -1}" == "/" ]]; then
          # Directory → recurse
          crawl_index "$url/${link%/}"
        else
          # File → record
          echo "$url/$link" >> "$OUTPUT_FILE"
        fi
      done
}

# Start crawling
crawl_index "$BASE_URL"

# Summary
echo "Done! $(wc -l < "$OUTPUT_FILE") links written to $OUTPUT_FILE"