import React from "react";
import { GoGraph, GoPeople, GoLightBulb } from 'react-icons/go'

const Navbar = () => {
    return(
        <nav className = "navbar">
            <ul className = "navbar-nav">
                <li className = "nav-item">
                    <a href = '#' className = "nav-link">
                        <GoGraph />
                        <span className = "link-text">Home</span>
                    </a>
                </li>

                <li className = "nav-item">
                    <a href = '#' className = "nav-link">
                        <GoLightBulb />
                        <span className = "link-text">How it works</span>
                    </a>
                </li>

                <li className = "nav-item">
                    <a href = '#' className = "nav-link">
                        <GoPeople />
                        <span className = "link-text">About Us</span>
                    </a>
                </li>
            </ul>
        </nav> 
    )
}

export default Navbar