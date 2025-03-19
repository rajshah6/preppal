import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AboutPage from './components/AboutPage';
import GetStarted from './components/GetStarted';
import PracticeQuestion from './components/Practice';
import Feedback from './components/Feedback';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import { Analytics } from "@vercel/analytics/react";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/Login" element={<Login />} />
        <Route path="/" element={<AboutPage />} />
        <Route path="/get-started" element={<GetStarted />} />
        <Route path="/practice" element={<PracticeQuestion />} />
        <Route path="/feedback" element={<Feedback />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Analytics />
      </Routes>
    </Router>
  );
};

export default App;