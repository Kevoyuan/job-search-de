#!/bin/bash
# Download ATS payloads using project-level .job-search overrides when present.
# Usage: download.sh [--workdir DIR] [--config-dir DIR]
set -u

SKILL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORKDIR="."
CONFIG_DIR=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --workdir) WORKDIR="$2"; shift 2 ;;
    --config-dir) CONFIG_DIR="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

WORKDIR="$(cd "$WORKDIR" && pwd)"
if [ -z "$CONFIG_DIR" ] && [ -d "$WORKDIR/.job-search" ]; then
  CONFIG_DIR="$WORKDIR/.job-search"
fi

BOARDS="$SKILL_ROOT/configs/boards.txt"
SETTINGS=""
if [ -n "$CONFIG_DIR" ]; then
  CONFIG_DIR="$(cd "$CONFIG_DIR" && pwd)"
  [ -f "$CONFIG_DIR/boards.txt" ] && BOARDS="$CONFIG_DIR/boards.txt"
  [ -f "$CONFIG_DIR/settings.ini" ] && SETTINGS="$CONFIG_DIR/settings.ini"
fi

COUNTRY_QUERY="germany"
if [ -n "$SETTINGS" ]; then
  configured_country="$(sed -n 's/^[[:space:]]*country_query[[:space:]]*=[[:space:]]*//p' "$SETTINGS" | head -1)"
  [ -n "$configured_country" ] && COUNTRY_QUERY="$configured_country"
fi

# Concurrency worker pool configuration (default: 8 parallel downloads)
MAX_PARALLEL="${GSTACK_DOWNLOAD_CONCURRENCY:-8}"
run_parallel() {
  while [ "$(jobs -p 2>/dev/null | wc -l)" -ge "$MAX_PARALLEL" ]; do
    sleep 0.05
  done
  "$@" &
}

# Resolve target search keywords dynamically from project or skill keywords
KEYWORDS_FILE=""
if [ -n "$CONFIG_DIR" ] && [ -f "$CONFIG_DIR/keywords.txt" ]; then
  KEYWORDS_FILE="$CONFIG_DIR/keywords.txt"
elif [ -f "$SKILL_ROOT/configs/keywords.txt" ]; then
  KEYWORDS_FILE="$SKILL_ROOT/configs/keywords.txt"
fi

SEARCH_KEYWORDS=()
if [ -n "$KEYWORDS_FILE" ]; then
  strong_line="$(sed -n 's/^[[:space:]]*STRONG:[[:space:]]*//p' "$KEYWORDS_FILE" | head -1)"
  if [ -n "$strong_line" ]; then
    IFS=',' read -ra ADDR <<< "$strong_line"
    count=0
    for kw in "${ADDR[@]}"; do
      kw_clean="$(echo "$kw" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
      if [ -n "$kw_clean" ] && [ "$count" -lt 5 ]; then
        SEARCH_KEYWORDS+=("$kw_clean")
        count=$((count + 1))
      fi
    done
  fi
fi

if [ ${#SEARCH_KEYWORDS[@]} -eq 0 ]; then
  SEARCH_KEYWORDS=("machine learning" "artificial intelligence" "generative ai" "data scientist")
fi

RAW="$WORKDIR/ats_raw"
mkdir -p "$RAW"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
fetch(){ curl -sS -m 18 -A "$UA" -o "$1" -w "%{http_code} $1\n" "$2" 2>/dev/null || echo "FAIL $1"; }

fetch_wd() {
  local tenant="$1" site="$2" q="$3" out="$4"
  curl -sS -m 20 -A "$UA" -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' \
    -d "{\"appliedFacets\":{},\"limit\":20,\"offset\":0,\"searchText\":\"$q\"}" \
    -o "$out" -w "%{http_code} $(basename "$out")\n" \
    "https://$tenant.wd3.myworkdayjobs.com/wday/cxs/$tenant/$site/jobs" 2>/dev/null || echo "FAIL $(basename "$out")"
}

rm -f "$RAW"/*.json "$RAW"/*.xml
while read -r line; do
  [ -z "$line" ] && continue
  case "$line" in \#*) continue ;; esac
  set -- $line
  case "$1" in
    gh) run_parallel fetch "$RAW/gh_$2.json" "https://boards-api.greenhouse.io/v1/boards/$2/jobs?content=true&per_page=500" ;;
    ab) run_parallel fetch "$RAW/ab_$2.json" "https://api.ashbyhq.com/posting-api/job-board/$2?includeCompensation=true" ;;
    lv) run_parallel fetch "$RAW/lv_$2.json" "https://api.lever.co/v0/postings/$2?mode=json" ;;
    pj) run_parallel fetch "$RAW/pj_$2.xml" "https://$2.jobs.personio.de/xml" ;;
    sr) run_parallel fetch "$RAW/sr_${2}_0.json" "https://api.smartrecruiters.com/v1/companies/$2/postings?limit=100&offset=0" ;;
    wd) tenant=$2; site=$3
        for q in "${SEARCH_KEYWORDS[@]}"; do
          fq=$(echo "$q" | tr ' ' '_')
          run_parallel fetch_wd "$tenant" "$site" "$q" "$RAW/wd_${tenant}_${site}_${fq}.json"
        done ;;
  esac
done < "$BOARDS"

for page in 1 2 3 4 5 6 7 8 9 10; do
  run_parallel fetch "$RAW/an_$page.json" "https://www.arbeitnow.com/api/job-board-api?location=$COUNTRY_QUERY&page=$page"
done

for keyword in "${SEARCH_KEYWORDS[@]}"; do
  keyword_file=$(echo "$keyword" | tr ' ' '_')
  run_parallel fetch "$RAW/an_kw_${keyword_file}_1.json" "https://www.arbeitnow.com/api/job-board-api?location=$COUNTRY_QUERY&search=$keyword&page=1"
  run_parallel fetch "$RAW/an_kw_${keyword_file}_2.json" "https://www.arbeitnow.com/api/job-board-api?location=$COUNTRY_QUERY&search=$keyword&page=2"
done

run_parallel fetch "$RAW/ro.json" "https://remoteok.com/api"
wait
echo "ALL_DONE config_dir=${CONFIG_DIR:-skill-defaults} country=$COUNTRY_QUERY concurrency=$MAX_PARALLEL raw=$RAW"
