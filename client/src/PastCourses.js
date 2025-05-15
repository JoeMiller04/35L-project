import { useNavigate } from 'react-router-dom';
import React, { useState } from 'react';
import './App.css';

// Add a save button to save taken courses in database which will be used in isValid
// users should default have empty taken courses

const cseCourses = [
  "COM SCI 31", "COM SCI 32", "COM SCI 33", "COM SCI 35L", "COM SCI M51A", "ECE 3", "ECE 100", "ECE 102", "ECE 115C",
  "COM SCI 111", "COM SCI 118", "COM SCI 131", "COM SCI 180", "COM SCI M151B",
  "MATH 31A", "MATH 31B", "MATH 32A", "MATH 32B", "MATH 33A", "MATH 33B", "MATH 61",
  "PHYSICS 1A", "PHYSICS 1B", "PHYSICS 1C", "PHYSICS 4AL/4BL"
];

export default function PastCourses() {
  const [takenCourses, setTakenCourses] = useState({});
  const navigate = useNavigate();
  const toggleCourse = (course) => {
    setTakenCourses((prev) => ({
      ...prev,  
      [course]: !prev[course],
    }));
  };

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">CSE Course Checklist</h1>
      <ul className="space-y-2">
        {cseCourses.map((course) => (
          <li key={course} className="flex items-center">
            <input
              type="checkbox"
              id={course}
              checked={takenCourses[course] || false}
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
  );
}