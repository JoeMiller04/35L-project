import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './App.css';

// Add a save planner button which passes the plan to isValid and returns if the plan is valid, if so save users plan in database

// Options for dropdowns
const availableTerms = ["25W", "25S", "25F", "26W", "26S", "26F"];
const availableCourses = [
  "COM SCI 31", "COM SCI 32", "COM SCI 33", "COM SCI 35L", "COM SCI M51A", "ECE 3", "ECE 100", "ECE 102", "ECE 115C",
  "COM SCI 111", "COM SCI 118", "COM SCI 131", "COM SCI 180", "COM SCI M151B",
  "MATH 31A", "MATH 31B", "MATH 32A", "MATH 32B", "MATH 33A", "MATH 33B", "MATH 61",
  "PHYSICS 1A", "PHYSICS 1B", "PHYSICS 1C", "PHYSICS 4AL/4BL"
];

  // Helper to sort terms: e.g., 25W -> 251, 25S -> 252
  const termToSortable = (term) => {
  const year = parseInt(term.slice(0, 2)); // "25W" → 25
  const quarterCode = { W: 1, S: 2, F: 3 }[term[2]]; // "W" → 1, "S" → 2, "F" → 3
  return year * 10 + quarterCode;
};

export default function FuturePlanner() {
  const [plan, setPlan] = useState([]); // Main state: [{ term: "25F", classes: ["COM SCI 32"] }]
  const [selectedTerm, setSelectedTerm] = useState('');
  const [selectedCourse, setSelectedCourse] = useState('');
  const navigate = useNavigate();
  const userObj = JSON.parse(localStorage.getItem("user_id"));
  const userId = userObj._id;
  //const userId = "68361c156a49e4907460b4a8";

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
  };

  if (userId) loadSavedPlan();
}, [userId]);

  // Add selected course to selected term in plan
  const addCourseToQuarter = () => {
    if (!selectedTerm || !selectedCourse) return;

    setPlan((prevPlan) => {
      const existing = prevPlan.find((entry) => entry.term === selectedTerm);
      if (existing) {
        return prevPlan.map((entry) =>
          entry.term === selectedTerm
            ? { ...entry, classes: [...new Set([...entry.classes, selectedCourse])] }
            : entry
        );
      } else {
        return [...prevPlan, { term: selectedTerm, classes: [selectedCourse] }];
      }
    });

    fetch(`http://127.0.0.1:8000/users/${userId}/courses`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      term: selectedTerm,
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

  return (
    <div style={{ display: 'flex', backgroundColor: '#f0f0f0', minHeight: '100vh' }}>
        <div style={{ position: 'fixed', left: 0, top: 0, width: '10%', backgroundColor: '#9cbcc5', height: '100vh', zIndex: 1 }}></div>
        <div style={{ width: '80%', marginLeft: '10%', marginRight: '10%', zIndex: 2 }}>


          {/*upper text*/}
       <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <button onClick={() => navigate('/PastCourses')} style={{cursor:'pointer', backgroundColor:'white', marginLeft:'50px', padding: '10px 20px', fontSize: '16px', marginTop:'10px' }}>Degree Information</button>
                    <h1 style={{ textAlign: 'center', fontSize: '50px' }}>Future Planner</h1>
                    <button onClick={() => navigate('/InfoPage')} style={{cursor:'pointer', backgroundColor:'white', marginRight:'50px', padding: '10px 20px', fontSize: '16px', marginTop:'10px' }}>View Classes</button>
        </div>
     
     
     
     
     
      {/* Dropdowns to select term and course */} 
      <div className="flex flex-wrap items-center gap-2 mb-4">
        <select
          value={selectedTerm}
          onChange={(e) => setSelectedTerm(e.target.value)}
          className="border p-2"
        >
          <option value="">Select Term</option>
          {availableTerms.map((term) => (
            <option key={term} value={term}>
              {term}
            </option>
          ))}
        </select>

        <select
          value={selectedCourse}
          onChange={(e) => setSelectedCourse(e.target.value)}
          className="border p-2 flex-1"
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
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Add Course
        </button>
      </div>

      {/* Display user's plan */}  
     {plan.length > 0 ? (
        <div className="space-y-4">
          {plan
            .sort((a, b) => termToSortable(a.term) - termToSortable(b.term))
            .map(({ term, classes }) => (
              <div key={term} className="border p-4 rounded shadow">
                <h2 className="font-semibold text-xl mb-2">{term}</h2>
                <ul className="list-disc list-inside space-y-1">
                  {classes.map((c) => (
                    <li key={c} className="flex justify-between items-center">
                      <span>{c}</span>
                      <button
                        onClick={() => removeCourse(term, c)}
                        className="text-red-500 text-sm"
                      >
                        Remove
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
        </div>
      ) : (
        <p className="text-gray-500">No courses planned yet.</p>
      )}

    {/* Validate Button */} 
      <div className="mt-6 text-center">
        <button
          onClick={() => console.log("Validate button clicked")}
          className="bg-green-600 hover:bg-green-700 text-white font-semibold px-6 py-2 rounded-md shadow"
        >
          Validate Plan
        </button>
      </div>

    <button onClick={() => navigate('/Home')}>Go to Home</button>
    <button onClick={() => navigate('/SearchPage')}>Go to Home2</button>
    <button onClick={() => navigate('/InfoPage')}>Go to Home3</button>
    <button onClick={() => navigate('/PastCourses')}>Go to Home4</button>
    <button onClick={() => navigate('/FuturePlanner')}>Go to Home5</button>
    </div>
        <div style={{ width: '10%', backgroundColor: '#9cbcc5', height: '100vh', zIndex: 1 }}></div>
      
    </div>
  );
} 