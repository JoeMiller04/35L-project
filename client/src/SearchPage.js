import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import './App.css';
import React from 'react';

function SearchPage() {
    const navigate = useNavigate();

    return (
        <div>
            <h1>Welcome to the Home2 Page</h1>
            <p>This is the second page of our application.</p>
            <button onClick={() => navigate('/Home')}>Go to Home</button>
            <button onClick={() => navigate('/InfoPage')}>Go to Home3</button>
        </div>
    );
}

export default SearchPage;