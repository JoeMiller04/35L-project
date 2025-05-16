import { useNavigate } from 'react-router-dom';
import React, { useState } from 'react';
import './App.css';

// Add a save button to save taken courses in database which will be used in isValid
// users should default have empty taken courses

const cseCourses = [
  "COM SCI 31", "COM SCI 32", "COM SCI 33", "COM SCI 35L", "COM SCI M51A", "ECE 3", "ECE 100", "ECE 102", "ECE 115C",
  "COM SCI 111", "COM SCI 118", "COM SCI 131", "COM SCI 180", "COM SCI M151B",
  "MATH 31A", "MATH 31B", "MATH 32A", "MATH 32B", "MATH 33A", "MATH 33B", "MATH 61",
  "PHYSICS 1A", "PHYSICS 1B", "PHYSICS 1C", "PHYSICS 4AL/4BL", "COM SCI ELECTIVE 1", "COM SCI ELECTIVE 2", "COM SCI ELECTIVE 3", "ECE ELECTIVE 1" 
];

export default function PastCourses() {

  const navigate = useNavigate();
  const [takenClasses, setTakenClasses] = useState([]);
 
  

  return (

     <div style={{ display: 'flex', backgroundColor: '#f0f0f0', minHeight: '100vh' }}>
    <div style={{ width: '10%', backgroundColor: '#9cbcc5', height: '100vh' }}></div>
    <div style={{ width: '80%' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <button onClick={() => navigate('/Home')} style={{marginLeft:'50px', padding: '10px 20px', fontSize: '16px', marginTop:'10px' }}>Home</button>
                    <h1 style={{ textAlign: 'center', fontSize: '50px', marginRight:'360px' }}>Degree Information</h1>
                </div>

                <hr style={{color:'black', backgroundColor:'black', height:'4px', border:'none', marginTop:'0px'}}/>
              <div style={{ textAlign: 'center', fontSize: '20px', margin: '30px 0' }}>
                   <p style={{ display: 'inline', margin: '0 20px' }}>Name: Kyle Reisinger</p>
                   <p style={{ display: 'inline', margin: '0 50px' }}>Year: Sophomore</p>
                   <p style={{ display: 'inline', margin: '0 50px' }}>Completed Units: 100</p>
                   <p style={{display: 'inline', margin:'0 20px'}}>Major: Computer Science and Engineering</p>
              </div>

              <hr style={{color:'black', backgroundColor:'black', height:'4px', border:'none', marginTop:'30px'}}/>
              <p style={{ textAlign: 'center', fontSize: '35px', marginTop:'20px'}}> Course History</p>

              
              <div style={{display: 'flex',flexDirection: 'row',justifyContent: 'center',alignItems: 'flex-start',marginTop: '-50px',gap: '500px'}}>
                  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                      <p style={{ fontSize: '20px'}}>Past Courses</p>
                           {/* Add past courses content here if needed */}
                           <div style={{display: 'flex',flexDirection: 'row',justifyContent: 'center',alignItems: 'flex-start',marginTop: '-20px',gap: '250px'}}>
                          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>

                            
                                <p>Test</p>


                          </div>


                          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>

                            
                            <p>Test</p>


                          </div>

                        </div>
                      </div>
                  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <p style={{ fontSize: '20px'}}>Future Courses</p>
                      {/* Add future courses content here if needed */}
                    </div>
                    </div>





           <div >
     
   

    </div>




    </div>

     




   
    <div style={{ width: '10%', backgroundColor: '#9cbcc5', height: '100vh' }}></div>
    </div>
  );
}