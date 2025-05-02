import { useNavigate } from 'react-router-dom';
import './App.css';
import React from 'react';

function Home3() {
    const navigate = useNavigate();

    return (
        <div>
            <h1>Welcome to the Home3 Page</h1>
            <p>This is the third page of our application.</p>
            <button onClick={() => navigate('/Home')}>Go to Home</button>
            <button onClick={() => navigate('/Home2')}>Go to Home2</button>
        </div>
    );
}

export default Home3;