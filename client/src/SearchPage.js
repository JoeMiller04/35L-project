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
    const [dropdown, setDropdown] = useState(passedObject.term + passedObject.instructor);


    useEffect(() => {
        const userObj = JSON.parse(localStorage.getItem('user_id'));
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
                const data = await response.json()
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
            (possibleClass) => possibleClass.term + possibleClass.instructor === drop.target.value
        );
        setGradesObj(selectedClass.grades || {});
        setHistogramData(
            Object.entries(selectedClass.grades || {}).map(([name, value]) => ({
                name,
                value
            }))
        );
        setTerm(selectedClass.term);
        setInstructor(selectedClass.instructor);
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

                <h1 style={{ textAlign: 'center', fontSize: '20px', fontWeight:'normal' }}>Grade Distribution for {term} {passedObject.subject} {passedObject.catalog} with {capitalizeWords(instructor.toLowerCase())}</h1>


                <ResponsiveContainer width="70%" height={200} alignItems="center" justifyContent="center" style={{ margin: '0 auto', marginTop: '20px' }}>
                  <BarChart data={histogramData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="value" fill="#8884d8" />
                  </BarChart>
                </ResponsiveContainer>

                 <select value={dropdown} onChange={handleChange} style={{ cursor:'pointer', width: '250px', height: '30px', border:'2px solid black' }}>
                        {possibleClasses.map((possibleClasses, idx) => (
                            <option key={idx} value={possibleClasses.term + capitalizeWords(possibleClasses.instructor.toLowerCase())}>
                                {possibleClasses.term} - {capitalizeWords(possibleClasses.instructor.toLowerCase())}
                            </option>
                        ))}
                    </select>
                

                















            
             </div>
            
            
            <div style={{ width: '10%', backgroundColor: '#9cbcc5', height: '100vh', zIndex: 1 }}></div>
        </div>
    );
}

export default SearchPage;