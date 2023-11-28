import styles from './styles/UpcomingEvents.module.css'
import React, { useEffect, useState } from 'react'

const upcomingEvents = {
    '9/3/2022': ['is_student_event'],
    '9/5/2022': ['is_holiday'], 
    '9/10/2022': ['is_student_event'], 
    '9/24/2022': ['is_student_event'], 
    '10/22/2022': ['is_student_event'], 
    '10/29/2022': ['is_student_event'], 
    '11/11/2022': ['is_holiday'], 
    '11/19/2022': ['is_student_event'], 
    '11/23/2022': ['school_break'], 
    '11/24/2022': ['school_break'], 
    '11/25/2022': ['school_break','is_student_event'], 
    '11/26/2022': ['school_break'], 
    '11/27/2022': ['school_break'], 
    '12/5/2022': ['is_rrr_week'],
    '12/6/2022': ['is_rrr_week'],
    '12/7/2022': ['is_rrr_week'],
    '12/9/2022': ['is_rrr_week'],
    '12/9/2022': ['is_rrr_week'],
    '12/12/2022': ['is_finals_week'],
    '12/13/2022': ['is_finals_week'],
    '12/14/2022': ['is_finals_week'],
    '12/15/2022': ['is_finals_week'],
    '12/16/2022': ['is_finals_week'],
    '12/17/2022': ['is_student_event'],
    '12/23/2022': ['is_holiday'], 
    '12/26/2022': ['is_holiday'],
    '12/30/2022': ['is_holiday'],
    '1/2/2023': ['is_holiday'],
    // Spring 2023
    '1/16/2023': ['is_holiday'],
    '2/25/2023': ['is_holiday'],
    '3/26/2023': ['school_break'],
    '3/27/2023': ['school_break'],
    '3/28/2023': ['school_break'],
    '3/29/2023': ['school_break'],
    '3/30/2023': ['school_break'],
    '3/1/2023': ['school_break'],
    '4/1/2023': ['school_break'],
    '4/2/2023': ['school_break'],
    '4/22/2023': ['is_student_event'],
    '5/1/2023': ['is_rrr_week'],
    '5/2/2023': ['is_rrr_week'],
    '5/3/2023': ['is_rrr_week'],
    '5/4/2023': ['is_rrr_week'],
    '5/5/2023': ['is_rrr_week'],
    '5/8/2023': ['is_finals_week'],
    '5/9/2023': ['is_finals_week'],
    '5/10/2023': ['is_finals_week'],
    '5/11/2023': ['is_finals_week'],
    '5/12/2023': ['is_finals_week'],
    '5/13/2023': ['is_student_event'],
    '5/29/2023': ['is_holiday'],
    // Summer 2023
    '6/19/2023': ['is_holiday'],
    '7/4/2023': ['is_holiday'],
    // Fall 2023
    '9/4/2023': ['is_holiday'],
    '9/9/2023': ['is_student_event'],
    '9/16/2023': ['is_student_event'],
    '9/30/2023': ['is_student_event'],
    '10/7/2023': ['is_student_event'],
    '10/28/2023': ['is_student_event'],
    '11/10/2023': ['is_holiday'],
    '11/11/2023': ['is_student_event'],
    '11/22/2023': ['school_break'],
    '11/23/2023': ['school_break'],
    '11/24/2023': ['school_break'],
    '11/25/2023': ['school_break'],
    '11/26/2023': ['school_break'],
    '12/4/2023': ['RRR Week'],
    '12/5/2023': ['RRR Week'],
    '12/6/2023': ['RRR Week'],
    '12/7/2023': ['RRR Week'],
    '12/8/2023': ['RRR Week'],
    '12/11/2023': ['Finals'],
    '12/12/2023': ['Finals'],
    '12/13/2023': ['Finals'],
    '12/14/2023': ['Finals'],
    '12/15/2023': ['Fall Semester Ends','Finals'],
    '12/25/2023': ['Christmas Day'],
    '12/26/2023': ['Holiday'],
    '1/1/2024': ["New Year's Day"],
    '1/2/2024': ['Holiday'],
    // Spring 2024
    '1/15/2024': ['Martin Luther King Jr. Day'],
    '2/19/2024': ["Presidents' Day"],
    '3/23/2024': ['Spring Recess'],
    '3/24/2024': ['Spring Recess'],
    '3/25/2024': ['Spring Recess'],
    '3/26/2024': ['Spring Recess'],
    '3/27/2024': ['Spring Recess'],
    '3/28/2024': ['Spring Recess'],
    '3/29/2024': ['Spring Recess'],
    '3/30/2024': ['Spring Recess'],
    '3/31/2024': ['Spring Recess'],
    // {Cal Day TBD}
    '4/29/2024': ['RRR Week'],
    '4/30/2024': ['RRR Week'],
    '5/1/2024': ['RRR Week'],
    '5/2/2024': ['RRR Week'],
    '5/3/2024': ['RRR Week'],
    '5/6/2024': ['Finals'],
    '5/7/2024': ['Finals'],
    '5/8/2024': ['Finals'],
    '5/9/2024': ['Finals'],
    '5/10/2024': ['Finals'],
    '5/11/2024': ['Commencement']
}

export default function UpcomingEvents() {
    // get the current data
    // use the variable to show next 3 upcoming events 
    const currentDate = new Date();
    // const day = currentDate.getDay; // an int from 0 to 6 with 0 as Sunday
    // const month = currentDate.getMonth + 1;
    // const date = currentDate.getDate; // day of the month from 1 to 31
    // const year = currentDate.getFullYear;

    const today = currentDate.toLocaleDateString('en-US'); // gets date in the format 'MM/DD/YYYY'

    // get the next 3 upcoming events
    const nextThreeEvents = Object.keys(upcomingEvents)
        .filter(date => new Date(date) >= currentDate) // filter dates in the future
        .sort((a, b) => new Date(a) - new Date(b)) // sort dates in ascending order
        .slice(0, 3); // take the first 3 upcoming dates


    return (
        <div className={styles.upcomingSchedule}>
            <h2>Upcoming Events</h2>
            <p>
                {nextThreeEvents.map(date => (
                    <p key={date}>
                        {date} - {upcomingEvents[date].join(', ')}
                    </p>
                ))}
            </p>
        </div>
    )
}