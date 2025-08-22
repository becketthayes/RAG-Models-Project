import './App.css';
import React from 'react';
import CreateModelForm from './components/CreateModelForm';
import TopBar from './components/TopBar';

function App() {
  return (
    <div className="page-layout">
      <TopBar />
      <div className="main-content">
        <CreateModelForm />
      </div>
    </div>
  );
}

export default App;
