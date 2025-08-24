import './App.css';
import React, { useState } from 'react';
import CreateModelForm from './components/CreateModelForm';
import TopBar from './components/TopBar';
import NavigationBar from './components/NavigationBar';

function App() {
  const [isCreating, setIsCreating] = useState(false);
  return (
    <div className="page-layout">
      <div className="main-content">
        {isCreating ? (
          <div className="form-container">
            <CreateModelForm />
          </div>
        ) : (
          <NavigationBar />
        )}
      </div>
    </div>
  );
}

export default App;
