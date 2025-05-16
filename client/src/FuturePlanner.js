import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './App.css';

// Make a secondary list of quarters and classes which users can choose from
// For updating possible quarters, get current date, determine quarter and add 11 quarters past it
// Add a save planner button which passes the plan to isValid and returns if the plan is valid, if so save users plan in database

export default function FuturePlanner() {
  const [plan, setPlan] = useState([]);
  const [quarter, setQuarter] = useState('');
  const [course, setCourse] = useState('');
  const navigate = useNavigate();

  const addCourseToQuarter = () => {
    if (!quarter || !course) return;

    setPlan((prevPlan) => {
      const existing = prevPlan.find((entry) => entry.term === quarter);
      if (existing) {
        return prevPlan.map((entry) =>
          entry.term === quarter
            ? { ...entry, classes: [...new Set([...entry.classes, course])] }
            : entry
        );
      } else {
        return [...prevPlan, { term: quarter, classes: [course] }];
      }
    });

    setCourse('');
  };

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
  };

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Future Course Planner</h1>

      <div className="flex space-x-2 mb-4">
        <input
          type="text"
          placeholder="e.g., 25F"
          value={quarter}
          onChange={(e) => setQuarter(e.target.value.toUpperCase())}
          className="border p-2 w-24"
        />
        <input
          type="text"
          placeholder="e.g., COM SCI 32"
          value={course}
          onChange={(e) => setCourse(e.target.value.toUpperCase())}
          className="border p-2 flex-1"
        />
        <button
          onClick={addCourseToQuarter}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Add Course
        </button>
      </div>

      {plan.length > 0 ? (
        <div className="space-y-4">
          {plan
            .sort((a, b) => (a.term < b.term ? -1 : 1))
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