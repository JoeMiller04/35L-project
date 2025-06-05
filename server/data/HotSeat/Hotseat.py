import json, re, requests, datetime as dt

BASE = "https://hotseat.io"
UA   = {"User-Agent": "cs35l-hotseat-analyser/1.0 (+github.com/NETID)"}
SCRIPT_RE = re.compile(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.S)

def _next_data(url: str) -> dict:
    html = requests.get(url, headers=UA, timeout=15).text
    blob = SCRIPT_RE.search(html).group(1)
    return json.loads(blob)

def sections_for_course(course_id: int) -> list[dict]:
    data = _next_data(f"{BASE}/courses/{course_id}")
    return data["props"]["pageProps"]["sections"]          # list of section dicts

def load_series(section_id: int) -> tuple[list[tuple[dt.datetime,int]], int]:
    d = _next_data(f"{BASE}/sections/{section_id}")
    series  = d["props"]["pageProps"]["historicEnrollmentSeries"]
    capacity = d["props"]["pageProps"]["capacity"]
    # convert timestamp strings to datetime objects
    series  = [(dt.datetime.fromisoformat(ts.rstrip("Z")), cur) for ts, cur in series]
    return series, capacity

#attempt to load a section's historic enrollment series and capacity
#overall , I think due to the nature of the data being time dependent, it would be hard to stay updated
#HotSeat does not have a public API, so it would be hard to stay updated and even update the data
# this is a best effort attempt to load the data, but overall I woulve been able to get implemented if had a public API or more time 


#tasks to do:
# Map UCLA pass cut-off times to get the data for each enrolement period
# Compute metrics days_to_fill and pct_after_second_pass to see how long it takes to fill a section and how many students enroll after the second pass
# lastly after these we can pipeline and get all the courses and sections and their data
# format example: { "days_to_fill": 3,  "pct_after_second_pass": 94.0 },