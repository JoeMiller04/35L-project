const host = arguments[0];
const subjectCode = arguments[1];
const subjectFull = arguments[2];
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
            container_id: containerId
        };
        
        // Extract subject and catalog
        // This doesn't work.
        // const safeSubject = "{subjectCode}".replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
        // const re = new RegExp(`${{safeSubject}}(\\d+[A-Za-z]*)`);
        // const catalogMatch = containerId.match(re);

        // WE'RE HARDCODING THE SUBJECT CODE HERE
        const catalogMatch = containerId.match(/PHYSICS(\d+[A-Za-z]*)/);
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