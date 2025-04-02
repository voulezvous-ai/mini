import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import PromptOSApp from './pages/PromptOSApp';
import LandingPage from './landing/index.html';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/app" element={<PromptOSApp />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;