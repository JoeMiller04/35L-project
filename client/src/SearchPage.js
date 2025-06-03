import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import './App.css';
import React, { useState } from 'react';

function SearchPage() {
    const navigate = useNavigate();
    


    return (
         <div style={{ display: 'flex', backgroundColor: '#f0f0f0', minHeight: '100vh' }}>
            <div style={{ position: 'fixed', left: 0, top: 0, width: '10%', backgroundColor: '#9cbcc5', height: '100vh', zIndex: 1 }}></div>
            <div style={{ width: '80%', marginLeft: '10%', zIndex: 2 }}>
             <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <button onClick={() => navigate('/Home')} style={{cursor:'pointer', backgroundColor:'white', marginLeft:'100px', padding: '10px 20px', fontSize: '16px', marginTop:'10px' }}>Home</button>
                    <h1 style={{ textAlign: 'center', fontSize: '50px' }}>Past Classes</h1>
                    <button onClick={() => navigate('/InfoPage')} style={{cursor:'pointer', backgroundColor:'white', marginRight:'100px', padding: '10px 20px', fontSize: '16px', marginTop:'10px' }}>View Classes</button>
                </div>

                <hr style={{color:'black', backgroundColor:'black', height:'1px', border:'none', marginTop:'0px'}} />

                

















            
             </div>
            
            
            <div style={{ width: '10%', backgroundColor: '#9cbcc5', height: '100vh', zIndex: 1 }}></div>
        </div>
    );
}

export default SearchPage;