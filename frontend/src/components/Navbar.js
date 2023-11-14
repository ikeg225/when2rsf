import React from "react";
import styles from './styles/NavBar.module.css';
import { GoGraph, GoPeople, GoLightBulb } from 'react-icons/go'

const Navbar = () => {
    return(
        <nav className = {styles.navbar}>
            <ul className = {styles.navbarNav}>
                <li className = {styles.navItem}>
                    <a href = '#' className = {styles.navLink}>
                        <GoGraph />
                        <span className = {styles.linkText}>Home</span>
                    </a>
                </li>

                <li className = {styles.navItem}>
                    <a href = '#' className = {styles.navLink}>
                        <GoLightBulb />
                        <span className = {styles.linkText}>How it works</span>
                    </a>
                </li>

                <li className = {styles.navItem}>
                    <a href = '#' className = {styles.navLink}>
                        <GoPeople />
                        <span className = {styles.linkText}>About Us</span>
                    </a>
                </li>
            </ul>
        </nav> 
    )
}

export default Navbar