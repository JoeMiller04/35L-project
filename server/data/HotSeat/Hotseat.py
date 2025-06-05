import json, re, requests
#test for example course 
COURSE_URL = "https://hotseat.io/courses/375542"   
html = requests.get(COURSE_URL, timeout=10).text

# 1. grab the JSON blob from the script tag
m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
data = json.loads(m.group(1))

# 2. Hotseat puts course info under props → pageProps
enroll = (data["props"]["pageProps"]
                ["initialEnrollment"])            # → {'current': 98,'capacity':100,'waitlist':5}

print(enroll["current"], "/", enroll["capacity"])