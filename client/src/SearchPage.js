import { Link } from 'react-router-dom';
import { useNavigate, useLocation } from 'react-router-dom';
import './App.css';
import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function SearchPage() {
    const navigate = useNavigate();
    const location = useLocation();
    const [id, setId] = useState(null);
    const passedObject = location.state?.classInfo;
    const data = JSON.stringify(passedObject ? passedObject.grades : [], null, 2);
    const [gradesObj, setGradesObj] = useState(passedObject ? passedObject.grades : {});
    const [histogramData, setHistogramData] = useState(Object.entries(gradesObj).map(([name, value]) => ({
        name,
        value
    })));

    const [possibleClasses, setPossibleClasses] = useState([]);

    const [term, setTerm] = useState(passedObject.term);
    const [instructor, setInstructor] = useState(passedObject.instructor);
    const [dropdownOptions, setDropdownOptions] = useState([]);
    const [courseRating, setCourseRating] = useState(null);


    const [dropdown, setDropdown] = useState(() => {
        // Find the class in possibleClasses that matches the passedObject's term and instructor
        if (passedObject && possibleClasses.length > 0) {
            const match = possibleClasses.find(
                (cls) => cls.term === passedObject.term && cls.instructor.toLowerCase() === passedObject.instructor.toLowerCase()
            );
            return match ? match._id : '';
        }
        return '';
    });


    useEffect(() => {
        const userObj = JSON.parse(localStorage.getItem('user_id'));
        getCourseRating();
        if (userObj && userObj._id) {
            setId(userObj._id);   
        }
        if (passedObject) {
            classQuery();
        } else {
            alert("No class information provided.");}
    }, []);


    function capitalizeWords(str) {
        return str.replace(/\b\w/g, c => c.toUpperCase());
    }

    async function classQuery() {

        
        let params = new URLSearchParams();
        
        params = new URLSearchParams({
            subject: passedObject.subject,
            catalog: passedObject.catalog,});
    
       
        try {
            const response = await fetch(`http://127.0.0.1:8000/courses?${params.toString()}`, {
                method: 'GET', 
                headers: {
                    'Content-Type': 'application/json',
                },
                });
            if (response.ok) {
                let data = await response.json();
                // Filter out classes with null grades
                data = data.filter(cls => cls.grades != null);
                setPossibleClasses(data);
                if (data.length === 0) {
                    alert("No classes found for the selected criteria.");
                }

                
                
              
            } else if (response.status === 400) {
                alert("NOOO")
                
                
            } else {
                
                alert(response.status);
                
                
            }
        } catch (error) {
            alert("It is bad if we are here");
        }
        }

    function handleChange(drop) {
        setDropdown(drop.target.value);
        const selectedClass = possibleClasses.find(
            (possibleClass) => possibleClass._id === drop.target.value
        );
        if (!selectedClass) {
            setGradesObj({});
            setHistogramData([]);
            setTerm('');
            setInstructor('');
            return;
        }
        // Remove grade entries with null values
        const filteredGrades = Object.entries(selectedClass.grades || {})
            .filter(([_, value]) => value !== null)
            .reduce((acc, [name, value]) => {
                acc[name] = value;
                return acc;
            }, {});
        setGradesObj(filteredGrades);
        setHistogramData(
            Object.entries(filteredGrades).map(([name, value]) => ({
                name,
                value
            }))
        );
        setTerm(selectedClass.term);
        setInstructor(selectedClass.instructor);
    }
    
    useEffect(() => {
        if (passedObject && possibleClasses.length > 0) {
            const match = possibleClasses.find(
                (cls) => cls.term === passedObject.term && cls.instructor.toLowerCase() === passedObject.instructor.toLowerCase()
            );
            if (match) setDropdown(match._id);
        }
        
    }, [possibleClasses, passedObject]);

    async function getCourseRating() {
        
        try {
            const response = await fetch(`http://127.0.0.1:8000/ratings/${passedObject.subject}/${passedObject.catalog}`, {
                method: 'GET', 
                headers: {
                    'Content-Type': 'application/json',
                },
                });
            if (response.ok) {
                const data = await response.json();
                setCourseRating(data); // Store the result in courseRating state
            } else {
                setCourseRating(null);
            }
        } catch (error) {
            setCourseRating(null);
        }
    }

    return (
         <div style={{ display: 'flex', backgroundColor: '#f0f0f0', minHeight: '100vh' }}>
            <div style={{ position: 'fixed', left: 0, top: 0, width: '10%', backgroundColor: '#9cbcc5', height: '100vh', zIndex: 1 }}></div>
            <div style={{ width: '80%', marginLeft: '10%', zIndex: 2 }}>
             <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <button onClick={() => navigate('/Home')} style={{cursor:'pointer', backgroundColor:'white', marginLeft:'100px', padding: '10px 20px', fontSize: '16px', marginTop:'10px' }}>Home</button>
                    <h1 style={{ marginRight:'450px', fontSize: '30px' }}>{passedObject.subject} {passedObject.catalog} Information</h1>
                </div>

                <hr style={{color:'black', backgroundColor:'black', height:'1px', border:'none', marginTop:'0px'}} />

                <h1 style={{ textAlign: 'center', fontSize: '20px', fontWeight:'normal', marginTop:'30px' }}>Grade Distribution for {term} {passedObject.subject} {passedObject.catalog} with {capitalizeWords(instructor.toLowerCase())}</h1>


                <ResponsiveContainer width="70%" height={200} alignItems="center" justifyContent="center" style={{ margin: '0 auto', marginTop: '20px' }}>
                  {gradesObj && Object.keys(gradesObj).length > 0 ? (
                    <BarChart data={histogramData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="value" fill="#8884d8" />
                    </BarChart>
                  ) : (
                    <div style={{textAlign: 'center', width: '100%', paddingTop: '80px', fontSize: '20px', color: '#888'}}>No grade data available</div>
                  )}
                </ResponsiveContainer>

                 <select value={dropdown} onChange={handleChange} style={{ cursor:'pointer', width: '250px', height: '30px', border:'2px solid black',  display:'block', margin: '20px auto' }}>
                        {possibleClasses.map((possibleClasses, idx) => (
                            <option key={idx} value={possibleClasses._id}>
                                {possibleClasses.term} - {capitalizeWords(possibleClasses.instructor.toLowerCase())}
                            </option>
                        ))}
                    </select>
                
                
                
                    
                        <h1 style={{ textAlign: 'center', fontSize: '20px', fontWeight:'normal', marginTop:'30px' }}>
                  {courseRating && typeof courseRating === 'object'
                    ? `Course Rating: ${courseRating.rating ?? 'No rating available'}`
                    : courseRating ?? 'N/A'}
                </h1>













            
             </div>
            
            
            <div style={{ position: 'fixed', right: 0, top: 0, width: '10%', backgroundColor: '#9cbcc5', height: '100vh', zIndex: 1 }}></div>
        </div>
    );
}

export default SearchPage;