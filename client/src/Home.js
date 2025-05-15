import { useNavigate } from 'react-router-dom';
import './App.css';
import { useState, useEffect } from 'react';

function Home() {
    const navigate = useNavigate();
    const [classes, setClasses] = useState([{ name: "PHYSICS 1C Lec 2", day: "Monday", start: "1400", end: "1515", location: "Kinsey Science Teaching" }, {name:"CS35L", day: "Tuesday", start:"1600", end:"1800", location:"Franz"}]);
    const colors = ['#FFD1DC', '#FFABAB', '#FFC3A0', '#FF677D', '#D4A5A5', '#392F5A', '#31A2AC', '#61C0BF', '#6B4226', '#D9BF77'];
    const [index, setIndex] = useState(-1);

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

    
    return (
        <div>
            <h1 style={{ textAlign: 'center', fontSize: '50px' }}>Schedule Planner Thing</h1>

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

            <button onClick={() => navigate('/SearchPage')}>Go to Home2</button>
            <button onClick={() => navigate('/InfoPage')}>Go to Home3</button>
            <button onClick={() => navigate('/PastCourses')}>Go to Home3</button>
        </div>
    );
}

export default Home;