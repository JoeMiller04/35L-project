import { Link } from 'react-router-dom';
import { useNavigate, useLocation } from 'react-router-dom';
import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function SearchPage() {
    const navigate = useNavigate();
    const location = useLocation();
    const [id, setId] = useState(null);
    const passedObject = location.state?.classInfo;
    const data = JSON.stringify(passedObject ? passedObject.grades : [], null, 2);
    const [gradesObj, setGradesObj] = useState([]);
    const [histogramData, setHistogramData] = useState(Object.entries(gradesObj).map(([name, value]) => ({
        name,
        value
    })));

    const [possibleClasses, setPossibleClasses] = useState([]);

    const [term, setTerm] = useState('');
    const [instructor, setInstructor] = useState('');
    const [dropdownOptions, setDropdownOptions] = useState([]);
    const [courseRating, setCourseRating] = useState(null);


    const [dropdown, setDropdown] = useState('');

    const [description, setDescription] = useState('');
    const [units, setUnits] = useState('');
    const [title, setTitle] = useState('');
    const [professorRatings, setProfessorRatings] = useState([]);


    useEffect(() => {
        const userObj = JSON.parse(localStorage.getItem('user_id'));
        getCourseRating();
        getCourseDescription();
        getProfessorRatings();
        if (userObj && userObj._id) {
            setId(userObj._id);   
        }
        if (passedObject) {
            classQuery();
        } else {
        console.log("No class information provided.");}
            
    }, []);


    useEffect(() => {
        if (possibleClasses.length > 0) {
            setDropdown(possibleClasses[0]._id || '');
            // Remove grade entries with null values
            const filteredGrades = Object.entries(possibleClasses[0].grades || {})
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
            setTerm(possibleClasses[0].term || '');
            setInstructor(possibleClasses[0].instructor || '');
        }
    }, [possibleClasses]);

    async function getProfessorRatings() {

      
    

        try {
            const response = await fetch(`http://127.0.0.1:8000/professor_ratings/${passedObject.subject}/${passedObject.catalog}`, {
                method: 'GET', 
                headers: {
                    'Content-Type': 'application/json',
                },
            });


            if (response.ok) {
                const data = await response.json();
                if (data) {
                    
                    setProfessorRatings(data.professors);
                } else {
                    console.log("NOO");
                    return [];
                }
            } else {
                console.log("No professor ratings found for this course.");
                return [];
            }
        } catch (error) {   
            console.log("Error fetching professor ratings: " + error.message);
            return [];
        }

    }


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
              
                data = data.filter(cls => cls.grades != null);
                setPossibleClasses(data);
                if (data.length === 0) {
                    //alert("No classes found for the selected criteria.");
                    console.log("No classes found for the selected criteria.");
                }

                
                
              
            } else if (response.status === 400) {
                console.log("NOOO")
                
                
            } else {
                
                console.log(response.status);
                
                
            }
        } catch (error) {
            console.log("It is bad if we are here");
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
                setCourseRating(data);
            } else {
                setCourseRating(null);
            }
        } catch (error) {
            setCourseRating(null);
        }
    }

    async function getCourseDescription() {
        
        try {
            const response = await fetch(`http://127.0.0.1:8000/description/${passedObject.subject}/${passedObject.catalog}`, {
                method: 'GET', 
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            if (response.ok) {
                
                const data = await response.json();
                setTitle(data.title);
                setUnits(data.units);
                setDescription(data.description);
                return data.description; 
            } else {
                console.log("No description found for this course");
                return "No description available";
            }
        } catch (error) {
            return "Error fetching description";
        }

    }

    
function getRatingColor(rating) {
    if (typeof rating !== 'number') return 'black';
    if (rating < 1.75) return '#8B0000'; 
    if (rating < 2.5) return 'red';
    if (rating < 3.5) return '#FFD600'; 
    if (rating < 4.25) return '#90EE90'; 
    return 'green';
}

    return (
         <div style={{ display: 'flex', backgroundColor: '#f0f0f0', minHeight: '100vh' }}>
            <div style={{ position: 'fixed', left: 0, top: 0, width: '10%', backgroundColor: '#9cbcc5', height: '100vh', zIndex: 1 }}></div>
            <div style={{ width: '80%', marginLeft: '10%', zIndex: 2 }}>
             <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative', width: '100%', marginBottom: '20px', marginTop: '20px' }}>
             
                <div style={{ display: 'flex', alignItems: 'center', position: 'absolute', left: 0, height: '100%' }}>
                  <button onClick={() => navigate('/Home')} style={{ cursor: 'pointer', backgroundColor: 'white', marginLeft: '50px', padding: '10px 20px', fontSize: '12px', marginTop: '10px', fontWeight: 'bold' }}>Home</button>
                </div>
              
                <div style={{ flex: 1, display: 'flex', justifyContent: 'center' }}>
                  <h1 style={{ margin: 0, fontSize: '30px', textAlign: 'center', fontWeight: 'bold' }}>{passedObject.subject} {passedObject.catalog}</h1>
                </div>
                
                <div style={{ display: 'flex', alignItems: 'center', position: 'absolute', right: 0, height: '100%' }}>
                  <button style={{ marginRight: '50px', fontSize: '12px', marginTop: '10px', borderWidth: '0px', width: '90px', backgroundColor: 'white', fontWeight: 'bold' }}></button>
                </div>
              </div>

                <hr style={{color:'black', backgroundColor:'black', height:'1px', border:'none', marginTop:'20px'}} />


             <div style={{ display: 'flex', backgroundColor: '#f0f0f0', minHeight: '50vh' }}>
                    <div style={{ width: '60%', marginLeft: '5%', zIndex: 4, borderRight: '1px solid black', height:'100%', marginRight:'100px' }}>
                        <h1 style={{ fontWeight:'bold', textAlign: 'left', fontSize: '20px', marginTop:'30px', zIndex:5, marginLeft:'30px', marginRight:'30px' }}>{passedObject.subject} {passedObject.catalog} - {passedObject.title}</h1>
                        <h1 style={{ fontSize:'18px', textAlign: 'left',  fontWeight:'normal', marginTop:'10px', zIndex:5, marginLeft:'30px', marginRight:'30px' }}>Units: {units}</h1>
                        <h1 style={{ textAlign: 'left', fontSize: '18px', fontWeight:'normal', marginTop:'10px', zIndex:5, marginLeft:'30px', marginRight:'50px' }}>{description}</h1>
                    
                    
                     {gradesObj && Object.keys(gradesObj).length > 0 && (
                <h1 style={{ textAlign: 'center', fontSize: '20px', fontWeight:'normal', marginTop:'50px', marginLeft:'-30px' }}>Grade Distribution for {term} {passedObject.subject} {passedObject.catalog} with {capitalizeWords(instructor.toLowerCase())}</h1>
                )}






                <ResponsiveContainer width="80%" height={200} alignItems="center" justifyContent="center" style={{ margin: '0 auto', marginTop: '20px', marginLeft:'30px' }}>
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

                 {gradesObj && Object.keys(gradesObj).length > 0 && (
                  <select value={dropdown} onChange={handleChange} style={{ cursor:'pointer', width: '250px', height: '30px', border:'2px solid black',  display:'block', margin: '20px auto' }}>
                        {possibleClasses.map((possibleClasses, idx) => (
                            <option key={idx} value={possibleClasses._id}>
                                {possibleClasses.term} - {capitalizeWords(possibleClasses.instructor.toLowerCase())}
                            </option>
                        ))}
                    </select>
                 )}
                    </div>
                    <div style={{ width: '35%', zIndex: 5, marginLeft:'-10%' }}>
                        
                        <h1 style={{ fontWeight:'bold', textAlign: 'center', fontSize: '25px', marginTop:'30px' }}>Overall Course Rating:</h1>
                        <h1 style={{ textAlign: 'center', fontSize: '60px', fontWeight:'normal', marginTop:'10px', color: (() => {
    let val = null;
    if (courseRating && typeof courseRating === 'object' && typeof courseRating.rating === 'string' && courseRating.rating.includes(':')) {
        val = parseFloat(courseRating.rating.split(':').pop().trim());
    } else if (courseRating && typeof courseRating === 'object' && typeof courseRating.rating === 'number') {
        val = courseRating.rating;
    } else if (typeof courseRating === 'number') {
        val = courseRating;
    }
    return getRatingColor(val);
})() }}>
    {courseRating && typeof courseRating === 'object' && typeof courseRating.rating === 'string' && courseRating.rating.includes(':')
        ? courseRating.rating.split(':').pop().trim() || 'No rating available'
        : courseRating && typeof courseRating === 'object' && courseRating.rating
            ? courseRating.rating
            : courseRating ?? 'N/A'}

    
    {professorRatings && professorRatings.length > 0 && (
        <div style={{ fontSize: '16px', marginTop: '100px', color: 'black', textAlign:'right', marginRight:'130px' }}>
            <div style={{fontSize:'25px', color:'black', marginBottom:'20px', textAlign:'center', marginRight:'-130px', fontWeight:'bold'}}> Professors by Rating:</div>
            {professorRatings
              .filter(professor => professor.rating !== 'N/A')
              .sort((a, b) => parseFloat(b.rating) - parseFloat(a.rating))
              .slice(0, 10)
              .map((professor, index) => (
                <div key={index} style={{ marginBottom: '5px' }}>
                  {professor.name}: {professor.rating}
                </div>
              ))}
        </div>
    )}
</h1>


                    </div>
                </div>


               
                
                
               
                 









            
             </div>
            
            
            <div style={{ position: 'fixed', right: 0, top: 0, width: '10%', backgroundColor: '#9cbcc5', height: '100vh', zIndex: 1 }}></div>
        </div>
    );
}

export default SearchPage;