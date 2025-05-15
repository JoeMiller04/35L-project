import { useNavigate } from 'react-router-dom';
import './App.css';
import React from 'react';

function InfoPage() {
    const navigate = useNavigate();

    return (
        <div>
            <h1>Welcome to the Home3 Page</h1>
            <p>This is the third page of our application.</p>
            <button onClick={() => navigate('/Home')}>Go to Home</button>
            <button onClick={() => navigate('/SearchPage')}>Go to Home2</button>
            <button onClick={() => navigate('/PastCourses')}>Go to Home4</button>
            <button onClick={() => navigate('/FuturePlanner')}>Go to Home5</button>
        </div>
    );
}

export default InfoPage;