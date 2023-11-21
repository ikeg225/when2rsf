import React from "react";
import styles from './styles/NavBar.module.css';
import { GoGraph, GoPeople, GoLightBulb } from 'react-icons/go'
import { Link } from 'react-router-dom';

const NavBar = () => {
    return(
        <nav className = {styles.navbar}>
            <ul className = {styles.navbarNav}>
                <li className = {styles.navItem}>
                    <Link className={styles.navLink} to="/">
                        <GoGraph />
                        <p>Home</p>
                    </Link>
                </li>
                <li className = {styles.navItem}>
                    <Link className={styles.navLink} to="/how-it-works">
                        <GoLightBulb />
                        <p>How it works</p>
                    </Link>
                </li>
                <li className = {styles.navItem}>
                    <Link className={styles.navLink} to="/about-us">
                        <GoPeople />
                        <p>About Us</p>
                    </Link>
                </li>
            </ul>
        </nav> 
    )
}

export default NavBar