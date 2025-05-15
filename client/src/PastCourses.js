import React, { useState } from 'react';

const cseCourses = [
  "COM SCI 31", "COM SCI 32", "COM SCI 33", "COM SCI 35L",
  "COM SCI 111", "COM SCI 131", "COM SCI 180", "COM SCI M151B",
  "MATH 31A", "MATH 31B", "MATH 32A", "MATH 32B", "MATH 33A", "MATH 33B",
  "PHYSICS 1A", "PHYSICS 1B", "PHYSICS 1C"
];

export default function PastCourses() {
  const [takenCourses, setTakenCourses] = useState({});

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
    </div>
  );
}