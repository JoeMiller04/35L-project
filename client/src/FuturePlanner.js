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

  // Dont think this works
  //const userId = 681e758d4b121097b1e43aef;
  const userId = localStorage.getItem("user_id");

      // POST to backend to update user’s course list
    const updateCourseInDB = async (courseName, action) => {
    try {
      const response = await fetch(`/users/${userId}/courses`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          course_name: courseName,
          action: action,
        }),
      });
      return await response.json();
    } catch (err) {
      console.error("Error updating course:", err);
    }
  };

  // GET saved courses from the backend
  useEffect(() => {
  const loadSaved = async () => {
    const fetchSavedCourses = async () => {
      try {
        const response = await fetch(`/users/${userId}/courses`);
        if (!response.ok) throw new Error("Failed to fetch saved courses");
        const data = await response.json();
        return data;
      } catch (err) {
        console.error("Error fetching saved courses:", err);
        return [];
      }
    };

    if (!userId) return;
    const savedCourses = await fetchSavedCourses();

    // Doesnt save term at the moment
    const grouped = {};
    savedCourses.forEach((course) => {
      if (!grouped["UNSPECIFIED"]) grouped["UNSPECIFIED"] = [];
      grouped["UNSPECIFIED"].push(course);
    });

    const newPlan = Object.entries(grouped).map(([term, classes]) => ({
      term,
      classes,
    }));

    setPlan(newPlan);
  };

  loadSaved();
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

    updateCourseInDB(selectedCourse, "add");
    setSelectedCourse('');
  };

  // Remove course from a specific term
  const removeCourse = (term, courseToRemove) => {
    setPlan((prevPlan) =>
      prevPlan
        .map((entry) =>
          entry.term === term
            ? { ...entry, classes: entry.classes.filter((c) => c !== courseToRemove) }
            : entry
        )
        .filter((entry) => entry.classes.length > 0)
    );

    updateCourseInDB(courseToRemove, "remove");
  };

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Future Course Planner</h1>

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

    <button onClick={() => navigate('/Home')}>Go to Home</button>
    <button onClick={() => navigate('/SearchPage')}>Go to Home2</button>
    <button onClick={() => navigate('/InfoPage')}>Go to Home3</button>
    <button onClick={() => navigate('/PastCourses')}>Go to Home4</button>
    <button onClick={() => navigate('/FuturePlanner')}>Go to Home5</button>
    </div>
  );
}