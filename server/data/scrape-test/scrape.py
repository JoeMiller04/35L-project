from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
import time
import json
import re
import traceback




opts = Options()
# Should work headless or not, but headless is faster
# # If you want to see the browser, comment out the next line
# CURRENTLY CRASHES IN HEADLESS MODE
# opts.add_argument("--headless")
opts.add_argument("--window-size=1920,1080")
opts.add_argument("--disable-gpu")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")
opts.add_argument("--disable-extensions")
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=opts)
wait = WebDriverWait(driver, 15)

def getHost():
    # The page usees something called a shadow DOM apparently
    host = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ucla-sa-soc-app"))
    )
    return host

def shadow_root():
    host = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "ucla-sa-soc-app")))
    return host.shadow_root        

def clickExpandAll(host):
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
        time.sleep(10)  # Wait for the page to expand
    else:
        print("Could not find Expand All button")


def go_next_page() -> bool:
    """
    Click the numbered paginator button for (current_page + 1).
    Returns True if we really advanced, False when already on last page.
    """
    # Get the current page number from the paginator
    cur_page = driver.execute_script(
        'return parseInt(document.querySelector("ucla-sa-soc-app")'
        '.shadowRoot.querySelector(".jPag-current").textContent, 10);')

    # Find the paginator button for the next page
    clicked = driver.execute_script(
        '''
        const host = document.querySelector('ucla-sa-soc-app');
        const root = host.shadowRoot;
        const target = [...root.querySelectorAll('.jPag-pages button')]
                       .find(b => parseInt(b.textContent.trim(), 10) === arguments[0]);
        if (!target) return false;        // already on last page
        target.scrollIntoView({block:'center'});
        target.click();
        return true;
        ''',
        cur_page + 1
    )
    if not clicked:
        return False # No next page button found, already on last page                     

    # Wait for the page to advance
    def page_has_advanced(_):
        try:
            host = driver.find_element(By.CSS_SELECTOR, 'ucla-sa-soc-app')
            new_pg = int(driver.execute_script(
                'return arguments[0].shadowRoot.querySelector(".jPag-current").textContent;',
                host))
            return new_pg == cur_page + 1
        except StaleElementReferenceException:
            return False

    try:
        wait.until(page_has_advanced)
        return True
    except TimeoutException:
        return False


def extractPageInfo(filename="courses_by_id.json", all_courses=None, subject="COM SCI", term="24S"):
    """
    Extract course data from current page
    
    Parameters:
    - filename: where to save this page's data
    - all_courses: list to append this page's courses to (for combined output)
    - subject: the subject being scraped (e.g., "COM SCI", "PHYSICS")
    - term: the term being scraped (e.g., "24S", "25W")
    
    Returns:
    - List of extracted courses from this page
    """
    # Convert subject to the format used in container IDs (no spaces, uppercase)
    # I can't guarantee that this works for all subjects, but it usually does
    subject_code = subject.replace(" ", "").upper()
    
    # Script to extract courses from current page
    js_extract_course_data = """
    const host = arguments[0];
    const subjectCode = arguments[1];
    const subjectFull = arguments[2];
    const term = arguments[3];
    const shadowRoot = host.shadowRoot;
    const containers = Array.from(shadowRoot.querySelectorAll('[id$="-container"]'));
    
    // Extract course data from containers
    const courses = [];
    
    for (const container of containers) {
        try {
            const containerId = container.id || '';
            
            // Only process containers for the specified subject
            if (!containerId.includes(subjectCode)) continue;
            
            const courseData = {
                container_id: containerId,
                term: term  
            };
            
            // Extract subject and catalog
            const catalogMatch = containerId.match(/"""+subject_code+"""(\d+[A-Za-z]*)/);
            if (catalogMatch) {
                courseData.subject = subjectFull;
                courseData.catalog = catalogMatch[1];
                
                // Clean catalog (remove leading zeros)
                const cleanedCatalog = catalogMatch[1].replace(/^0+/, '');
                courseData.catalog_cleaned = cleanedCatalog;
                
                // Course code for finding related elements
                const courseCode = subjectCode + catalogMatch[1];
                
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
    
    # Execute script with host element as argument, passing the subject code and full subject name
    extracted_courses = driver.execute_script(js_extract_course_data, host, subject_code, subject, term)
    # with open('extract_data.js') as f:
    #     script = f.read()
    # extracted_courses = driver.execute_script(script, getHost(), subject_code, subject)
    print(f"Extracted data for {len(extracted_courses)} courses")
    
    # Save the extracted data to a JSON file (for backup)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(extracted_courses, f, indent=2)
    
    print(f"Saved {len(extracted_courses)} courses to {filename}")
    
    if len(extracted_courses) == 0:
        print(f"WARNING: No courses found on this page for subject {subject}!")
        driver.save_screenshot(f"no_courses_found_{subject.replace(' ', '_')}.png")
    
    # If all_courses list is provided, append these courses to it
    if all_courses is not None:
        all_courses.extend(extracted_courses)
    
    return extracted_courses


try:
    """
    Main script to scrape course data from UCLA's Schedule of Classes
    save to individual JSON files and a combined file.
    For some reason, every course gets duplicated, but we can process
    that as we upload to MongoDB.
    """
    # PARAMETERS
    TERMS = ["25S"]
    # SUBJECTS NEED TO BE HARDCODED IN EXTRACT_DATA.JS
    # SO YOU ONLY CAN RUN ONE AT A TIME FOR NOW (sob)
    SUBJECTS = ["PHYSICS", "COM SCI"]

    # Track total courses added across all pages
    total_added = 0
    total_skipped = 0
    total_pages = 0

    all_courses = []

    # Output file for combined data
    combined_output_file = f"all_courses.json"
    for TERM in TERMS:
        for SUBJECT in SUBJECTS:

            page_num = 1
            
            # List to collect all courses across all pages

            url = (
            "https://sa.ucla.edu/ro/public/soc/Results"
            f"?t={TERM}&sBy=subject&subj={SUBJECT.replace(' ', '+')}"
            "&catlg=&cls_no=&undefined=Go&btnIsInIndex=btn_inIndex"
            )

            # print(f"Navigating to {url}")
            driver.get(url)
            
            print("Heads up that course counts are probably off by a factor of 2")
            # Wait for page to load
            time.sleep(10)
            host = getHost()
            
            repeat = True
            while repeat:
                total_pages += 1
                print(f"Processing courses for {TERM} - {SUBJECT} (Page {page_num})")
                clickExpandAll(host)
                
                # Pass the all_courses list to append this page's courses
                courses = extractPageInfo(f"courses_term_{TERM}_subject_{SUBJECT.replace(' ', '_')}_page_{page_num}.json", all_courses, subject=SUBJECT, term=TERM)
                total_added += len(courses)
                
                # Try to go to the next page
                repeat = go_next_page()
                if repeat:
                    page_num += 1
                    # Wait for the new page to load
                    time.sleep(5)
    
    # Save combined courses to a single file
    print(f"\nSaving {len(all_courses)} total courses to {combined_output_file}")
    with open(combined_output_file, "w", encoding="utf-8") as f:
        json.dump(all_courses, f, indent=2)
    
    print(f"\nScraping completed: processed {total_pages} pages with {total_added} total courses")

except Exception as e:
    print(f"Error: {e}")
    print(traceback.format_exc())  # For debugging
    driver.save_screenshot("error_screenshot.png")
    
    # Try to save any collected courses even if there was an error
    if 'all_courses' in locals() and all_courses:
        emergency_file = f"emergency_save_{TERM}_{SUBJECT.replace(' ', '_')}.json"
        print(f"Saving {len(all_courses)} courses collected so far to {emergency_file}")
        with open(emergency_file, "w", encoding="utf-8") as f:
            json.dump(all_courses, f, indent=2)
    
finally:
    driver.quit()
