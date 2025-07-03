import { useNavigate } from 'react-router-dom';
import React, { useState, useEffect } from 'react';


export default function PastCourses() {
  // Track which courses have been checked (i.e., taken by the user)
  const [takenCourses, setTakenCourses] = useState({});
  const [selectedDegree, setSelectedDegree] = useState('');
  const navigate = useNavigate();
  const userObj = JSON.parse(localStorage.getItem("user_id"));
  const userId = userObj._id;
  const [popup, setPopup] = useState(false);
  const [major, setMajor] = useState('');
  const [filePopup, setFilePopup] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [darsOutput, setDarsOutput] = useState(''); 

  


  const availableCourses = selectedDegree === 'CS' ? ["COM SCI 1","COM SCI 30","COM SCI 31","COM SCI 32","COM SCI 33","COM SCI 35L","COM SCI M51A","COM SCI 111","COM SCI 112","COM SCI 117","COM SCI 118","COM SCI M119","COM SCI C121","COM SCI C122","COM SCI C124","COM SCI 130","COM SCI 131","COM SCI 132","COM SCI 133","COM SCI 134","COM SCI 136","COM SCI C137A","COM SCI C137B","COM SCI M138","COM SCI 143","COM SCI 144","COM SCI 145","COM SCI M146","COM SCI M148","COM SCI M151B","COM SCI M152A","COM SCI 152B","COM SCI 161","COM SCI 162","COM SCI 163","COM SCI 168","COM SCI 170A","COM SCI M171L","COM SCI 172","COM SCI 174A","COM SCI 174B","COM SCI C174C","COM SCI 180","COM SCI 181","COM SCI M182","COM SCI 183","COM SCI M184","COM SCI CM186","COM SCI CM187","COM SCI 188","MATH 31A","MATH 31B","MATH 32A","MATH 32B","MATH 33A","MATH 33B","MATH 61","MATH 170A","MATH 170E","C&EE 110","STATS 100A","PHYSICS 1A","PHYSICS 1B","PHYSICS 1C","PHYSICS 4AL","PHYSICS 4BL","LIFESCI 30A","LIFESCI 30B","EC ENGR M16","EC ENGR 131A","EC ENGR 132B","EC ENGR M117","EC ENGR M116L","GE 1","GE 2","GE 3","GE 4","GE 5","TECH BREADTH 1","TECH BREADTH 2","TECH BREADTH 3","SCI TECH 1","SCI TECH 2","SCI TECH 3","ENGCOMP 3","ETHICS"] : selectedDegree === 'CSE' ? ["COM SCI 1","COM SCI 30","COM SCI 31","COM SCI 32","COM SCI 33","COM SCI 35L","COM SCI M51A","COM SCI 111","COM SCI 112","COM SCI 117","COM SCI 118","COM SCI M119","COM SCI C121","COM SCI C122","COM SCI C124","COM SCI 130","COM SCI 131","COM SCI 132","COM SCI 133","COM SCI 134","COM SCI 136","COM SCI C137A","COM SCI C137B","COM SCI M138","COM SCI 143","COM SCI 144","COM SCI 145","COM SCI M146","COM SCI M148","COM SCI M151B","COM SCI M152A","COM SCI 152B","COM SCI 161","COM SCI 162","COM SCI 163","COM SCI 168","COM SCI 170A","COM SCI M171L","COM SCI 172","COM SCI 174A","COM SCI 174B","COM SCI C174C","COM SCI 180","COM SCI 181","COM SCI M182","COM SCI 183","COM SCI M184","COM SCI CM186","COM SCI CM187","COM SCI 188","MATH 31A","MATH 31B","MATH 32A","MATH 32B","MATH 33A","MATH 33B","MATH 61","MATH 170A","MATH 170E","C&EE 110","STATS 100A","PHYSICS 1A","PHYSICS 1B","PHYSICS 1C","PHYSICS 4AL","PHYSICS 4BL","LIFESCI 30A","LIFESCI 30B","EC ENGR 3","EC ENGR M16","EC ENGR 100","EC ENGR 102","EC ENGR 115C","EC ENGR 131A","EC ENGR 132B","EC ENGR M117","EC ENGR M116L","GE 1","GE 2","GE 3","GE 4","GE 5","TECH BREADTH 1","TECH BREADTH 2","TECH BREADTH 3","ENGCOMP 3","ETHICS"] : [];

  const handleFileChange = (e) => {
      setSelectedFile(e.target.files[0]);
      setUploadStatus('');
     
  };
      
         
  const handleUpload = async () => {
      if (!selectedFile) {
          setUploadStatus('Please select a file first.');
          return;
      }
      const formData = new FormData();
      formData.append('file', selectedFile);
      try {
          setUploadStatus('Uploading...');
          const response = await fetch(`${process.env.REACT_APP_API_URL}/users/${userId}/upload`, {
              method: 'POST',
              body: formData,
          });
          if (response.ok) {
              const data = await response.json(); 
              setUploadStatus('Upload successful!');
              
              setDarsOutput(data);
              loadPastCourses();
          } else {
              setUploadStatus('Upload failed.');
              
          }
      } catch (error) {
          setUploadStatus('Error uploading file.');
          
      }


};
  

async function loadPastCourses() {
  try {
    const response = await fetch(`${process.env.REACT_APP_API_URL}/users/${userId}/courses`);
    const data = await response.json(); 
    
    const pastOnly = data.filter((entry) => entry.term === "PAST");

    const initial = {};
    pastOnly.forEach(({ course_name }) => {
      initial[course_name] = true;
    });

    setTakenCourses(initial);
  } catch (err) {
    console.error("Error loading past courses:", err);
  }
};

  useEffect(() => {
    const majorObj = JSON.parse(localStorage.getItem('major'));
    const majorStr = majorObj ? majorObj.major : 'CS';
    setSelectedDegree(majorStr);
    setMajor(majorStr);
    loadPastCourses();
  }, [userId]);

  // Toggle checkbox state and update the backend accordingly
  const toggleCourse = async (course) => {
    const isNowChecked = !takenCourses[course];

    // Update UI state immediately
    setTakenCourses((prev) => ({
      ...prev,
      [course]: isNowChecked,
    }));


    // Update backend with add/remove action
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/users/${userId}/courses`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          term: "PAST",
          course_name: course,
          action: isNowChecked ? 'add' : 'remove'
        })
      });

      if (!response.ok) throw new Error("Failed to update backend");
    } catch (err) {
      console.error("Error syncing course:", err);
    }
  };

  function toggleMajor() {
    setPopup(!popup);
  }

  function updateMajor(maj) {
    localStorage.setItem('major', JSON.stringify({major: maj}));
    setMajor(maj);
    setTakenCourses({}); 
  }

  function toggleFilePopup() {
    setFilePopup(!filePopup);
  }

  return (
    <div>
      <div style={{ display: 'flex', backgroundColor: '#f0f0f0', minHeight: '100vh' }}>
        <div style={{ position: 'fixed', left: 0, top: 0, width: '10%', backgroundColor: '#9cbcc5', height: '100vh', zIndex: 1 }}></div>
        <div style={{ width: '80%', marginLeft: '10%', zIndex: 2 }}>
    
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative', width: '100%', marginBottom: '20px', marginTop: '20px' }}>
       
          <div style={{ display: 'flex', alignItems: 'center', position: 'absolute', left: 0, height: '100%' }}>
            <button onClick={() => navigate('/Home')} style={{ cursor: 'pointer', backgroundColor: 'white', marginLeft: '50px', padding: '10px 20px', fontSize: '12px', marginTop: '10px', fontWeight: 'bold' }}>Home</button>
            <button onClick={() => toggleFilePopup()} style={{ cursor: 'pointer', backgroundColor: 'white', marginLeft: '20px', padding: '10px 20px', fontSize: '12px', marginTop: '10px', fontWeight: 'bold' }}>Upload</button>
          </div>
        
          <div style={{ flex: 1, display: 'flex', justifyContent: 'center' }}>
            <h1 style={{ textAlign: 'center', fontSize: '40px', fontWeight: 'bold', margin: 0 }}>Past Course Checklist</h1>
          </div>
     
          <div style={{ display: 'flex', alignItems: 'center', position: 'absolute', right: 0, height: '100%' }}>
            <button onClick={() => toggleMajor()} style={{ cursor: 'pointer', backgroundColor: 'white', marginRight: '20px', padding: '10px 20px', fontSize: '12px', marginTop: '10px', fontWeight: 'bold' }}>Change Major</button>
            <button onClick={() => navigate('/FuturePlanner')} style={{ cursor: 'pointer', backgroundColor: 'white', marginRight: '50px', padding: '10px 20px', fontSize: '12px', marginTop: '10px', fontWeight: 'bold' }}>Future Plan</button>
          </div>
        </div>
                <hr style={{color:'black', backgroundColor:'black', height:'1px', border:'none', marginTop:'0px'}}/>

           
            
     

  
{selectedDegree && (() => {

  const grouped = {};
  availableCourses.forEach((course) => {
    const lastSpaceIdx = course.lastIndexOf(' ');
    const dept = lastSpaceIdx !== -1 ? course.substring(0, lastSpaceIdx) : course;
    if (!grouped[dept]) grouped[dept] = [];
    grouped[dept].push(course);
  });

 
  const columns = [];
  Object.entries(grouped).forEach(([dept, courses]) => {
    for (let i = 0; i < courses.length; i += 10) {
      columns.push({
        dept,
        courses: courses.slice(i, i + 10),
      });
    }
  });

  
  return (
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '32px', marginTop: '24px', marginLeft:'80px' }}>
      {columns.map((col, idx) => (
        <div key={col.dept + idx} style={{ minWidth: 180 }}>
          <h3 style={{ textAlign: 'left', marginBottom:8 }}>{col.dept}</h3>
          <ul style={{ listStyle: 'none', padding: 0 , marginTop:'-5px'}}>
            {col.courses.map((course) => (
              <li key={course}>
                <input
                  type="checkbox"
                  id={course}
                  checked={takenCourses[course] || false}
                  onChange={() => toggleCourse(course)}
                />
                <label htmlFor={course} style={{ marginLeft: 4 }}>{course}</label>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
})()}


     
      </div>
            <div style={{ position: 'fixed', right: 0, top: 0, width: '10%', backgroundColor: '#9cbcc5', height: '100vh', zIndex: 1 }}></div>


      </div>

      




      
        {popup && (<>
            <div style={{ position: 'fixed', top: 0, left: 0, width: '100%', height: '100%', backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 999 }}>
                <div style={{ position: 'fixed', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', backgroundColor: '#fff', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)', zIndex: 1000, minWidth: '300px' }}>
                    <button onClick={() => toggleMajor()}
                        style={{ position: 'absolute', top: 10, right: 10, background: 'none', border: 'none', fontSize: '24px', color: '#888', cursor: 'pointer', fontWeight: 'bold' }}
                        aria-label="Close error popup"
                    >
                        ×
                    </button>
                    <h2 style={{ marginTop: '10px' }}>Select Your Major</h2>
                    <select value={selectedDegree} style={{marginLeft:'0px'}} onChange={(e) => { setSelectedDegree(e.target.value); updateMajor(e.target.value); loadPastCourses();}}>
                      
                    <option value="CS">Computer Science (CS)</option>
                     <option value="CSE">Computer Science and Engineering (CSE)</option>
                 </select>


                    
                </div>
                </div>
                </>
            )}

            
        {filePopup && (<>
            <div style={{ position: 'fixed', top: 0, left: 0, width: '100%', height: '100%', backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 999 }}>
                <div style={{ position: 'fixed', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', backgroundColor: '#fff', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)', zIndex: 1000, minWidth: '300px' }}>
                    <button onClick={() => toggleFilePopup()}
                        style={{ position: 'absolute', top: 10, right: 10, background: 'none', border: 'none', fontSize: '24px', color: '#888', cursor: 'pointer', fontWeight: 'bold' }}
                        aria-label="Close error popup"
                    >
                        ×
                    </button>
                    <h2 style={{ marginTop: '10px' }}>Upload a DARS File</h2>
                    
                      <div style={{ marginTop: '40px', textAlign: 'center' }}>
                        <input type="file" onChange={handleFileChange} />
                       <button onClick={handleUpload} style={{ marginLeft: '10px', padding: '8px 16px', fontSize: '16px', cursor: 'pointer' }}>Upload</button>
                     {uploadStatus && <div style={{ marginTop: '10px', color: uploadStatus.includes('successful') ? 'green' : 'red' }}>{uploadStatus}</div>}
                 </div>

                    
                </div>
                </div>
                </>
            )}




</div>
 
  
  );
}