from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re
import traceback

TERM = "25S"
SUBJECT = "COM SCI"

url = (
    "https://sa.ucla.edu/ro/public/soc/Results"
    f"?SubjectAreaName=Computer+Science+(COM+SCI)"
    f"&t={TERM}&sBy=subject&subj={SUBJECT.replace(' ', '+')}"
    "&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex"
)

opts = Options()
# opts.add_argument("--headless")
opts.add_argument("--window-size=1920,1080")
opts.add_argument("--disable-gpu")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")
opts.add_argument("--disable-extensions")
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=opts)

try:
    print(f"Navigating to {url}")
    driver.get(url)
    
    # Wait for page to load
    time.sleep(10)
    
    # The page usees something called a shadow DOM apparently
    host = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ucla-sa-soc-app"))
    )
    
    # Find and click expand all button within shadow DOM
    # Use JavaScript to access the shadow root and find the button
    js_click_expand = """
    const host = arguments[0];
    const shadowRoot = host.shadowRoot;
    const expandButton = shadowRoot.querySelector('#expandAll');
    if (expandButton) {
        expandButton.click();
        return true;
    }
    return false;
    """
    
    expand_clicked = driver.execute_script(js_click_expand, host)
    if expand_clicked:
        print("Clicked Expand All!")
    else:
        print("Could not find Expand All button")
    
    # Wait for the page to expand
    time.sleep(3)
    
    # Script to extract courses from current page
    js_extract_course_data = """
    const host = arguments[0];
    const shadowRoot = host.shadowRoot;
    const containers = Array.from(shadowRoot.querySelectorAll('[id$="-container"]'));
    
    // Extract course data from containers
    const courses = [];
    
    for (const container of containers) {
        try {
            const containerId = container.id || '';
            
            // Only process course containers
            if (!containerId.includes('COMSCI')) continue;
            
            const courseData = {
                container_id: containerId
            };
            
            // Extract subject and catalog
            const catalogMatch = containerId.match(/COMSCI(\d+[A-Za-z]*)/);
            if (catalogMatch) {
                courseData.subject = "COM SCI";
                courseData.catalog = catalogMatch[1];
                
                // Clean catalog (remove leading zeros)
                const cleanedCatalog = catalogMatch[1].replace(/^0+/, '');
                courseData.catalog_cleaned = cleanedCatalog;
                
                // Course code for finding related elements
                const courseCode = 'COMSCI' + catalogMatch[1];
                
                // Find title
                const titleElements = shadowRoot.querySelectorAll(`[id*="${courseCode}"][id*="title"]`);
                for (const elem of titleElements) {
                    if (elem.textContent && elem.textContent.trim()) {
                        courseData.title = elem.textContent.trim();
                        break;
                    }
                }
                
                // Find instructor
                const instructorElements = shadowRoot.querySelectorAll(`[id*="${courseCode}"][id*="instructor"]`);
                for (const elem of instructorElements) {
                    if (elem.textContent && elem.textContent.trim()) {
                        courseData.instructor = elem.textContent.trim();
                        break;
                    }
                }
                
                // Find meeting days
                const dayElements = shadowRoot.querySelectorAll(`[id*="${courseCode}"][id*="days"]`);
                for (const elem of dayElements) {
                    if (elem.textContent && elem.textContent.trim()) {
                        courseData.days = elem.textContent.trim();
                        break;
                    }
                }
                
                // Find meeting times
                const timeElements = shadowRoot.querySelectorAll(`[id*="${courseCode}"][id*="time"]`);
                for (const elem of timeElements) {
                    if (elem.textContent && elem.textContent.trim()) {
                        courseData.time = elem.textContent.trim();
                        break;
                    }
                }
                
                // Find location
                const locationElements = shadowRoot.querySelectorAll(`[id*="${courseCode}"][id*="location"]`);
                for (const elem of locationElements) {
                    if (elem.textContent && elem.textContent.trim()) {
                        courseData.location = elem.textContent.trim();
                        break;
                    }
                }
                
                // Only add if we have at least some data
                if (Object.keys(courseData).length > 1) {
                    courses.push(courseData);
                }
            }
        } catch (error) {
            console.error("Error processing container:", error);
        }
    }
    
    return courses;
    """
    
    # Execute script with host element as argument
    extracted_courses = driver.execute_script(js_extract_course_data, host)
    print(f"Extracted data for {len(extracted_courses)} courses")
    
    # Save the extracted data to a JSON file
    with open("courses_by_id.json", "w", encoding="utf-8") as f:
        json.dump(extracted_courses, f, indent=2)
    
    print(f"Saved {len(extracted_courses)} courses to courses_by_id.json")
    
except Exception as e:
    print(f"Error: {e}")
    print(traceback.format_exc())  # For debugging
    driver.save_screenshot("error_screenshot.png")
    
finally:
    driver.quit()
