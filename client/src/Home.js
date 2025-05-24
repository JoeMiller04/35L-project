import { useNavigate } from 'react-router-dom';
import './App.css';
import { useState, useEffect } from 'react';
import {COMSCIClassOptions, MATHClassOptions, ECENGRClassOptions, PHYSICSClassOptions} from './ClassesLists'

function Home() {
    const navigate = useNavigate();
    const [classes, setClasses] = useState([]);
    const colors = ['#FFD1DC', '#FFABAB', '#FFC3A0', '#FF677D', '#D4A5A5', '#392F5A', '#31A2AC', '#61C0BF', '#6B4226', '#D9BF77'];
    const [index, setIndex] = useState(-1);
    const [dropdown, setDropdown] = useState("");
    const [dropdownClass, setDropdownClass] = useState("");
    const [quarter, setQuarter] = useState("25S");
    const [dataFromQuery, setDataFromQuery] = useState([]);

    // Run changeColor every time a new class is rendered
    useEffect(() => {
        if (classes.length > 0) {
            changeColor();
        }
    }, [classes, index]); 

    // update class list when user loads in
    useEffect(() => {
        setClasses([]);
        fetchClasses();
      
    }, []);

    async function fetchClasses() {

        setClasses([]);

        



    }

    //Get grid column and row for each class
    function calcGridPosition(clas) {
        const startRow = getTimeRow(clas.start);
        const endRow = getTimeRow(clas.end);
        return {
            gridColumn: getDayColumn(clas.day),
            gridRow: startRow,
            gridRowEnd: `span ${endRow - startRow}`, // Span rows based on duration
        };
    }

    //Process time for text
    function makeTimeNice(time) {
        function format(t) {
            t = t.toString().padStart(4, '0');
            let hour = parseInt(t.slice(0, 2), 10);
            let min = t.slice(2);
            let ampm = hour <= 12 ? 'AM' : 'PM';
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
        }
    }

    const classOptionsMap = {
         COMSCI: COMSCIClassOptions,
         MATH: MATHClassOptions, 
         ECENGR: ECENGRClassOptions, 
         PHYSICS: PHYSICSClassOptions

    };

    const classOptions = [
         { value: '', label: '— Select Dept —' }
    ]


    //query class function
    async function classQuery() {

        let temp = dropdown;
        if (temp === "COMSCI") {
            temp = "COM SCI";
        } else if (temp === "ECENGR") {
            temp = "EC ENGR";
        }
        const params = new URLSearchParams({
            term: quarter,
            subject: temp,
            catalog: dropdownClass
        });
       
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
              
            } else if (response.status === 400) {
                alert("NOOO")
                
                
            } else {
                alert(response.status);
                
            }
        } catch (error) {
            alert('Error:' + error.message);
        }
        }
    

    //get row from time
    function getTimeRow(time) {
        const hour = parseInt(time.slice(0, 2), 10);
        const minute = parseInt(time.slice(2), 10);
        let row = 0;
        row = 2 + (hour - 8) * 4;
        if (minute === 15) {
            row += 1;
        } else if (minute === 30) {
            row += 2;
        } else if (minute === 45) {
            row += 3;
        }

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

    const options = [
    { value: '', label: '— Select a Department —' },
    { value: 'COMSCI', label: 'Computer Science (COM SCI)' },
    {value: 'ECENGR', label:'Electrical Engineering (EC ENGR)'}
    , {value:'PHYSICS', label:'Physics (PHYSICS)'}, 
    {value:'MATH', label:'Mathematics (MATH)'}
    
  ];

  

  const quarterOptions = [
    { value: '25S', label: 'Spring 2025' }
   
  ];

    //dropdown change function
    function handleChange(drop) {
        setDropdown(drop.target.value);
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
    
    return (
        <div style={{ display: 'flex', backgroundColor: '#f0f0f0', minHeight: '100vh' }}>
        <div style={{ position: 'fixed', left: 0, top: 0, width: '10%', backgroundColor: '#9cbcc5', height: '100vh', zIndex: 1 }}></div>
        <div style={{ width: '80%', marginLeft: '10%', marginRight: '10%', zIndex: 2 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <button onClick={() => navigate('/PastCourses')} style={{marginLeft:'50px', padding: '10px 20px', fontSize: '16px', marginTop:'10px' }}>Degree Information</button>
                    <h1 style={{ textAlign: 'center', fontSize: '50px' }}>Schedule Planner Thing</h1>
                    <button onClick={() => navigate('/InfoPage')} style={{marginRight:'50px', padding: '10px 20px', fontSize: '16px', marginTop:'10px' }}>Future Requirements</button>
                </div>

                <div className='grid'>
                    <div className='daysOfWeekTitle'>Sunday</div>
                    <div className='daysOfWeekTitle'>Monday</div>
                    <div className='daysOfWeekTitle'>Tuesday</div>
                    <div className='daysOfWeekTitle'>Wednesday</div>
                    <div className='daysOfWeekTitle'>Thursday</div>
                    <div className='daysOfWeekTitle'>Friday</div>
                    <div className='daysOfWeekTitle'>Saturday</div>

                    {/* Render the grid lines */}
                    {Array.from({ length: 40 }).map((_, rowIndex) => (
                        Array.from({ length: 7 }).map((_, colIndex) => (
                            <div
                                key={`${rowIndex}-${colIndex}`}
                                style={{
                                    borderTop: rowIndex % 4 === 0 ? '1px solid black' : 'none',
                                    borderLeft: '1px solid black',
                                    borderRight: colIndex === 6 ? '1px solid black' : 'none',
                                    borderBottom: rowIndex === 39 ? '1px solid black' : 'none',
                                    height: '15px',
                                }}
                            ></div>
                        ))
                    ))}

                    {/*time labels*/}
                    <h1 style={{position:'absolute', top:'10px', left:'-62px', fontSize:'20px'}}>8 am</h1>
                    <h1 style={{position:'absolute', top:'70px', left:'-62px', fontSize:'20px'}}>9 am</h1>
                    <h1 style={{position:'absolute', top:'130px', left:'-75px', fontSize:'20px'}}>10 am</h1>
                    <h1 style={{position:'absolute', top:'190px', left:'-75px', fontSize:'20px'}}>11 am</h1>
                    <h1 style={{position:'absolute', top:'250px', left:'-75px', fontSize:'20px'}}>12 pm</h1>
                    <h1 style={{position:'absolute', top:'310px', left:'-64px', fontSize:'20px'}}>1 pm</h1>
                    <h1 style={{position:'absolute', top:'370px', left:'-64px', fontSize:'20px'}}>2 pm</h1>
                    <h1 style={{position:'absolute', top:'430px', left:'-64px', fontSize:'20px'}}>3 pm</h1>
                    <h1 style={{position:'absolute', top:'490px', left:'-64px', fontSize:'20px'}}>4 pm</h1>
                    <h1 style={{position:'absolute', top:'550px', left:'-64px', fontSize:'20px'}}>5 pm</h1>
                    <h1 style={{position:'absolute', top:'610px', left:'-64px', fontSize:'20px'}}>6 pm</h1>

                    {/* Render the class blocks */}
                    {classes.map((cls, index) => {
                        const position = calcGridPosition(cls);
                        return (
                            <div
                                key={index}
                                style={{
                                    position: 'absolute', 
                                    top: `${40 + (position.gridRow - 2) * 15}px`, 
                                    left: `${(position.gridColumn - 1) * (100 / 7)}%`, 
                                    height: `${(position.gridRowEnd.split(' ')[1] || 1) * 15}px`,
                                    width: `${100 / 7}%`, 
                                    border: '1px solid red',
                                    backgroundColor: colors[index], 
                                    display: 'flex', 
                                    justifyContent: 'center', 
                                    alignItems:'center', 
                                    textAlign: 'center'
                                    
                                }}
                            >
                                {cls.name}
                                <br />
                                {cls.location}
                            </div>
                        );
                    })}
                </div>

                {/*validate schedule button*/}
                <div style={{ display: 'flex', justifyContent: 'left', alignItems: 'center', marginTop: '30px', gap: '20px' , marginLeft:'300px'}}>
                    <button style={{ width: '170px', height: '40px', backgroundColor: 'white', border: '2px solid black', borderRadius: '4px', fontSize: '14px', cursor: 'pointer', marginLeft:'75px' }}>Validate Schedule</button>
                </div>

                
                {/*horizontal line*/}
                <hr style={{color:'black', backgroundColor:'black', height:'4px', border:'none', marginTop:'20px'}}/>

           

                {/*search area*/}
                <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: '30px', gap: '20px' }}>   
                    
                    {/*dept dropdown*/}
                    <h1 style={{fontSize:'25px'}}>Search for Class:</h1>
                    <select value={dropdown} onChange={handleChange} style={{ width: '250px', height: '30px', border:'2px solid black' }}>
                        {options.map((opt) => (
                            <option key={opt.value} value={opt.value}>
                                {opt.label}
                            </option>
                        ))}
                    </select>
                    
                    {/*class dropdown*/}
                    <select value={dropdownClass} onChange={handleClassChange} style={{ width: '140px', height: '30px', border:'2px solid black' }}>
                        {(classOptionsMap[dropdown]||classOptions).map((opt) => (
                            <option key={opt.value} value={opt.value}>
                                {opt.label}
                            </option>
                        ))}
                    </select>
                    
                    {/*quarter dropdown*/}
                    <select value={quarter} onChange={handleQuarterChange} style={{ width: '120px', height: '30px', border:'2px solid black' }}>
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
                 <hr style={{color:'black', backgroundColor:'black', height:'4px', border:'none', marginTop:'30px'}}/>
                            

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
          <div style={{fontSize:'15px'}}>{capitalizeWords(item.instructor.toLowerCase())}</div>
          
          {/*this is to map the time object to text*/}
          <div>
            {item.times && typeof item.times === 'object' ? (
              <div>
                {Object.entries(item.times).map(([day, time]) => (
                    
                  <div key={day} style={{fontSize:'15px'}}>
                    <span style={{fontSize:'15px'}}>{capitalizeWords(day.toLowerCase())}:</span> {makeTimeNice(time)} 
                  </div>
                   
                ))}
              </div>
            ) : (
              <div>{item.times}</div>
            )}
          </div>



          
          <button style={{}}>Add to Plan</button>


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
    <span>{dataFromQuery}</span>
  )}
</div>









           
            
               
            </div>

            
            <div style={{ position: 'fixed', right: 0, top: 0, width: '10%', backgroundColor: '#9cbcc5', height: '100vh', zIndex: 1 }}></div>

       
        </div>
    );
}

export default Home;