import styles from './App.module.css';
import { Routes, Route } from 'react-router-dom';
import Home from './components/Home';
import HowItWorks from './components/HowItWorks';
import NavBar from './components/NavBar';

function App() {
  return (
    <>
      <NavBar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/how-it-works" element={<HowItWorks />} />
      </Routes>
    </>
  );
}

export default App;
