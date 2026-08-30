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

RAW="$WORKDIR/ats_raw"
mkdir -p "$RAW"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
fetch(){ curl -sS -m 18 -A "$UA" -o "$1" -w "%{http_code} $1\n" "$2" 2>/dev/null || echo "FAIL $1"; }

rm -f "$RAW"/*.json "$RAW"/*.xml
while read -r line; do
  [ -z "$line" ] && continue
  case "$line" in \#*) continue ;; esac
  set -- $line
  case "$1" in
    gh) fetch "$RAW/gh_$2.json" "https://boards-api.greenhouse.io/v1/boards/$2/jobs?content=true&per_page=500" & ;;
    ab) fetch "$RAW/ab_$2.json" "https://api.ashbyhq.com/posting-api/job-board/$2?includeCompensation=true" & ;;
    lv) fetch "$RAW/lv_$2.json" "https://api.lever.co/v0/postings/$2?mode=json" & ;;
    pj) fetch "$RAW/pj_$2.xml" "https://$2.jobs.personio.de/xml" & ;;
    sr) fetch "$RAW/sr_${2}_0.json" "https://api.smartrecruiters.com/v1/companies/$2/postings?limit=100&offset=0" & ;;
    wd) tenant=$2; site=$3
        for q in "machine learning" "artificial intelligence" "generative ai"; do
          fq=$(echo "$q" | tr ' ' '_')
          curl -sS -m 20 -A "$UA" -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' \
            -d "{\"appliedFacets\":{},\"limit\":20,\"offset\":0,\"searchText\":\"$q\"}" \
            -o "$RAW/wd_${tenant}_${site}_${fq}.json" -w "%{http_code} wd_${tenant}_${site}_${fq}\n" \
            "https://$tenant.wd3.myworkdayjobs.com/wday/cxs/$tenant/$site/jobs" 2>/dev/null || echo "FAIL wd_${tenant}_${site}_${fq}" &
        done ;;
  esac
done < "$BOARDS"

for page in 1 2 3 4 5 6 7 8 9 10; do
  fetch "$RAW/an_$page.json" "https://www.arbeitnow.com/api/job-board-api?location=$COUNTRY_QUERY&page=$page" &
done
for keyword in "AI" "machine learning" "LLM" "GenAI" "data scientist"; do
  keyword_file=$(echo "$keyword" | tr ' ' '_')
  fetch "$RAW/an_kw_${keyword_file}_1.json" "https://www.arbeitnow.com/api/job-board-api?location=$COUNTRY_QUERY&search=$keyword&page=1" &
  fetch "$RAW/an_kw_${keyword_file}_2.json" "https://www.arbeitnow.com/api/job-board-api?location=$COUNTRY_QUERY&search=$keyword&page=2" &
done
fetch "$RAW/ro.json" "https://remoteok.com/api" &
wait
echo "ALL_DONE config_dir=${CONFIG_DIR:-skill-defaults} country=$COUNTRY_QUERY raw=$RAW"
