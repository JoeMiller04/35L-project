import { useNavigate } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import './App.css';

// List of required or typical CSE courses
const cseCourses = [
  "COM SCI 31", "COM SCI 32", "COM SCI 33", "COM SCI 35L", "COM SCI M51A", "ECE 3", "ECE 100", "ECE 102", "ECE 115C",
  "COM SCI 111", "COM SCI 118", "COM SCI 131", "COM SCI 180", "COM SCI M151B",
  "MATH 31A", "MATH 31B", "MATH 32A", "MATH 32B", "MATH 33A", "MATH 33B", "MATH 61",
  "PHYSICS 1A", "PHYSICS 1B", "PHYSICS 1C", "PHYSICS 4AL/4BL", "COM SCI ELECTIVE 1", "COM SCI ELECTIVE 2", "COM SCI ELECTIVE 3", "ECE ELECTIVE 1" 
];

export default function PastCourses() {
  // Track which courses have been checked (i.e., taken by the user)
  const [takenCourses, setTakenCourses] = useState({});
  const [selectedDegree, setSelectedDegree] = useState('');
  const navigate = useNavigate();
  const userObj = JSON.parse(localStorage.getItem("user_id"));
  const userId = userObj._id;


  const availableCourses = selectedDegree === 'CS'
    ? [
    "COM SCI 1",
    "COM SCI 30",
    "COM SCI 31",
    "COM SCI 32",
    "COM SCI 33",
    "COM SCI 35L",
    "COM SCI M51A",
    "MATH 31A",
    "MATH 31B",
    "MATH 32A",
    "MATH 32B",
    "MATH 33A",
    "MATH 33B",
    "MATH 61",
    "MATH 170A",
    "MATH 170E",
    "PHYSICS 1A",
    "PHYSICS 1B",
    "PHYSICS 1C",
    "PHYSICS 4AL",
    "PHYSICS 4BL",
    "LIFESCI 30A",
    "LIFESCI 30B",
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
    "COM SCI 188"
]
    : selectedDegree === 'CSE'
      ? [
    "COM SCI 1",
    "COM SCI 30",
    "COM SCI 31",
    "COM SCI 32",
    "COM SCI 33",
    "COM SCI 35L",
    "COM SCI M51A",
    "ECE 3",
    "MATH 31A",
    "MATH 31B",
    "MATH 32A",
    "MATH 32B",
    "MATH 33A",
    "MATH 33B",
    "MATH 61",
    "MATH 170A",
    "MATH 170E",
    "PHYSICS 1A",
    "PHYSICS 1B",
    "PHYSICS 1C",
    "PHYSICS 4AL",
    "PHYSICS 4BL",
    "LIFESCI 30A",
    "LIFESCI 30B",
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
    "ECE 100", 
    "ECE 102", 
    "ECE 115C"
]
      : [];

  // Load saved courses from backend when the component first mounts
  useEffect(() => {
    const loadPastCourses = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/users/${userId}/courses`);
        const data = await response.json(); // expects [{ term: "PAST", course_name: "..." }, ...]
        
        const pastOnly = data.filter((entry) => entry.term === "PAST");

        const initial = {};
        pastOnly.forEach(({ course_name }) => {
          initial[course_name] = true;
        });

        setTakenCourses(initial);
      } catch (err) {
        console.error("Error loading past courses:", err);
      }
    };

    loadPastCourses();
  }, [userId]);

  // Toggle checkbox state and update the backend accordingly
  const toggleCourse = async (course) => {
    const isNowChecked = !takenCourses[course];

    // Update UI state immediately
    setTakenCourses((prev) => ({
      ...prev,
      [course]: isNowChecked,
    }));


    // Update backend with add/remove action
    try {
      const response = await fetch(`http://127.0.0.1:8000/users/${userId}/courses`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          term: "PAST",
          course_name: course,
          action: isNowChecked ? 'add' : 'remove'
        })
      });

      if (!response.ok) throw new Error("Failed to update backend");
    } catch (err) {
      console.error("Error syncing course:", err);
    }
  };

  return (
    <div>
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">CSE Course Checklist</h1>

      {/* Degree selection dropdown */}
        <select
          value={selectedDegree}
          onChange={(e) => setSelectedDegree(e.target.value)}
          className="border p-2 mb-4"
        >
          <option value="">Select Degree</option> {/* Default option */}
          <option value="CS">Computer Science (CS)</option>
          <option value="CSE">Computer Science and Engineering (CSE)</option>
        </select>

      {/* Display course checklist only if a degree is selected */}
        {selectedDegree && (
      <ul className="space-y-2">
        {availableCourses.map((course) => (
          <li key={course} className="flex items-center">
            <input
              type="checkbox"
              id={course}
              checked={takenCourses[course] || false} // Default to false if not present
              onChange={() => toggleCourse(course)}
              className="mr-3"
            />
            <label htmlFor={course} className="text-lg">{course}</label>
          </li>
        ))}
      </ul>
        )}
      <button onClick={() => navigate('/Home')}>Go to Home</button>
      <button onClick={() => navigate('/SearchPage')}>Go to Home2</button>
      <button onClick={() => navigate('/InfoPage')}>Go to Home3</button>
      <button onClick={() => navigate('/FuturePlanner')}>Go to Home5</button>
      </div>

    </div>
  
  );
}