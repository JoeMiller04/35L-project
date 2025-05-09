import { Routes, Route } from 'react-router-dom'; // No need for BrowserRouter here
import './App.css';
import Home from './Home';
import SearchPage from './SearchPage';
import InfoPage from './InfoPage';
import LogIn from './LogIn';
import CreateUser from './CreateUser'; // Import the CreateUser component

function Navigation() {
  return (
    <div>
     
    <Routes>
      <Route path="/" element={<LogIn />} /> {/* Default route */}
      <Route path="/Home" element={<Home />} />
      <Route path="/SearchPage" element={<SearchPage />} />
      <Route path="/InfoPage" element={<InfoPage />} />
      <Route path="/CreateUser" element={<CreateUser />} /> 
    </Routes>
    </div>
  );
}

export default Navigation;


