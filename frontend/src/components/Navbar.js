import React from "react";
import styles from './styles/NavBar.module.css';
import { GoGraph, GoPeople, GoLightBulb } from 'react-icons/go'
import { Link } from 'react-router-dom';

const NavBar = () => {
    return(
        <nav className = {styles.navbar}>
            <ul className = {styles.navbarNav}>
                <li className = {styles.navItem}>
                    <a href = '#' className = {styles.navLink}>
                        <GoGraph />
                        <Link className={styles.linkText} to="/">Home</Link>
                    </a>
                </li>

                <li className = {styles.navItem}>
                    <a href = '#' className = {styles.navLink}>
                        <GoLightBulb />
                        <Link className={styles.linkText} to="/how-it-works">How it works</Link>
                    </a>
                </li>

                <li className = {styles.navItem}>
                    <a href = '#' className = {styles.navLink}>
                        <GoPeople />
                        <Link className={styles.linkText} to="/about-us">About Us</Link>
                    </a>
                </li>
            </ul>
        </nav> 
    )
}

export default NavBar