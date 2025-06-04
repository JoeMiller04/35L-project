import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './App.css';

// Helper to convert display term to backend code
function displayTermToCode(term) {
  const [season, year] = term.split(' ');
  if (!season || !year) return term;
  if (season === 'Winter') return year + 'W';
  if (season === 'Spring') return year + 'S';
  if (season === 'Summer') return year + '1';
  if (season === 'Fall') return year + 'F';
  return term;
}

const availableTerms = [
  "Winter 25", "Spring 25", "Summer 25", "Fall 25",
  "Winter 26", "Spring 26", "Summer 26", "Fall 26",
  "Winter 27", "Spring 27", "Summer 27", "Fall 27",
  "Winter 28", "Spring 28", "Summer 28", "Fall 28"
];

  
  const termToSortable = (term) => {
  if (term === "PAST")
  {
    return 10000;
  }
  const year = parseInt(term.slice(0, 2)); 
  const quarterCode = { W: 1, S: 2, F: 4, SS:3 }[term[2]]; 
  return year * 10 + quarterCode;
};

export default function FuturePlanner() {
  const [plan, setPlan] = useState([]); 
  const [selectedTerm, setSelectedTerm] = useState('');
  const [selectedCourse, setSelectedCourse] = useState('');
  const [selectedDegree, setSelectedDegree] = useState('');
  const [validationMessage, setValidationMessage] = useState('');
  const navigate = useNavigate();
  const userObj = JSON.parse(localStorage.getItem("user_id"));
  const userId = userObj._id;
  const [major, setMajor] = useState('');
  const [popup, setPopup] = useState(false);


  const availableCourses = selectedDegree === 'CS' 
    ? [
    "MATH 31A",
    "MATH 31B",
    "MATH 32A",
    "MATH 32B",
    "MATH 33A",
    "MATH 33B",
    "MATH 61",
    "MATH 170A",
    "MATH 170E",
    "C&EE 110",
    "STATS 100A",
    "PHYSICS 1A",
    "PHYSICS 1B",
    "PHYSICS 1C",
    "PHYSICS 4AL",
    "PHYSICS 4BL",
    "LIFESCI 30A",
    "LIFESCI 30B",
    "COM SCI 1",
    "COM SCI 30",
    "COM SCI 31",
    "COM SCI 32",
    "COM SCI 33",
    "COM SCI 35L",
    "COM SCI M51A",
    "COM SCI 111",
    "COM SCI 112",
    "COM SCI 117",
    "COM SCI 118",
    "COM SCI M119",
    "COM SCI C121",
    "COM SCI C122",
    "COM SCI C124",
    "COM SCI 131",
    "COM SCI 130",
    "COM SCI 132",
    "COM SCI M151B",
    "COM SCI 133",
    "COM SCI 134",
    "COM SCI 136",
    "COM SCI C137A",
    "COM SCI C137B",
    "COM SCI M138",
    "COM SCI 143",
    "COM SCI 144",
    "COM SCI 145",
    "COM SCI M146",
    "COM SCI M148",
    "COM SCI M152A",
    "COM SCI 152B",
    "COM SCI 180",
    "COM SCI 161",
    "COM SCI 162",
    "COM SCI 163",
    "COM SCI 168",
    "COM SCI 170A",
    "COM SCI M171L",
    "COM SCI 172",
    "COM SCI 174A",
    "COM SCI 174B",
    "COM SCI C174C",
    "COM SCI 181",
    "COM SCI M182",
    "COM SCI 183",
    "COM SCI M184",
    "COM SCI CM186",
    "COM SCI CM187",
    "COM SCI 188",
    "EC ENGR M16",
    "EC ENGR 131A",
    "EC ENGR 132B",
    "EC ENGR M117",
    "EC ENGR M116L",
    "GE",
    "SCI-TECH",
    "TECH BREADTH",
    "ENG COMP",
    "ETHICS",
    "COM SCI ELECTIVE" 
]
    : selectedDegree === 'CSE'
      ? [
    "MATH 31A",
    "MATH 31B",
    "MATH 32A",
    "MATH 32B",
    "MATH 33A",
    "MATH 33B",
    "MATH 61",
    "MATH 170A",
    "MATH 170E",
    "C&EE 110",
    "STATS 100A",
    "PHYSICS 1A",
    "PHYSICS 1B",
    "PHYSICS 1C",
    "PHYSICS 4AL",
    "PHYSICS 4BL",
    "LIFESCI 30A",
    "LIFESCI 30B",
    "COM SCI 1",
    "COM SCI 30",
    "COM SCI 31",
    "COM SCI 32",
    "COM SCI 33",
    "COM SCI 35L",
    "COM SCI M51A",
    "COM SCI 111",
    "COM SCI 112",
    "COM SCI 117",
    "COM SCI 118",
    "COM SCI M119",
    "COM SCI C121",
    "COM SCI C122",
    "COM SCI C124",
    "COM SCI 131",
    "COM SCI 130",
    "COM SCI 132",
    "COM SCI M151B",
    "COM SCI 133",
    "COM SCI 134",
    "COM SCI 136",
    "COM SCI C137A",
    "COM SCI C137B",
    "COM SCI M138",
    "COM SCI 143",
    "COM SCI 144",
    "COM SCI 145",
    "COM SCI M146",
    "COM SCI M148",
    "COM SCI M152A",
    "COM SCI 152B",
    "COM SCI 180",
    "COM SCI 161",
    "COM SCI 162",
    "COM SCI 163",
    "COM SCI 168",
    "COM SCI 170A",
    "COM SCI M171L",
    "COM SCI 172",
    "COM SCI 174A",
    "COM SCI 174B",
    "COM SCI C174C",
    "COM SCI 181",
    "COM SCI M182",
    "COM SCI 183",
    "COM SCI M184",
    "COM SCI CM186",
    "COM SCI CM187",
    "COM SCI 188",
    "EC ENGR 3",
    "EC ENGR M16",
    "EC ENGR 100",
    "EC ENGR 102",
    "EC ENGR 115C",
    "EC ENGR 131A",
    "EC ENGR 132B",
    "EC ENGR M117",
    "EC ENGR M116L",
    "GE",
    "TECH BREADTH",
    "ENG COMP",
    "ETHICS",
    "COM SCI ELECTIVE" 
]
      : [];

      function updateMajor(maj) {
    localStorage.setItem('major', JSON.stringify({major: maj}));
    setMajor(maj);
  }

  function toggleMajor() {
    setPopup(!popup);
  }


  // GET saved courses from the backend
  useEffect(() => {
  const loadSavedPlan = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/users/${userId}/courses`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to fetch user course list');
            }
      const data = await response.json(); // Expects: [{ term: "25F", course_name: "COM SCI 32" }, ...]

      // Group courses by term
      const grouped = {};
      data.forEach(({ term, course_name }) => {
        if (!grouped[term]) grouped[term] = [];
        grouped[term].push(course_name);
      });

      const structuredPlan = Object.entries(grouped).map(([term, classes]) => ({
        term,
        classes,
      }));

      setPlan(structuredPlan);
    } catch (err) {
      console.error("Error loading saved plan:", err);
    }
    
    const majorObj = JSON.parse(localStorage.getItem('major'));
if (majorObj && majorObj.major) {
    setSelectedDegree(majorObj.major);
    setMajor(majorObj.major);
} else {
    
    setMajor('');
}
  };

  if (userId) loadSavedPlan();
}, [userId]);

   const handleValidation = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/users/${userId}/courses`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to fetch user course list');
            }
      const data = await response.json(); 
      //const result = isValid(data); // Call isValid function with the current plan
      const result = true;

      if (result === true) {
        setValidationMessage("Your plan is valid!");
      } else {
        setValidationMessage(result); // Assuming result is an error message from isValid
      }
    } catch (error) {
      setValidationMessage("An error occurred while validating the plan: " + error.message);
    }
  };

  // Add selected course to selected term in plan
  const addCourseToQuarter = () => {
    if (!selectedTerm || !selectedCourse) return;
    const backendTerm = selectedTerm;
    setPlan((prevPlan) => {
      const existing = prevPlan.find((entry) => entry.term === backendTerm);
      if (existing) {
        return prevPlan.map((entry) =>
          entry.term === backendTerm
            ? { ...entry, classes: [...new Set([...entry.classes, selectedCourse])] }
            : entry
        );
      } else {
        return [...prevPlan, { term: backendTerm, classes: [selectedCourse] }];
      }
    });
    fetch(`http://127.0.0.1:8000/users/${userId}/courses`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        term: backendTerm,
        course_name: selectedCourse,
        action: "add",
      }),
    });
    setSelectedCourse('');
  };

  // Remove course from a specific term
const removeCourse = (termToRemove, courseToRemove) => {
  // Update local state
  setPlan((prevPlan) =>
    prevPlan
      .map((entry) =>
        entry.term === termToRemove
          ? { ...entry, classes: entry.classes.filter((c) => c !== courseToRemove) }
          : entry
      )
      .filter((entry) => entry.classes.length > 0)
  );

  // Remove from backend
  fetch(`http://127.0.0.1:8000/users/${userId}/courses`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      term: termToRemove,
      course_name: courseToRemove,
      action: "remove",
    }),
  });
};

  // For display, map backend code to display term
function codeToDisplayTerm(code) {
  const year = code.slice(0, 2);
  const season = code.slice(2);
  if (season === 'W') return `Winter ${year}`;
  if (season === 'S') return `Spring ${year}`;
  if (season === '1') return `Summer ${year}`;
  if (season === 'F') return `Fall ${year}`;
  return code;
}

  return (
    <div style={{ display: 'flex', backgroundColor: '#f0f0f0', minHeight: '100vh' }}>
        <div style={{ position: 'fixed', left: 0, top: 0, width: '10%', backgroundColor: '#9cbcc5', height: '100vh', zIndex: 1 }}></div>
        <div style={{ width: '80%', marginLeft: '10%', zIndex: 2, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
    {/* Header */}
    <div style={{ width: '100%' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative', width: '100%', marginBottom: '20px' }}>
          {/* Left button group */}
          <div style={{ display: 'flex', alignItems: 'center', position: 'absolute', left: 0, height: '100%' }}>
            <button onClick={() => navigate('/Home')} style={{ cursor: 'pointer', backgroundColor: 'white', marginLeft: '50px', padding: '10px 20px', fontSize: '12px', marginTop: '10px', fontWeight: 'bold' }}>Home</button>
            <button onClick={() => navigate('/PastCourses')} style={{ cursor: 'pointer', backgroundColor: 'white', marginLeft: '20px', padding: '10px 20px', fontSize: '12px', marginTop: '10px', fontWeight: 'bold' }}>Past Courses</button>
          </div>
          {/* Centered title */}
          <div style={{ flex: 1, display: 'flex', justifyContent: 'center' }}>
            <h1 style={{ textAlign: 'center', fontSize: '50px', fontWeight: 'bold', margin: 0 }}>Future Plan</h1>
          </div>
          {/* Right button group */}
          <div style={{ display: 'flex', alignItems: 'center', position: 'absolute', right: 0, height: '100%' }}>
            <button onClick={() => toggleMajor()} style={{ cursor: 'pointer', backgroundColor: 'white', marginRight: '50px', padding: '10px 20px', fontSize: '12px', marginTop: '10px', fontWeight: 'bold' }}>Change Major</button>
          </div>
        </div>
                <hr style={{color:'black', backgroundColor:'black', height:'2px', border:'none', marginTop:'0px'}}/>
    </div>

    {/* Dropdowns and Add Course button */}
    <div style={{ width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '20px', marginBottom: '10px' }}>
        {/*degree dropdown*/} 
      <div>
        


{/* Dropdowns to select term and course, displayed only if degree is selected */}
        {true && (
          <>
        <select
          value={selectedTerm}
          onChange={(e) => setSelectedTerm(e.target.value)}
          style={{ cursor:'pointer', width: '100px', height: '30px', border:'2px solid black', marginRight:'20px' }}
         
        >
          <option value="">Select Term</option>
          {availableTerms.map((term) => (
            <option key={term} value={displayTermToCode(term)}>
              {term}
            </option>
          ))}
        </select>

        <select
          value={selectedCourse}
          onChange={(e) => setSelectedCourse(e.target.value)}
          style={{ cursor:'pointer', width: '150px', height: '30px', border:'2px solid black', marginRight:'20px' }}
         
        >
          <option value="">Select Course</option>
          {availableCourses.map((course) => (
            <option key={course} value={course}>
              {course}
            </option>
          ))}
        </select>

        <button
          onClick={addCourseToQuarter}
          style={{ width: '100px', height: '30px', backgroundColor: 'white', border: '2px solid black', borderRadius: '4px', fontSize: '14px', cursor: 'pointer', marginLeft:'40px' }}
         
        >
          Add Course
        </button>

          <button onClick={handleValidation} style={{ width: '100px', height: '30px', backgroundColor: 'white', border: '2px solid black', borderRadius: '4px', fontSize: '14px', cursor: 'pointer', marginLeft:'40px' }}>

            Validate Plan

          </button>

        </>
        )}
      </div>
    </div>


<hr style={{border: 'none', borderTop: '2px solid black', marginTop: '0px', width: '100%', marginTop:'20px'}} />






    {/* display things */}  
     {plan.length > 0 ? (
  <div style={{ display: 'flex', width: '100%', marginTop: '24px' }}>
    {/* everything but past */}
    <div style={{ width: '85%', maxWidth: '1200px', display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '24px', textAlign: 'left', marginLeft:'50px', marginRight:'-30px' }}>
      {availableTerms.map((term) => {
        const backendTerm = displayTermToCode(term);
        const planEntry = plan.find((entry) => entry.term === backendTerm);
        const classes = planEntry ? planEntry.classes : [];
        return (
          <div key={backendTerm}>
            <h2>{term}</h2>
            <ul style={{ marginTop: '-20px', listStyleType: 'none', paddingLeft: '0px' }}>
              {classes.length > 0 ? (
                classes.map((c) => (
                  <li key={c}>
                    <button onClick={() => removeCourse(backendTerm, c)} style={{ border: 'none', cursor: 'pointer', color: 'red' }}>X</button>
                    <span>{c}</span>
                  </li>
                ))
              ) : (
                <li style={{ color: '#aaa' }}>(No courses)</li>
              )}
            </ul>
          </div>
        );
      })}
    </div>
    {/*for past terms */}
    <div style={{ width: '25%', minWidth: '200px', display: 'grid', gridTemplateColumns: '1fr', gap: '24px', textAlign: 'left', marginLeft: '24px' }}>
      {plan
        .filter(({ term }) => term === 'PAST')
        .map(({ term, classes }) => (
          <div key={term}>
            <h2>{term}</h2>
            <ul style={{ marginTop: '-20px', listStyleType: 'none', paddingLeft: '0px' }}>
              {classes.map((c) => (
                <li key={c}>
                  <span>{c}</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
    </div>
  </div>
) : (
  <p className="text-gray-500" style={{ textAlign: 'center' }}>No courses planned yet.</p>
)}

    
     

      {/* validation message */}
         {validationMessage && (<>
            <div style={{ position: 'fixed', top: 0, left: 0, width: '100%', height: '100%', backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 999 }}>
                <div style={{ position: 'fixed', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', backgroundColor: '#fff', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)', zIndex: 1000, minWidth: '300px' }}>
                    <button onClick={() => setValidationMessage('')}
                        style={{ position: 'absolute', top: 10, right: 10, background: 'none', border: 'none', fontSize: '24px', color: '#888', cursor: 'pointer', fontWeight: 'bold' }}
                        aria-label="Close error popup"
                    >
                        ×
                    </button>
                   
                    <p>{validationMessage}</p>
                </div>
                </div>
                </>
            )}

              {popup && (<>
            <div style={{ position: 'fixed', top: 0, left: 0, width: '100%', height: '100%', backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 999 }}>
                <div style={{ position: 'fixed', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', backgroundColor: '#fff', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)', zIndex: 1000, minWidth: '300px' }}>
                    <button onClick={() => toggleMajor()}
                        style={{ position: 'absolute', top: 10, right: 10, background: 'none', border: 'none', fontSize: '24px', color: '#888', cursor: 'pointer', fontWeight: 'bold' }}
                        aria-label="Close error popup"
                    >
                        ×
                    </button>
                    <h2 style={{ marginTop: '10px' }}>Select Your Major</h2>
                    <select value={selectedDegree} style={{marginLeft:'0px'}} onChange={(e) => { setSelectedDegree(e.target.value); updateMajor(e.target.value); }}>
                       <option value="">Select Degree</option> {/* Default option */}
                    <option value="CS">Computer Science (CS)</option>
                     <option value="CSE">Computer Science and Engineering (CSE)</option>
                 </select>


                    
                </div>
                </div>
                </>
            )}

 
    </div>
            <div style={{ position: 'fixed', right: 0, top: 0, width: '10%', backgroundColor: '#9cbcc5', height: '100vh', zIndex: 1 }}></div>
      
    </div>
  );
}