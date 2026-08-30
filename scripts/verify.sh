#!/bin/bash
# job-search-de: verify posting URLs -> title / datePosted / datePublished / validThrough / http code
# Usage: scripts/verify.sh urls.txt   (one URL per line)
while IFS= read -r u; do
  [ -z "$u" ] && continue
  f=$(mktemp)
  code=$(curl -sS -m 18 -L -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36" -o "$f" -w "%{http_code}" "$u" 2>/dev/null)
  t=$(grep -o '<title>[^<]*' "$f" 2>/dev/null | head -1 | sed 's/<title>//')
  d=$(grep -oE '"datePosted"[^,}]{0,42}|datePosted[^,}<]{0,42}' "$f" 2>/dev/null | head -1)
  d2=$(grep -oE '"datePublished"[^,}]{0,42}' "$f" 2>/dev/null | head -1)
  vt=$(grep -oE '"validThrough"[^,}]{0,42}' "$f" 2>/dev/null | head -1)
  echo "[$code] $d $d2 $vt :: $(echo "$t" | head -c 60) :: $u"
  rm -f "$f"
done < "$1"
