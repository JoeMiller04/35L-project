import sys
import json
import re
from bs4 import BeautifulSoup
import pandas as pd

#This function Given a list of class names (e.g. ["Status_OK", ...]), returs "OK", "IP", "NO", or "NONE".
def _status(class_list):
    if not class_list:
        return "NONE"
    if "Status_OK" in class_list:
        return "OK"
    if "Status_IP" in class_list:
        return "IP"
    if "Status_NO" in class_list:
        return "NO"
    return "NONE"
#function reformats term, ex "FA22" to "22F"
def _reformat_term(term_raw: str) -> str:
 
    term_raw = term_raw.strip().upper()
    m = re.match(r"^([A-Z]{2})(\d{2})$", term_raw)
    if not m:
        return term_raw
    season_raw, year_raw = m.group(1), m.group(2)
    season_map = {
        "FA": "F",  # Fall
        "WI": "W",  # Winter
        "SP": "S",  # Spring
        "SU": "1",  # Summer
    }
    return f"{year_raw}{season_map.get(season_raw, season_raw)}"

# List of UCLA subject codes
UCLA_SUBJECTS = [
  "A&O SCI", "AERO ST", "AF AMER", "AM IND", "AN N EA", "ANTHRO", "APP CHM", "ARABIC",
  "ARCH&UD", "ARCHEOL", "ARMENIA", "ART", "ART HIS", "ART&ARC", "ARTS ED", "ASIA AM",
  "ASIAN", "ASL", "ASTR", "BIOENGR", "BIOINFO", "BIOL CH", "BIOMATH", "BIOSTAT",
  "BMD RES", "C&EE", "C&EE ST", "C&S BIO", "CCAS", "CESC", "CH ENGR", "CHEM", "CHIN",
  "CLASSIC",
  "CLUSTER",
  "COM HLT",
  "COM LIT",
  "COM SCI",
  "COMM",
  "COMPTNG",
  "CS",
  "DANCE",
  "DESMA",
  "DGT HUM",
  "DIS STD",
  "DS BMED",
  "DUTCH",
  "EA STDS",
  "EC ENGR",
  "ECON",
  "EDUC",
  "EE BIOL",
  "ELTS",
  "ENGCOMP",
  "ENGL",
  "ENGR",
  "ENV HLT",
  "ENVIRON",
  "EPIDEM",
  "EPS SCI",
  "ESL",
  "ETHNMUS",
  "FIAT LX",
  "FILIPNO",
  "FILM TV",
  "FOOD ST",
  "FRNCH",
  "GENDER",
  "GEOG",
  "GERMAN",
  "GJ STDS",
  "GLB HLT",
  "GLBL ST",
  "GRAD PD",
  "GREEK",
  "GRNTLGY",
  "HEBREW",
  "HIN-URD",
  "HIST",
  "HLT ADM",
  "HLT POL",
  "HNRS",
  "HUM GEN",
  "I A STD",
  "I E STD",
  "I M STD",
  "IL AMER",
  "INDO",
  "INF STD",
  "INTL DV",
  "IRANIAN",
  "ISLM ST",
  "ITALIAN",
  "JAPAN",
  "JEWISH",
  "KOREA",
  "LATIN",
  "LAW",
  "LBR STD",
  "LGBTQS",
  "LIFESCI",
  "LING",
  "M E STD",
  "M PHARM",
  "MAT SCI",
  "MATH",
  "MC&IP",
  "MCD BIO",
  "MECH&AE",
  "MED",
  "MED HIS",
  "MGMT",
  "MGMTEX",
  "MGMTFE",
  "MGMTFT",
  "MGMTGEX",
  "MGMTMFE",
  "MGMTMSA",
  "MGMTPHD",
  "MIL SCI",
  "MIMG",
  "MOL BIO",
  "MOL TOX",
  "MSC IND",
  "MUSC",
  "MUSCLG",
  "NAV SCI",
  "NEURBIO",
  "NEURLGY",
  "NEURO",
  "NEUROSC",
  "NR EAST",
  "NURSING",
  "OBGYN",
  "ORL BIO",
  "PATH",
  "PBMED",
  "PEDS",
  "PHILOS",
  "PHYSCI",
  "PHYSICS",
  "POL SCI",
  "PORTGSE",
  "PSYCH",
  "PSYCTRY",
  "PUB AFF",
  "PUB HLT",
  "PUB PLC",
  "QNT SCI",
  "RELIGN",
  "RES PRC",
  "ROMANIA",
  "RUSSN",
  "S ASIAN",
  "SCAND",
  "SCI EDU",
  "SEASIAN",
  "SEMITIC",
  "SLAVC",
  "SOC GEN",
  "SOC SC",
  "SOC WLF",
  "SOCIOL",
  "SPAN",
  "SRB CRO",
  "STATS",
  "SURGERY",
  "SWAHILI",
  "THAI",
  "THEATER",
  "TURKIC",
  "UG-LAW",
  "UKRN",
  "UNIV ST",
  "URBN PL",
  "VIETMSE",
  "WL ARTS",
  "YIDDSH"
]

#split a course code into (subject, catalog) by finding the boundary where digits begin
#If no digit‐prefix is found, fall back to splitting on the last space.
def _split_subject_catalog(code_raw: str) -> tuple[str, str]:
    code = code_raw.strip()
    
    # First try to match against known subjects
    for subject in sorted(UCLA_SUBJECTS, key=len, reverse=True):  # Try longest subjects first
        if code.upper().startswith(subject.upper()):
            # Found a matching subject, extract catalog
            catalog = code[len(subject):].strip()
            return subject, catalog
    
    # Fallback to original algorithm if no subject match found
    m = re.match(r"^(.+?)\s*([0-9].*)$", code)
    if m:
        subject = m.group(1).strip()
        catalog = m.group(2).strip()
        return subject, catalog
    
    parts = code.rsplit(" ", 1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    
    return "", code


"""
    Parse DARS HTML and return a dictionary with:
      - "requirements": a list of requirement objects (only those with >0‐unit courses).
      - "missing_requirements": a list of {code, title, status} for requirements not OK.
    Each requirement object includes:
      - code, title, status
      - sub: list of sub‐requirements containing ≥1 >0‐unit course
      - courses are deduped globally by (subject, catalog)
"""
def parse_dars(html_text: str) -> dict:
    
    soup = BeautifulSoup(html_text, "html.parser")

    req_map: dict[str, dict] = {}
    seen_courses_all: set[tuple[str, str]] = set()  

    for r in soup.select("div.requirement"):
        code = (r.get("rname") or "").strip()
        if not code:
            continue
        if code in req_map:
            continue

        h3 = r.select_one("h3.sr-only")
        title = h3.get_text(strip=True).replace("Requirement: ", "") if h3 else ""
        status = _status(r.get("class", []))

        req_record = {
            "code":   code,
            "title":  title,
            "status": status,
            "sub":    [],  
        }

        seen_sub_pseudos: set[str] = set()

        for s in r.select("div.subrequirement"):
            pseudo = (s.get("pseudo") or "").strip()
            if not pseudo or (pseudo in seen_sub_pseudos):
                continue
            seen_sub_pseudos.add(pseudo)

            
            sub_title_tag = s.select_one("span.subreqTitle")
            sub_title = sub_title_tag.get_text(strip=True) if sub_title_tag else ""
            status_tag = s.select_one("span.status")
            sub_status = _status(status_tag.get("class", [])) if status_tag else "NONE"

            sub_record = {
                "pseudo": pseudo,
                "title":  sub_title,
                "status": sub_status,
                "courses": []
            }

            seen_courses_in_sub: set[tuple[str, str]] = set()

            for row in s.select("tr.takenCourse, tr.takenCourse.ip"):
                td = row.find_all("td")
                term_raw   = td[0].get_text(strip=True) if len(td) > 0 else ""
                code_raw   = td[1].get_text(strip=True) if len(td) > 1 else ""
                units_text = td[2].get_text(strip=True) if len(td) > 2 else "0"
                grade      = td[3].get_text(strip=True) if len(td) > 3 else ""

                try:
                    units = float(units_text) if units_text else 0.0
                except ValueError:
                    units = 0.0

                # Skip any non‐academic (zero‐unit) courses
                if units <= 0.0:
                    continue

                term    = _reformat_term(term_raw)
                subject, catalog = _split_subject_catalog(code_raw)
                if not subject and not catalog:
                    continue  # skip if  couldn't parse a valid code

                course_status = "IP" if "ip" in row.get("class", []) else "OK"
                course_key = (subject.upper(), catalog.upper())

             
                #basically if the course is already in the list, skip it
                if course_key in seen_courses_all or course_key in seen_courses_in_sub:
                    continue

                seen_courses_all.add(course_key)
                seen_courses_in_sub.add(course_key)

                sub_record["courses"].append({
                    "term":    term,
                    "subject": subject,
                    "catalog": catalog,
                    "units":   units,
                    "grade":   grade,
                    "status":  course_status,
                })

            if sub_record["courses"]:
                req_record["sub"].append(sub_record)

        if req_record["sub"]:
            req_map[code] = req_record

    requirements = list(req_map.values())

    missing_requirements = [
        {"code": r["code"], "title": r["title"], "status": r["status"]}
        for r in requirements
        if r["status"] != "OK"
    ]

    return {
        "requirements": requirements,
        "missing_requirements": missing_requirements
    }

def main():
    # Ensure exactly one argument: path to DARS HTML
    if len(sys.argv) != 2:
        print("Usage: python3 dars_parser.py <path_to_dars_html_file>")
        sys.exit(1)

    html_path = sys.argv[1]
    try:
        with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
            html_text = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {html_path}")
        sys.exit(1)

    output = parse_dars(html_text)
    print(json.dumps(output, indent=2))

    all_courses = []

    # Loop through all requirements and sub-requirements to find courses
    for requirement in output.get('requirements', []):
        for subreq in requirement.get('sub', []):
            for course in subreq.get('courses', []):
                # Check if course status is "OK" or "IP"
                if course.get('status') in ['OK', 'IP']:
                    # Extract relevant information
                    course_info = {
                        'term': course.get('term'),
                        'subject': course.get('subject'),
                        'catalog': course.get('catalog'),
                        'units': course.get('units'),
                        'grade': course.get('grade'),
                        'status': course.get('status')
                    }
                    all_courses.append(course_info)

    df_courses = pd.DataFrame(all_courses)

    # Remove duplicate courses (some might appear in multiple requirements)
    df_courses = df_courses.drop_duplicates(subset=['term', 'subject', 'catalog'])

    # Sort by term for debugging purposes
    df_courses = df_courses.sort_values(['term', 'subject', 'catalog'], ascending=[False, True, True])

    # Print, for debugging
    print(f"Found {len(df_courses)} unique courses")
    print(df_courses)

    # Create a simplified JSON with just term, subject, and catalog
    simplified_courses = df_courses[['term', 'subject', 'catalog']].to_dict(orient='records')

    # Save simplified courses to JSON
    with open('courses_simple.json', 'w') as f:
        json.dump(simplified_courses, f, indent=2)

    print(f"Saved {len(simplified_courses)} courses to courses_simple.json")

if __name__ == "__main__":
    main()