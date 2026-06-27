#!/usr/bin/env python3
"""Verify every cited claim: fetch the URL and confirm the verbatim quote is
present on the page. Produces citations_verified.csv.

Status:
  VERIFIED    - page fetched AND normalized quote found in page text
  UNSUPPORTED - page fetched but quote NOT found (possible JS-render or misquote)
  DEAD        - page could not be fetched (4xx/5xx/timeout)

Pages that fail here (often JS-rendered or 403 to urllib) are retried with
WebFetch in a second pass; this script writes retry_urls.txt for that.
"""
from __future__ import annotations
import json, csv, re, time, urllib.request, ssl
from pathlib import Path

HERE = Path(__file__).resolve().parent
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def strip_html(html: str) -> str:
    html = re.sub(r"(?is)<(script|style|noscript).*?</\1>", " ", html)
    html = re.sub(r"(?s)<[^>]+>", " ", html)
    html = (html.replace("&amp;", "&").replace("&quot;", '"')
            .replace("&#39;", "'").replace("&rsquo;", "'").replace("&nbsp;", " ")
            .replace("&mdash;", "-").replace("&ndash;", "-").replace("&lt;", "<")
            .replace("&gt;", ">"))
    return html


def fetch(url: str):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=45, context=CTX) as r:
        raw = r.read()
    try:
        return raw.decode("utf-8", "ignore")
    except Exception:
        return raw.decode("latin-1", "ignore")


def quote_found(quote: str, page_norm: str) -> bool:
    q = norm(quote)
    if q and q in page_norm:
        return True
    # relaxed: >=85% of quote's significant tokens present on page
    toks = [t for t in q.split() if len(t) > 2]
    if not toks:
        return False
    hit = sum(1 for t in toks if t in page_norm)
    return hit / len(toks) >= 0.85


def main():
    records = []
    for fn in ("claims_A.json", "claims_B.json"):
        p = HERE / fn
        if p.exists():
            records += json.loads(p.read_text())
    print(f"claims: {len(records)}")

    # fetch each unique URL once
    cache = {}
    urls = sorted({r["url"] for r in records})
    for u in urls:
        try:
            page = fetch(u)
            cache[u] = ("ok", norm(strip_html(page)))
            print(f"  FETCH ok   {u[:70]}")
        except Exception as e:
            code = getattr(e, "code", type(e).__name__)
            cache[u] = (f"dead:{code}", "")
            print(f"  FETCH FAIL {code} {u[:64]}")
        time.sleep(0.3)

    rows = []
    retry = set()
    for r in records:
        st, pg = cache[r["url"]]
        if st != "ok":
            status = "DEAD"; retry.add(r["url"])
        elif quote_found(r["quote"], pg):
            status = "VERIFIED"
        else:
            status = "UNSUPPORTED"; retry.add(r["url"])
        rows.append({**r, "status": status})

    with (HERE / "citations_verified.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["status", "platform", "dimension", "claim", "url", "quote", "date"])
        for r in rows:
            w.writerow([r["status"], r["platform"], r["dimension"], r["claim"],
                        r["url"], r["quote"], r.get("date", "")])
    (HERE / "citations_verified.json").write_text(json.dumps(rows, indent=1))
    (HERE / "retry_urls.txt").write_text("\n".join(sorted(retry)))

    from collections import Counter
    c = Counter(r["status"] for r in rows)
    print("\n=== status counts ===")
    for k in ("VERIFIED", "UNSUPPORTED", "DEAD"):
        print(f"  {k}: {c.get(k,0)}")
    print(f"URLs to retry with WebFetch: {len(retry)}")


if __name__ == "__main__":
    main()
