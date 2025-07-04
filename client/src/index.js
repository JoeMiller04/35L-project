import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Navigation from './App'; // Ensure this matches the export from App.js
import { BrowserRouter } from 'react-router-dom';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
    <Navigation />
  </BrowserRouter>
);
