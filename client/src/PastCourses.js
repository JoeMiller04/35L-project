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
  const navigate = useNavigate();
  const userObj = JSON.parse(localStorage.getItem("user_id"));
  const userId = userObj._id;

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
      <ul className="space-y-2">
        {cseCourses.map((course) => (
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
      <button onClick={() => navigate('/Home')}>Go to Home</button>
      <button onClick={() => navigate('/SearchPage')}>Go to Home2</button>
      <button onClick={() => navigate('/InfoPage')}>Go to Home3</button>
      <button onClick={() => navigate('/FuturePlanner')}>Go to Home5</button>
      </div>

    </div>
  
  );
}