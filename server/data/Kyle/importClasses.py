from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re
import os
from pymongo import MongoClient
import json
from bson import json_util
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db["descriptions"]

options = Options()
options.add_argument('--headless')  # Run in headless mode (no window)
driver = webdriver.Chrome(options=options)

urls = [
    "https://registrar.ucla.edu/academics/course-descriptions?search=Aerospace+Studies", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=African+American+Studies",
    "https://registrar.ucla.edu/academics/course-descriptions?search=African+Studies", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=American+Indian+Studies", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=American+Sign+Language", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Ancient+Near+East", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Anesthesiology", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Anthropology", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Applied+Chemical+Sciences", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Applied+Linguistics", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Arabic", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Archaeology", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Architecture+and+Urban+Design", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Armenian", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Art", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Art+History", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Arts+and+Architecture", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Arts+Education", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Asian", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Asian+American+Studies", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Astronomy", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Atmospheric+and+Oceanic+Sciences", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Bioengineering", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Bioinformatics+(Graduate)", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Bioinformatics+(Undergraduate)", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Biological+Chemistry", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Biomathematics", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Biomedical+Research", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Biostatistics", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Bulgarian", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Central+and+East+European+Studies", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Chemical+Engineering", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Chemistry+and+Biochemistry", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Chicana%2Fo+and+Central+American+Studies", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Chinese", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Civil+and+Environmental+Engineering", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Classics", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Clusters", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Communication", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Community+Engagement+and+Social+Change", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Community+Health+Sciences", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Comparative+Literature", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Computational+and+Systems+Biology", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Computer+Science", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Conservation+of+Cultural+Heritage", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Czech", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Dance", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Data+Science+in+Biomedicine", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Dentistry", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Design+%2F+Media+Arts", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Digital+Humanities", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Disability+Studies", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Dutch", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Earth%2C+Planetary%2C+and+Space+Sciences", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=East+Asian+Studies", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Ecology+and+Evolutionary+Biology", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Economics", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Education", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Electrical+and+Computer+Engineering", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Engineering", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=English", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=English+as+A+Second+Language", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=English+Composition", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Environment", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Environmental+Health+Sciences", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Epidemiology", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Ethnomusicology", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=European+Languages+and+Transcultural+Studies", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Family+Medicine", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Fiat+Lux", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Filipino", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Film+and+Television", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Food+Studies", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=French", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Gender+Studies", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Geography", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=German", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Gerontology", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Global+Health", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Global+Jazz+Studies", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Global+Studies", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Graduate+Student+Professional+Development", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Greek", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Health+Policy+and+Management", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Healthcare+Administration", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Hebrew", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Hindi-Urdu", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=History", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Honors+Collegium", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Human+Genetics", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Hungarian", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Indigenous+Languages+of+the+Americas", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Indo-European+Studies", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Indonesian", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Information+Studies", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=International+and+Area+Studies", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=International+Development+Studies", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=International+Migration+Studies", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Iranian", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Islamic+Studies", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Italian", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Japanese", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Jewish+Studies", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Korean", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Labor+Studies", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Latin", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Latin+American+Studies", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Law", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Law+(Undergraduate)", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Lesbian%2C+Gay%2C+Bisexual%2C+Transgender%2C+and+Queer+Studies", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Life+Sciences", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Linguistics", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Lithuanian", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Management", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Management-Executive+MBA", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Management-Full-Time+MBA", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Management-Fully+Employed+MBA", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Management-Global+Executive+MBA+Asia+Pacific", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Management-Master+of+Financial+Engineering", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Management-Master+of+Science+in+Business+Analytics", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Management-PhD", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Materials+Science+and+Engineering", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Mathematics", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Mechanical+and+Aerospace+Engineering", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Medical+History", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Medicine", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Microbiology%2C+Immunology%2C+and+Molecular+Genetics", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Middle+Eastern+Studies", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Military+Science", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Molecular+and+Medical+Pharmacology", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Molecular+Biology", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Molecular+Toxicology", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Molecular%2C+Cell%2C+and+Developmental+Biology", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Molecular%2C+Cellular%2C+and+Integrative+Physiology", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Music", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Music+Industry", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Musicology", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Naval+Science", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Near+Eastern+Languages", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Neurobiology", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Neurology", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Neuroscience", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Neuroscience+(Graduate)", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Neurosurgery", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Nursing", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Obstetrics+and+Gynecology", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Ophthalmology", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Oral+Biology", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Orthopaedic+Surgery", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Pathology+and+Laboratory+Medicine", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Pediatrics", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Philosophy", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Physics", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Physics+and+Biology+in+Medicine", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Physiological+Science", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Physiology", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Polish", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Political+Science", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Portuguese", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Program+in+Computing", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Psychiatry+and+Biobehavioral+Sciences",
    "https://registrar.ucla.edu/academics/course-descriptions?search=Psychology", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Public+Affairs", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Public+Health", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Public+Policy", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Quantum+Science+and+Technology", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Radiation+Oncology", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Radiological+Science", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Religion%2C+Study+of", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Research+Practice", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Romanian", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Russian", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Scandinavian", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Science+Education", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Semitic", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Serbian%2FCroatian", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Slavic",
    "https://registrar.ucla.edu/academics/course-descriptions?search=Social+Science", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Social+Thought", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Social+Welfare", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Society+and+Genetics", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Sociology", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=South+Asian", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Southeast+Asian", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Spanish", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Statistics", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Surgery", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Swahili", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Thai", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Theater", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Turkic+Languages", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Ukrainian", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=University+Studies", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Urban+Planning", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Urology", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Vietnamese", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=World+Arts+and+Cultures", 
    "https://registrar.ucla.edu/academics/course-descriptions?search=Yiddish"
]


all_courses = []
added = 0
count = 0

for url in urls:
    driver.get(url)
    time.sleep(5)  # Wait for JS to load content

    html = driver.page_source
    with open('selenium_response_content.html', 'w', encoding='utf-8') as f:
        f.write(html)

    soup = BeautifulSoup(html, 'html.parser')
    # Extract department name from <h1> in <div id="block-ucla-sa-page-title">
    dept_div = soup.find('div', id='block-ucla-sa-page-title')
    dept_name = dept_div.find('h1').text.strip() if dept_div and dept_div.find('h1') else ''
    # Only keep the part inside parentheses, if present
    match = re.search(r'\(([^)]+)\)', dept_name)
    dept_name = match.group(1) if match else dept_name

    course_records = soup.find_all('div', class_='course-record')
    print(f"Found {len(course_records)} course records for department: {dept_name}.")

    for record in course_records:
        title_tag = record.find('h3')
        all_p = record.find_all('p')
        units = all_p[0].text.replace('Units:', '').strip() if all_p else ''
        description = all_p[1].text.strip() if len(all_p) > 1 else ''
        title = title_tag.text.strip() if title_tag else ''
        catalog = title.split('.', 1)[0]
        try:
            title = title.split(' ', 1)[1].strip() if '.' in title else title
        except IndexError:
            pass  # If split is out of range, keep title as is
        
        course_json = {
            'subject': dept_name,
            'catalog': catalog,
            'title': title,
            'units': units,
            'description': description
        }
        existing_course = collection.find_one({
            'subject': course_json['subject'],
            'catalog': course_json['catalog'],    
        })
        count += 1
        if not existing_course:
            result = collection.insert_one(course_json)
            added += 1

        all_courses.append(course_json)
        print(f"Scraped course: {dept_name} {title} {catalog}- {units} units")
print(f"Total courses scraped: {count}")
print(f"Total courses added: {added}")

# Save all courses to a JSON file as a backup
with open('scraped_courses.json', 'w', encoding='utf-8') as f:
    json.dump(all_courses, f, indent=2, ensure_ascii=False, default=json_util.default)
print(f"All courses saved to scraped_courses.json")
driver.quit()



