import { useNavigate } from 'react-router-dom';
import {useState} from 'react';
import './App.css';


function LogIn() {
    //for navigation
    const navigate = useNavigate();

    //variables for login
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [noUserOrPassword, setNoUserOrPassword] = useState(false);
    const [incorrectInfo, setIncorrectInfo] = useState(false);
    const [data, setData] = useState(null);


    //function that calls backend login function
    async function loginLink(username, password) {
        try {
            const response = await fetch(`http://127.0.0.1:8000/login?username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                navigate('/Home'); // Redirect to the home page after successful login
                localStorage.setItem('user_id', JSON.stringify(data));
            } else if (response.status === 401) {
                setNoUserOrPassword(false);
                setIncorrectInfo(true); // Handle incorrect username or password
            } else {
                console.log('Failed to log in');
            }
        } catch (error) {
            console.log('Error: ' + error.message);
        }
    }

    //handle log in function
    function handleLogin() {

        if (username === '' || password === '') {
            setIncorrectInfo(false);
            setNoUserOrPassword(true);
            return;
        }
        
        loginLink(username, password);


    }

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '50px' }}>
            <h1 style={{ textAlign: 'center', marginBottom: '40px', marginTop:'100px', fontSize: '45px' }}>Sign In</h1>

            <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                style={{ marginBottom: '10px', padding: '10px', width: '300px' }}
            />

            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={{ marginBottom: '20px', padding: '10px', width: '300px' }}
            />

            <div style={{ display: 'flex', flexDirection: 'row', gap: '10px', marginTop: '10px' }}>
                 <button
                    onClick={() => navigate('/CreateUser')}
                    style={{ padding: '10px 20px', fontSize: '16px', cursor:'pointer' }}
                >
                    Create User
                </button>
                <button
                    onClick={() => handleLogin()}
                    style={{ padding: '10px 20px', fontSize: '16px', cursor:'pointer' }}
                >
                    Log In
                </button>

                
            </div>

            {noUserOrPassword && (<div style={{ color: 'red', marginTop: '10px' }}>Please enter a username and password.</div>)}
            {incorrectInfo && (<div style={{ color: 'red', marginTop: '10px' }}>Incorrect username or password.</div>)}
 
        </div>
    )
}

export default LogIn;