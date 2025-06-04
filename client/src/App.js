import { Routes, Route } from 'react-router-dom'; // No need for BrowserRouter here
import Home from './Home';
import SearchPage from './SearchPage';
import InfoPage from './InfoPage';
import LogIn from './LogIn';
import CreateUser from './CreateUser'; // Import the CreateUser component
import PastCourses from './PastCourses';
import FuturePlanner from './FuturePlanner';

function Navigation() {
  return (
    <div>
     
    <Routes>
      <Route path="/" element={<LogIn />} /> {/* Default route */}
      <Route path="/Home" element={<Home />} />
      <Route path="/SearchPage" element={<SearchPage />} />
      <Route path="/InfoPage" element={<InfoPage />} />
      <Route path="/CreateUser" element={<CreateUser />} /> 
      <Route path="/PastCourses" element={<PastCourses />} />
      <Route path="/FuturePlanner" element={<FuturePlanner />} />
    </Routes>
    </div>
  );
}

export default Navigation;


