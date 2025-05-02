import { Routes, Route } from 'react-router-dom'; // No need for BrowserRouter here
import './App.css';
import Home from './Home';
import Home2 from './Home2';
import Home3 from './Home3';

function Navigation() {
  return (
    <div>
      <h1>App is rendering</h1>
    <Routes>
      <Route path="/" element={<Home />} /> {/* Default route */}
      <Route path="/Home" element={<Home />} />
      <Route path="/Home2" element={<Home2 />} />
      <Route path="/Home3" element={<Home3 />} />
    </Routes>
    </div>
  );
}

export default Navigation;


