#!/usr/bin/env python3
"""Pull per-measure participant counts for the ECHO de-identified release.

Uses the public PlatIPUS "Browse" page on ECHOPortal
(https://echoportal.org/Platipus/PCohorts/Index?pversion=DASH), which lists
every form / derived-variable file with the number of participants who have
data in the de-identified (DASH / AoU Workbench) release.

Output: raw/echo_platipus_counts.csv
Usage:  python3 survey-inventory/scripts/fetch_echo_counts.py
"""
import csv
import html
import http.cookiejar
import json
import pathlib
import re
import urllib.request

BASE = "https://echoportal.org/Platipus/PCohorts"
OUT = pathlib.Path(__file__).resolve().parent.parent / "raw" / "echo_platipus_counts.csv"

INPUT = re.compile(r'<input[^>]*class="faceted-browsing"[^>]*>')
ATTR = re.compile(r'([\w-]+)="([^"]*)"')


def main():
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    opener.addheaders = [("User-Agent", "Mozilla/5.0")]
    # The Browse page 500s without the public-session cookies these pages set.
    for warmup in ("https://echoportal.org/Users/PublicIndex",
                   "https://echoportal.org/Platipus/MainMenu/Index"):
        opener.open(warmup, timeout=120).read()
    page =opener.open(f"{BASE}/Index?pversion=DASH", timeout=120).read().decode("utf-8")
    counts = json.load(opener.open(
        f"{BASE}/changeParticipantCounts?measuresSelected=&version=any&level=both",
        timeout=120))
    by_id = {str(m["MeasureID"]): m["ParticipantCount"] for m in counts["measureCount"]}

    rows, seen = [], set()
    for tag in INPUT.findall(page):
        a = dict(ATTR.findall(tag))
        mid = a.get("data-measures", "")
        if not mid or mid in seen:
            continue
        seen.add(mid)
        rows.append([mid, a.get("shortName", ""), html.unescape(a.get("name", "")),
                     html.unescape(a.get("data-firstlabel", "")), by_id.get(mid, "")])
    with OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["platipus_measure_id", "short_name", "name", "group",
                    "n_participants"])
        w.writerows(rows)
    print(f"{OUT.name}: {len(rows)} measures; release total {counts['totalCount']:,} participants")


if __name__ == "__main__":
    main()
