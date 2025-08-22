import React from 'react';
import './TopBar.css';
import userIcon from '../User.svg';

function TopBar() {
    return (
        <div className="top-bar-container">
            <div className="top-bar-user-info">
                <p className="username">Username</p>
                <img src={userIcon} alt="User Icon" className="user-icon" />
            </div>
        </div>
    )
}

export default TopBar