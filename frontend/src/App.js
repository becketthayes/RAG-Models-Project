import './App.css';
import React, { useState } from 'react';
import CreateModelForm from './components/CreateModelForm';
import TopBar from './components/TopBar';
import CreateNewRAGModel from './components/CreateNewRAGModel';
import NavigationBar from './components/NavigationBar';
import { useAuth0 } from "@auth0/auth0-react";

function App() {
  const [isCreating, setIsCreating] = useState(false);
  const {
    isLoading, // Loading state, the SDK needs to reach Auth0 on load
    isAuthenticated,
    error,
    loginWithRedirect: login, // Starts the login flow
    logout: auth0Logout, // Starts the logout flow
    user, // User profile
  } = useAuth0();

  const handleModelCreate = () => {
    setIsCreating(prevIsCreating => !prevIsCreating)
  }


  const signup = () =>
    login({ authorizationParams: { screen_hint: "signup" } });

  const logout = () =>
    auth0Logout({ logoutParams: { returnTo: window.location.origin } });

  if (isLoading) return "Loading...";

  return isAuthenticated ? (
    <>
      <div className="page-layout">
        {!isCreating && <NavigationBar />}

        <div className="main-content">
          {isCreating ? (
            <div className="form-container">
              <CreateModelForm onCancelForm={handleModelCreate}/>
            </div>
          ) : (

            <CreateNewRAGModel onModelCreate={handleModelCreate}/>
          )}
        </div>
      </div>
    </>
  ) : (
    <>
      {error && <p>Error: {error.message}</p>}

      <button onClick={signup}>Signup</button>

      <button onClick={login}>Login</button>
    </>
  );
}

export default App;


{/*
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
*/}