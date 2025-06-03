import { useNavigate } from 'react-router-dom';
import './App.css';
import { useState, useEffect } from 'react';

//this page should be mostly done. It is the home page


function Home() {
    const navigate = useNavigate();
    const [classes, setClasses] = useState([]);
    const colors = ['#FFD1DC', '#FFABAB', '#FFC3A0', '#FF677D', '#D4A5A5', '#392F5A', '#31A2AC', '#61C0BF', '#6B4226', '#D9BF77']; //someone change these to something better
    const [index, setIndex] = useState(-1);
    const [dropdown, setDropdown] = useState('- Select Dept -');
    const [dropdownClass, setDropdownClass] = useState('- Select a Class -');
    const [quarter, setQuarter] = useState("25S");
    const [dataFromQuery, setDataFromQuery] = useState([]);
    const [id, setId] = useState(null);
    const [subjects, setSubjects] = useState([]);
    const [classesPerSubject, setClassesPerSubject] = useState({});
    const [error, setError] = useState(null);
    const [popup, setPopup] = useState(false);
    const dayOrder = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    // Run changeColor every time a new class is rendered
    useEffect(() => {
        if (classes.length > 0) {
            changeColor();
        }
    }, [classes, index]); 

    // update class list when user loads in
    useEffect(() => {
        const userObj = JSON.parse(localStorage.getItem('user_id'));
        if (userObj && userObj._id) {
            setId(userObj._id);
            setClasses([]);
            runGetClasses(userObj._id);
        }
        getSubjects();
        setClassesPerSubject({'- Select Dept -': ['- Select a Class -']});
    }, []);

    //fetch classes from backend
    async function updateUserCourseList(userId, courseId) {
        if (!userId) {
            userId = JSON.parse(localStorage.getItem('user_id'));
            userId = userId._id;
            setId(userId);
        }
        try {
            const response = await fetch(`http://127.0.0.1:8000/users/${userId}/course-list`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ course_id: courseId, action:"add" }),
              
            });
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to update course list');
            }
            setClasses([]);
            runGetClasses(userId);
            return await response.json();

        } catch (err) {
            setError(err.message);
            setPopup(true);
        }
    }

    function addClass(id, courseId, action) {
        updateUserCourseList(id, courseId, action);
    }

    async function getClasses(userId) {
        setClasses([]);
        if (!userId) {
            userId = JSON.parse(localStorage.getItem('user_id'));
            userId = userId._id;
            setId(userId);
        }
        try {
            const response = await fetch(`http://127.0.0.1:8000/users/${userId}/course-list`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to fetch user course list');
            }
            const data = await response.json();
            setClasses(data);
        } catch (err) {
            alert('Error fetching user course list: ' + err.message);
        }
    }

    function runGetClasses(userId) {
        getClasses(userId);
    }

    //Get grid column and row for each class
    function calcGridPosition(clas) {
        const startRow = getTimeRow(clas.start);
        const endRow = getTimeRow(clas.end);
        return {
            gridColumn: getDayColumn(clas.day),
            gridRow: startRow,
            gridRowEnd: `span ${endRow - startRow}`, 
        };
    }

    //Process time for text
    function makeTimeNice(time) {
        function format(t) {
            t = t.toString().padStart(4, '0');
            let hour = parseInt(t.slice(0, 2), 10);
            let min = t.slice(2);
            let ampm = hour < 12 ? 'AM' : 'PM';
            if (hour > 12) hour -= 12;
            if (hour === 0) hour = 12; 
            return `${hour}:${min} ${ampm}`;
        }
        if (Array.isArray(time) && time.length === 2) {
            return `${format(time[0])} - ${format(time[1])}`;
        }
        if (Array.isArray(time)) {
            return time.map(format).join(', ');
        }
        return String(time);
    }

    //Get column from day fo the week
    function getDayColumn(day) {
        switch (day) {
            case 'Sunday':
                return 1;
            case 'Monday':
                return 2;
            case 'Tuesday':
                return 3;
            case 'Wednesday':
                return 4;
            case 'Thursday':
                return 5;
            case 'Friday':
                return 6;
            case 'Saturday':
                return 7;
            default:
                return 1; 
        }
    }

  

    //query class function
    async function classQuery() {

        let temp = dropdown;
        if (temp === "COMSCI") {
            temp = "COM SCI";
        } else if (temp === "ECENGR") {
            temp = "EC ENGR";
        }
        let params = new URLSearchParams();
        if (quarter === "idk") {
            params = new URLSearchParams({
                subject: temp,
                catalog: dropdownClass
            });
        } else {
            params = new URLSearchParams({
                term: quarter,
                subject: temp,
                catalog: dropdownClass
            });
        }
       
        try {
            const response = await fetch(`http://127.0.0.1:8000/courses?${params.toString()}`, {
                method: 'GET', 
                headers: {
                    'Content-Type': 'application/json',
                },
                });
            if (response.ok) {
                const data = await response.json()
                setDataFromQuery(data);
                if (data.length === 0) {
                    setError("No classes found for the selected criteria.");
                    setPopup(true);
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
    

    //get row from time
    function getTimeRow(time) {
        if (typeof time === 'number') {
            time = time.toString().padStart(4, '0');
        }
        if (typeof time !== 'string' || time.length !== 4) {
            return 2; // default row
        }
        const hour = parseInt(time.slice(0, 2), 10);
        const minute = parseInt(time.slice(2), 10);
        // 12 rows per hour, starting at 8am
        let row = 2 + (hour - 8) * 12 + Math.floor(minute / 5);
        return row;
    }

    //change color of class blocks
    function changeColor() {
        if (index === 9) {
            setIndex(0);
        } else {
            setIndex(index + 1);
        }
    }

  

  

  const quarterOptions = [
    { value:'idk', label: 'Any Term'},
    { value: '25S', label: 'Spring 2025' }
   
  ];

    //dropdown change function
    function handleChange(drop) {
        setDropdown(drop.target.value);
        getClassesBySubject(drop.target.value);
    }

    function handleQuarterChange(drop) {
        setQuarter(drop.target.value);
    }

    function handleClassChange(drop) {
        setDropdownClass(drop.target.value);
    }

    function handleClassQuery() {
        classQuery();

    }

    // Capitalize the first letter
     function capitalizeWords(str) {
        return str.replace(/\b\w/g, c => c.toUpperCase());
    }

    async function getSubjects() {
        try {
            const response = await fetch('http://127.0.0.1:8000/subjects', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            if (!response.ok) {
                throw new Error('Failed to fetch subjects');
            }
            const thing = await response.json();
            // Insert a custom first element, e.g., '— Select Dept —'
            setSubjects(['- Select Dept -', ...thing]);
        } catch (error) {
            alert('Error fetching subjects: ' + error.message);
            return [];
        }
    }

    async function getClassesBySubject(subject) {
        if (subject === '- Select Dept -') {
            setClassesPerSubject({'- Select Dept -': ['- Select a Class -']});
            setDropdownClass('- Select a Class -');
            return [];
        }
        try {
        
            const response = await fetch(`http://127.0.0.1:8000/courses/catalogs/${encodeURIComponent(subject)}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            if (!response.ok) {
                throw new Error('Failed to fetch catalogs');
            }
            const catalogs = await response.json();
            setClassesPerSubject(prev => ({ ...prev, [subject]: catalogs }));
            setDropdownClass((catalogs && catalogs.length > 0) ? catalogs[0] : '- Select a Class -');
            return catalogs;
        } catch (error) {
            alert('Error fetching catalogs: ' + error.message);
            setDropdownClass('- Select a Class -');
            return [];
        }
    }
    
    return (
        <div style={{ display: 'flex', backgroundColor: '#f0f0f0', minHeight: '100vh' }}>
        <div style={{ position: 'fixed', left: 0, top: 0, width: '10%', backgroundColor: '#9cbcc5', height: '100vh', zIndex: 1 }}></div>
        <div style={{ width: '80%', marginLeft: '10%', marginRight: '10%', zIndex: 2 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <button onClick={() => navigate('/PastCourses')} style={{cursor:'pointer', backgroundColor:'white', marginLeft:'50px', padding: '10px 20px', fontSize: '12px', marginTop:'10px', fontWeight: 'bold' }}>Past Courses</button>
                    <button onClick={() => navigate('/SearchPage')} style={{cursor:'pointer', backgroundColor:'white', marginRight:'0px', padding: '10px 20px', fontSize: '12px', marginTop:'10px', fontWeight: 'bold' }}>Joe's Page</button>
                    <h1 style={{ textAlign: 'center', fontSize: '50px', fontWeight: 'bold' }}>Schedule Planner Thing</h1>
                    <button onClick={() => navigate('/InfoPage')} style={{cursor:'pointer', backgroundColor:'white', marginRight:'0px', padding: '10px 20px', fontSize: '12px', marginTop:'10px', fontWeight: 'bold' }}> Classes</button>
                    <button onClick={() => navigate('/FuturePlanner')} style={{cursor:'pointer', backgroundColor:'white', marginRight:'50px', padding: '10px 20px', fontSize: '12px', marginTop:'10px', fontWeight: 'bold' }}>Future Plan</button>
                </div>

                <div style={{ position: 'relative', width: '80%', minHeight: `${144 * 5}px`, margin: '0 auto', marginTop: '40px' }}>
                  {/* time labels*/}
                  <div style={{
                    position: 'absolute',
                    top: 0,
                    left: '-80px', 
                    width: '70px',
                    height: `${60 * 11}px`,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'flex-end',
                    zIndex: 10,
                    pointerEvents: 'none',
                    marginTop: '-30px',
                  }}>
                    {['8 am', '9 am', '10 am', '11 am', '12 pm', '1 pm', '2 pm', '3 pm', '4 pm', '5 pm', '6 pm'].map((label, idx) => (
                      <div key={label} style={{ height: '60px', fontSize: '20px', fontWeight: 'bold', display: 'flex', alignItems: 'center', justifyContent: 'flex-end', paddingRight: '10px' }}>
                        {label}
                      </div>
                    ))}
                  </div>
                  {/* day labels*/}
                  <div style={{
                    position: 'absolute',
                    top: '-40px',
                    left: 0,
                    width: '100%',
                    display: 'flex',
                    flexDirection: 'row',
                    justifyContent: 'space-between',
                    zIndex: 10,
                    pointerEvents: 'none',
                  }}>
                    {['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'].map((day, idx) => (
                      <div key={day} style={{ width: '100%', textAlign: 'center', fontSize: '20px', fontWeight: 'bold' }}>
                        {day}
                      </div>
                    ))}
                  </div>
  {/* grid lines */}
                <div style={{position: 'absolute', top: 0, left: 0, width: '100%', height: `${120 * 5}px`, zIndex: 0,
                     display: 'grid', gridTemplateRows: `repeat(120, 5px)`, gridTemplateColumns: `repeat(7, 1fr)`,
                  pointerEvents: 'none',  backgroundColor:'white'
                    }}>
    {Array.from({ length: 120 * 7 }).map((_, i) => {
      const rowIndex = Math.floor(i / 7);
      const colIndex = i % 7;
      return (
        <div
          key={`${rowIndex}-${colIndex}`}
          style={{
            borderTop: rowIndex % 12 === 0 ? '1px solid black' : 'none',
            borderLeft: '1px solid black',
            borderRight: colIndex === 6 ? '1px solid black' : 'none',
            borderBottom: rowIndex === 119 ? '1px solid black' : 'none',
            height: '5px',
            width: '100%',
            boxSizing: 'border-box',
          }}
        ></div>
      );
    })}
  </div>
  {/* Class blocks (absolutely positioned, zIndex: 1) */}
  {/* Class blocks */}
{classes.map((cls, classIdx) =>
    cls.times
        ? Object.entries(cls.times).map(([day, timeArr], timeIdx) => {
            if (!Array.isArray(timeArr) || timeArr.length !== 2) return null;
            const position = calcGridPosition({
                ...cls,
                day,
                start: timeArr[0],
                end: timeArr[1],
            });
            return (
                <div
                    key={`${classIdx}-${day}-${timeIdx}`}
                    style={{
                        position: 'absolute',
                        zIndex: 1,
                        top: `${(position.gridRow - 2) * 5}px`, // 5px per row, minus header rows
                        left: `${(position.gridColumn - 1) * (100 / 7)}%`,
                        height: `${(position.gridRowEnd.split(' ')[1] || 1) * 5}px`,
                        width: `${100 / 7}%`,
                        backgroundColor: colors[classIdx % colors.length],
                        border: '1px solid #333',
                        borderRadius: '4px',
                        display: 'flex',
                        flexDirection: 'column',
                        justifyContent: 'center',
                        alignItems: 'center',
                        textAlign: 'center',
                        overflow: 'hidden',
                    }}
                >
                    <div style={{ fontWeight: 'bold', fontSize:'15px'}}>{cls.name || `${cls.subject} ${cls.catalog}`}</div>
                    <div style={{fontSize:'12px'}}>{capitalizeWords(cls.instructor.toLowerCase())}</div>
                    
                </div>
            );
        })
        : null
)}
</div>

               

                
                {/*horizontal line*/}
                <hr style={{color:'black', backgroundColor:'black', height:'2px', border:'none', marginTop:'-50px'}}/>

           

                {/*search area*/}
                <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: '30px', gap: '20px' }}>   
                    
                    {/*dept dropdown*/}
                    <h1 style={{fontSize:'25px'}}>Search for Class:</h1>
                    <select value={dropdown} onChange={handleChange} style={{ cursor:'pointer', width: '250px', height: '30px', border:'2px solid black' }}>
                        {subjects.map((subject, idx) => (
                            <option key={idx} value={subject}>
                                {subject}
                            </option>
                        ))}
                    </select>
                    
                    {/*class dropdown*/}
                    <select value={dropdownClass} onChange={handleClassChange} style={{ cursor:'pointer', width: '140px', height: '30px', border:'2px solid black' }}>
                        {(classesPerSubject[dropdown] || []).map((catalog) => (
                        <option key={catalog} value={catalog}>
                                         {catalog}
                        </option>
                                 ))}
                    </select>
                    
                    {/*quarter dropdown*/}
                    <select value={quarter} onChange={handleQuarterChange} style={{ cursor:'pointer', width: '120px', height: '30px', border:'2px solid black' }}>
                        {quarterOptions.map((opt) => (
                            <option key={opt.value} value={opt.value}>
                                {opt.label}
                            </option>
                        ))}
                    </select>
                    
                    {/*search button*/}
                    <button style={{ width: '100px', height: '30px', backgroundColor: 'white', border: '2px solid black', borderRadius: '4px', fontSize: '14px', cursor: 'pointer', marginLeft:'40px' }} onClick={()=> handleClassQuery()}>Search</button>    
                </div>

                
                {/*horizontal line*/}
                 <hr style={{color:'black', backgroundColor:'black', height:'2px', border:'none', marginTop:'30px'}}/>
                            

                {/*everything below this is for rendering class search results*/}
                <div style={{ marginTop: '20px', padding: '10px', background: '#f0f0f0', border: '1px solid #ccc', borderRadius: '4px' }}>
  {Array.isArray(dataFromQuery) && dataFromQuery.length > 0 ? (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px' }}>
      {dataFromQuery.map((item, idx) => (
        <div key={idx} style={{ border: '1px solid #aaa', borderRadius: '8px', padding: '16px', background: '#f9f9f9', boxShadow: '0 2px 8px rgba(0,0,0,0.05)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '20px' }}>
            <span style={{ textAlign: 'left' }}>{item.subject} {item.catalog}</span>
            <span style={{ textAlign: 'right', fontWeight: 'normal', fontSize: '16px', color: 'black' }}>{item.term}</span>
          </div>
          <div style={{fontSize:'15px'}}>{capitalizeWords(item.instructor?.toLowerCase() || '')}</div>
          {/* Render times */}
          <div>
            {item.times && typeof item.times === 'object' ? (
              <div>
                {Object.entries(item.times)
                  .sort(([a], [b]) => dayOrder.indexOf(a) - dayOrder.indexOf(b))
                  .map(([day, time]) => {
                    let timeText = '';
                    if (Array.isArray(time) && time.length === 2) {
                      timeText = makeTimeNice(time);
                    } else if (typeof time === 'string') {
                      timeText = makeTimeNice(time);
                    } else {
                      timeText = String(time);
                    }
                    return (
                      <div key={day} style={{fontSize:'15px'}}>
                        <span style={{fontSize:'15px'}}>{capitalizeWords(day.toLowerCase())}:</span> {timeText}
                      </div>
                    );
                  })}
              </div>
            ) : (
              <div>{String(item.times)}</div>
            )}
          </div>
          <button style={{ marginTop: '10px' }} onClick={() => {
            addClass(id._id, item._id, "add");
            setDataFromQuery(prev => prev.filter(i => i._id !== item._id));
            runGetClasses(id._id);
          }}>Add to Plan</button>
        </div>
      ))}
    </div>
  ) : typeof dataFromQuery === 'object' && dataFromQuery !== null && Object.keys(dataFromQuery).length > 0 ? (
    <div style={{ display: 'flex', justifyContent: 'center' }}>
      <div style={{ border: '1px solid #aaa', borderRadius: '8px', padding: '16px', background: '#f9f9f9', boxShadow: '0 2px 8px rgba(0,0,0,0.05)' }}>
        {Object.entries(dataFromQuery).map(([key, value]) => (
          <div key={key} style={{ marginBottom: '8px' }}>
            <span style={{ fontWeight: 'bold', color: '#333' }}>{key}: </span>
            <span style={{ color: '#555' }}>{String(value)}</span>
          </div>
        ))}
      </div>
    </div>
  ) : (
    <span>{String(dataFromQuery)}</span>
  )}
</div>
           
            
               
            </div>

            
            <div style={{ position: 'fixed', right: 0, top: 0, width: '10%', backgroundColor: '#9cbcc5', height: '100vh', zIndex: 1 }}></div>





            {/*error popup*/}
            {popup && (<>
            <div style={{ position: 'fixed', top: 0, left: 0, width: '100%', height: '100%', backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 999 }}>
                <div style={{ position: 'fixed', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', backgroundColor: '#fff', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)', zIndex: 1000, minWidth: '300px' }}>
                    <button onClick={() => setPopup(false)}
                        style={{ position: 'absolute', top: 10, right: 10, background: 'none', border: 'none', fontSize: '24px', color: '#888', cursor: 'pointer', fontWeight: 'bold' }}
                        aria-label="Close error popup"
                    >
                        ×
                    </button>
                    <h2 style={{ marginTop: '10px' }}>Error</h2>
                    <p>{error}</p>
                </div>
                </div>
                </>
            )}






        </div>
    );
}

export default Home;