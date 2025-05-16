import { useNavigate } from 'react-router-dom';
import './App.css';
import { useState, useEffect } from 'react';

function Home() {
    const navigate = useNavigate();
    const [classes, setClasses] = useState([{ name: "PHYSICS 1C Lec 2", day: "Monday", start: "1400", end: "1515", location: "Kinsey Science Teaching" }, {name:"CS35L", day: "Tuesday", start:"1600", end:"1800", location:"Franz"}]);
    const colors = ['#FFD1DC', '#FFABAB', '#FFC3A0', '#FF677D', '#D4A5A5', '#392F5A', '#31A2AC', '#61C0BF', '#6B4226', '#D9BF77'];
    const [index, setIndex] = useState(-1);
    const [dropdown, setDropdown] = useState("");
    const [dropdownClass, setDropdownClass] = useState("");
    const [quarter, setQuarter] = useState("S25");

    // Run changeColor every time a new class is rendered
    useEffect(() => {
        if (classes.length > 0) {
            changeColor();
        }
    }, [classes, index]); 

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
    { value: 'COM SCI', label: 'Computer Science (COM SCI)' },
    
  ];

  const classOptions = [
    { value: '', label: '— Select Class —' },
    { value: '31', label: '31' },
    {value: '32', label:'32'}
    
  ];

  const quarterOptions = [
    { value: 'S25', label: 'Spring 2025' }
   
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

    
    return (
        <div style={{ display: 'flex', backgroundColor: '#f0f0f0', minHeight: '100vh' }}>
            <div style={{ width: '10%', backgroundColor: '#9cbcc5', height: '200vh' }}></div>
            <div style={{ width: '80%' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <button onClick={() => navigate('/SearchPage')} style={{marginLeft:'50px', padding: '10px 20px', fontSize: '16px', marginTop:'10px' }}>Edit Class History</button>
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
                <div style={{ display: 'flex', justifyContent: 'left', alignItems: 'center', marginTop: '30px', gap: '20px' , marginLeft:'300px'}}>
                    <h1 style={{fontSize:'25px'}}>Select Quarter:</h1>
                    <select value={quarter} onChange={handleQuarterChange} style={{ width: '120px', height: '30px', border:'2px solid black' }}>
                        {quarterOptions.map((opt) => (
                            <option key={opt.value} value={opt.value}>
                                {opt.label}
                            </option>
                        ))}
                    </select>
                    <button style={{ width: '170px', height: '40px', backgroundColor: 'white', border: '2px solid black', borderRadius: '4px', fontSize: '14px', cursor: 'pointer', marginLeft:'75px' }}>Validate Schedule</button>
                </div>

                

                <hr style={{color:'black', backgroundColor:'black', height:'4px', border:'none', marginTop:'20px'}}/>

                {/*working on dropdown search*/}
                <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: '30px', gap: '20px' }}>
                    {/*Quarter dropdown*/}
                    
                    {/*class dropdown*/}
                    <h1 style={{fontSize:'25px'}}>Search for Class:</h1>
                    <select value={dropdown} onChange={handleChange} style={{ width: '250px', height: '30px', border:'2px solid black' }}>
                        {options.map((opt) => (
                            <option key={opt.value} value={opt.value}>
                                {opt.label}
                            </option>
                        ))}
                    </select>

                    <select value={dropdownClass} onChange={handleClassChange} style={{ width: '140px', height: '30px', border:'2px solid black' }}>
                        {classOptions.map((opt) => (
                            <option key={opt.value} value={opt.value}>
                                {opt.label}
                            </option>
                        ))}
                    </select>
                </div>

                 <hr style={{color:'black', backgroundColor:'black', height:'4px', border:'none', marginTop:'30px'}}/>
                        
            </div>
            <div style={{ width: '10%', backgroundColor: '#9cbcc5', height: '200vh' }}></div>
        </div>
    );
}

export default Home;