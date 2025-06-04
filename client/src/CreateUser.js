import { useNavigate } from 'react-router-dom';
import {useState} from 'react';
import './App.css'; 


function CreateUser() {
    //for navigation
    const navigate = useNavigate();

    //variables for login
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [passwordCheck, setPasswordCheck] = useState('');
    const [error, setError] = useState(false);
    const [userAlreadyExists, setUserAlreadyExists] = useState(false);
    const [passwordLengthError, setPasswordLengthError] = useState(false);
    const [userTooShort, setUserTooShort] = useState(false);


    //function that calls backend createUser function
    async function createUserLink(username, password) {
        try {
            const response = await fetch('http://127.0.0.1:8000/users', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password,
                }),
            });

            if (response.ok) {
                const data = await response.json();
                setError(false);
                setUserAlreadyExists(false);
                setPasswordLengthError(false);
                setUserTooShort(false);
                navigate('/'); // Redirect to login page after successful creation
            } else if (response.status === 400) {
                setError(false);
                setPasswordLengthError(false);
                setUserTooShort(false);
                setUserAlreadyExists(true); // Handle username already exists error
                
                
            } else {
                alert('Failed to create user');
                
            }
        } catch (error) {
            alert('Error:' + error.message);
        }
    }

    //function to handle user creation
    function handleCreateUser() {
        if (password !== passwordCheck) {
            setUserAlreadyExists(false);
            setPasswordLengthError(false);
            setUserTooShort(false);
            setError(true);
            return;
        } else {
            setError(false);
        }

        if (false) { //Change this to password.length < 8 later
            setError(false);
            setUserAlreadyExists(false);
            setUserTooShort(false);
            setPasswordLengthError(true);
            return;

        }

        if (username.length < 1) {
            setError(false);
            setUserAlreadyExists(false);
            setPasswordLengthError(false);
            setUserTooShort(true);
            return;
        }

        createUserLink(username, password); // Call the API function
    }

    //return statement

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '50px' }}>
            <h1 style={{ textAlign: 'center', marginBottom: '40px', marginTop:'100px', fontSize: '45px' }}>Create a New User</h1>

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
                style={{ marginBottom: '10px', padding: '10px', width: '300px' }}
            />

            <input
                type="password"
                placeholder="Confirm Password"
                value={passwordCheck}
                onChange={(e) => setPasswordCheck(e.target.value)}
                style={{ marginBottom: '10px', padding: '10px', width: '300px' }}
            />

            <div style={{ display: 'flex', flexDirection: 'row', gap: '10px', marginTop: '10px' }}>
                
             <button
                    onClick={() => {
                        navigate('/');
                        setError(false);
                        setUserAlreadyExists(false);
                        setPasswordLengthError(false);
                        setUserTooShort(false);
                    }}
                    style={{ padding: '10px 20px', fontSize: '16px', cursor:'pointer' }}
                >
                    Back to Log In
                </button>
                
                <button
                    onClick={() => handleCreateUser()}
                    style={{ padding: '10px 20px', fontSize: '16px', cursor:'pointer' }}
                
                >
                    Create User
                </button>

                
            </div>

            {error && <p style={{ color: 'red' }}>Passwords do not match</p>}
            {userAlreadyExists && <p style={{ color: 'red' }}>Username already exists</p>}
            {passwordLengthError && <p style={{ color: 'red' }}>Password must be at least 8 characters long</p>}
            {userTooShort && <p style={{ color: 'red' }}>Username must be at least 1 character long</p>}
        </div>
    )
}

export default CreateUser;