import { useNavigate } from 'react-router-dom';
import './App.css';
import React from 'react';

function Home() {
    const navigate = useNavigate();

    return (
        <div>
            <h1>Welcome to the Home Page</h1>
            <p>This is the home page of our application.</p>
            <button onClick={() => navigate('/Home2')}>Go to Home2</button>
            <button onClick={() => navigate('/Home3')}>Go to Home3</button>
        </div>
    );
}

export default Home;