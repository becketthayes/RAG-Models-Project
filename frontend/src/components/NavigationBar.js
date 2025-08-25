import React, { useState } from 'react';
import './NavigationBar.css'; // Don't forget to import the CSS!

function NavigationBar() {
    const [activeItem, setActiveItem] = useState("Dashboard");
    return (
        <div className="sidebar">
            <div className="sidebar-content">
                <p className="title">RAG Builder</p>

                <nav>
                    <ul>
                        {['Dashboard', 'Models', 'Data Sources'].map(item => (
                            <li key={item}>
                                <a 
                                    href="#"
                                    className={activeItem === item ? 'nav-link active': 'nav-link'}
                                    onClick={() => setActiveItem(item)}
                                >
                                    {item}
                                </a>
                            </li>
                        ))}
                    </ul>
                </nav>
            </div>
        </div>
    )
}

export default NavigationBar