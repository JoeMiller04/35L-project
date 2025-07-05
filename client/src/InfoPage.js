import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';

//this page should be mostly done. It is the page to remove classes



function InfoPage() {
    const navigate = useNavigate();
    const [classes, setClasses] = useState([]);
    const [id, setId] = useState(null);
    const dayOrder = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];


    useEffect(() => {
            const userObj = JSON.parse(sessionStorage.getItem('user_id'));
            if (userObj && userObj._id) {
                setId(userObj._id);
                setClasses([]);
                runGetClasses(userObj._id);
            }
        }, []);

    

    async function getClasses(userId) {
        setClasses([]);
        if (!userId) {
            userId = JSON.parse(sessionStorage.getItem('user_id'));
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
            console.log('Error fetching user course list: ' + err.message);
        }
    }


    function runGetClasses(userId) {
        getClasses(userId);
    }

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

    function capitalizeWords(str) {
        return str.replace(/\b\w/g, c => c.toUpperCase());
    }

    async function updateUserCourseList(userId, courseId) {
        if (!userId) {
            userId = JSON.parse(sessionStorage.getItem('user_id'));
            userId = userId._id;
            setId(userId);
        }
        try {
            const response = await fetch(`http://127.0.0.1:8000/users/${userId}/course-list`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ course_id: courseId, action:"remove" }),
              
            });
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to update course list');
            }
            setClasses([]);
            runGetClasses(userId);
            return await response.json();

        } catch (err) {
            console.log(userId);
            console.log('Error: ' + err.message);
        }
    }

    function removeClass(courseId) {
            updateUserCourseList(id, courseId);
    }




    return (
        <div>
             <div style={{ display: 'flex', backgroundColor: '#f0f0f0', minHeight: '100vh' }}>
                <div style={{ position: 'fixed', left: 0, top: 0, width: '10%', backgroundColor: '#9cbcc5', height: '100vh', zIndex: 1 }}></div>
                <div style={{ width: '80%', marginLeft: '10%', marginRight: '10%', zIndex: 2 }}>

                            {/*upper area*/}
                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative', width: '100%', marginBottom: '20px' }}>
              {/* Left button group */}
              <div style={{ display: 'flex', alignItems: 'center', position: 'absolute', left: 0, height: '100%' }}>
                <button onClick={() => navigate('/')} style={{ cursor: 'pointer', backgroundColor: 'white', marginLeft: '50px', padding: '10px 20px', fontSize: '12px', marginTop: '10px', fontWeight: 'bold' }}>Go to Home</button>
              </div>
              {/* Centered title */}
              <div style={{ flex: 1, display: 'flex', justifyContent: 'center' }}>
                <h1 style={{ textAlign: 'center', fontSize: '50px', fontWeight: 'bold', margin: 0 }}>Current Class Information</h1>
              </div>
              {/* Right button group (placeholder for symmetry) */}
              <div style={{ display: 'flex', alignItems: 'center', position: 'absolute', right: 0, height: '100%' }}>
                <button style={{ marginRight: '50px', fontSize: '12px', marginTop: '10px', borderWidth: '0px', width: '90px', backgroundColor: 'white', fontWeight: 'bold' }}></button>
              </div>
            </div>


        {/*class rendering*/}
                            {Array.isArray(classes) && classes.length > 0 ? (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '20px', marginRight: '20px', marginLeft:'20px' }}>
      {classes.map((item, idx) => (
        <div key={idx} style={{ border: '1px solid #aaa', borderRadius: '8px', padding: '16px', background: '#f9f9f9', boxShadow: '0 2px 8px rgba(0,0,0,0.05)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '20px' }}>
            <span style={{ textAlign: 'left' }}>{item.subject} {item.catalog} - {item.title}</span>
            <span style={{ textAlign: 'right', fontWeight: 'normal', fontSize: '16px', color: 'black' }}>{item.term}</span>
          </div>
          <div style={{fontSize:'15px'}}>{capitalizeWords(item.instructor?.toLowerCase() || '')}</div>
          {/* Render times */}
          <div>
            {item.times && typeof item.times === 'object' ? (
              <div>
                {Object.entries(item.times)
                  .sort(([a], [b]) => dayOrder.indexOf(a) - dayOrder.indexOf(b))
                  .map(([day, time]) =>{
                  let timeText = '';
                  if (Array.isArray(time) && time.length === 2) {
                    timeText = makeTimeNice(time);
                  } else if (typeof time === 'string') {
                    timeText = makeTimeNice(time);
                  } else {
                    timeText = String(time);
                  }
                  
                  return (
                    <div key={day} style={{fontSize:'13px'}}>
                        <span style={{fontSize:'13px'}}>{capitalizeWords(day.toLowerCase())}:</span> {item.times === null ? 'Missing time information' : timeText}
                    </div>
                  );
                })}
              </div>
            ) : (
              <div style={{fontSize:'13px'}}>{String("Missing Time Information")}</div>
            )}
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '10px' }}>
          <button style={{ marginTop: '10px', background:'white', cursor:'pointer' }} onClick={() => {
            removeClass(item._id);
            setClasses(prev => prev.filter(i => i._id !== item._id));
            runGetClasses(id._id);
          }}>Remove Class</button>
           <button style={{ backgroundColor:'white', cursor:'pointer' }} onClick={() => {
              navigate('/SearchPage', { state: { classInfo: item } });
            }}> More Info</button>
            </div>
        </div>
      ))}
    </div>
  ) : typeof classes === 'object' && classes !== null && Object.keys(classes).length > 0 ? (
    <div style={{ display: 'flex', justifyContent: 'center' }}>
      <div style={{ border: '1px solid #aaa', borderRadius: '8px', padding: '16px', background: '#f9f9f9', boxShadow: '0 2px 8px rgba(0,0,0,0.05)' }}>
        {Object.entries(classes).map(([key, value]) => (
          <div key={key} style={{ marginBottom: '8px' }}>
            <span style={{ fontWeight: 'bold', color: '#333' }}>{key}: </span>
            <span style={{ color: '#555' }}>{String(value)}</span>
          </div>
        ))}
      </div>
    </div>
  ) : (
    <span>{String(classes)}</span>
  
  
  )}
            </div>
            <div style={{ position: 'fixed', right: 0, top: 0, width: '10%', backgroundColor: '#9cbcc5', height: '100vh', zIndex: 1 }}></div>
            </div>
        </div>
    );
}

export default InfoPage;