import styles from './styles/UpcomingEvents.module.css'
import React, { useEffect, useState } from 'react'

export const upcomingEvents = {
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
    '11/25/2022': {'event_name': 'Thanksgiving', 'categories': ['school_break','is_student_event']}, 
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
    // start here
    '12/4/2023': {'event_name': 'RRR Week', 'categories': ['is_rrr_week']},
    '12/5/2023': {'event_name': 'RRR Week', 'categories': ['is_rrr_week']},
    '12/6/2023': {'event_name': 'RRR Week', 'categories': ['is_rrr_week']},
    '12/7/2023': {'event_name': 'RRR Week', 'categories': ['is_rrr_week']},
    '12/8/2023': {'event_name': 'RRR Week', 'categories': ['is_rrr_week']},
    '12/11/2023': {'event_name': 'Finals Week', 'categories': ['is_finals_week']},
    '12/12/2023': {'event_name': 'Finals Week', 'categories': ['is_finals_week']},
    '12/13/2023': {'event_name': 'Finals Week', 'categories': ['is_finals_week']},
    '12/14/2023': {'event_name': 'Finals Week', 'categories': ['is_finals_week']},
    '12/15/2023': {'event_name': 'Finals Week, End of Fall Semester', 'categories': ['is_student_event', 'is_finals_week']},
    // TODO: need school_break dates here
    '12/16/2023': {'event_name': 'Winter Commencement, Winter Recess', 'categories': ['is_student_event', 'school_break']},
    '12/17/2023': {'event_name': 'Winter Recess', 'categories': ['school_break']},
    '12/18/2023': {'event_name': 'Winter Recess', 'categories': ['school_break']},
    '12/19/2023': {'event_name': 'Winter Recess', 'categories': ['school_break']},
    '12/20/2023': {'event_name': 'Winter Recess', 'categories': ['school_break']},
    '12/21/2023': {'event_name': 'Winter Recess', 'categories': ['school_break']},
    '12/22/2023': {'event_name': 'Winter Recess', 'categories': ['school_break']},
    '12/23/2023': {'event_name': 'Winter Recess', 'categories': ['school_break']},
    '12/24/2023': {'event_name': 'Winter Recess', 'categories': ['school_break']},
    '12/25/2023': {'event_name': 'Christmas Day, Winter Recess', 'categories': ['is_holiday', 'school_break']},
    '12/26/2023': {'event_name': 'Holiday, Winter Recess', 'categories': ['is_holiday', 'school_break']},
    '12/27/2023': {'event_name': 'Winter Recess', 'categories': ['school_break']},
    '12/28/2023': {'event_name': 'Winter Recess', 'categories': ['school_break']},
    '12/29/2023': {'event_name': 'Winter Recess', 'categories': ['school_break']},
    '12/30/2023': {'event_name': 'Winter Recess', 'categories': ['school_break']},
    '12/31/2023': {'event_name': 'Winter Recess', 'categories': ['school_break']},
    // TODO: need school_break dates here
    '1/1/2024': {'event_name': "New Year's Day, Winter Recess", 'categories': ['is_holiday', 'school_break']},
    '1/2/2024': {'event_name': "Holiday, Winter Recess", 'categories': ['is_holiday', 'school_break']},
    '1/3/2024': {'event_name': 'Winter Recess', 'categories': ['school_break']},
    '1/4/2024': {'event_name': 'Winter Recess', 'categories': ['school_break']},
    '1/5/2024': {'event_name': 'Winter Recess', 'categories': ['school_break']},
    '1/6/2024': {'event_name': 'Winter Recess', 'categories': ['school_break']},
    '1/7/2024': {'event_name': 'Winter Recess', 'categories': ['school_break']},
    '1/8/2024': {'event_name': 'Winter Recess', 'categories': ['school_break']},
    // Spring 2024
    // TODO: need school_break dates here
    '1/15/2024': {'event_name': 'Martin Luther King Jr. Day', 'categories': ['is_holiday']},
    '2/19/2024': {'event_name': "Presidents' Day", 'categories': ['is_holiday']},
    '3/23/2024': {'event_name': 'Spring Recess', 'categories': ['school_break']},
    '3/24/2024': {'event_name': 'Spring Recess', 'categories': ['school_break']},
    '3/25/2024': {'event_name': 'Spring Recess', 'categories': ['school_break']},
    '3/26/2024': {'event_name': 'Spring Recess', 'categories': ['school_break']},
    '3/27/2024': {'event_name': 'Spring Recess', 'categories': ['school_break']},
    '3/28/2024': {'event_name': 'Spring Recess', 'categories': ['school_break']},
    '3/29/2024': {'event_name': 'Spring Recess', 'categories': ['school_break']},
    '3/30/2024': {'event_name': 'Spring Recess', 'categories': ['school_break']},
    '3/31/2024': {'event_name': 'Spring Recess', 'categories': ['school_break']},
    '4/13/2024': {'event_name': 'Cal Day', 'categories': ['is_student_event']},
    '4/29/2024': {'event_name': 'RRR Week', 'categories': ['is_rrr_week']},
    '4/30/2024': {'event_name': 'RRR Week', 'categories': ['is_rrr_week']},
    '5/1/2024': {'event_name': 'RRR Week', 'categories': ['is_rrr_week']},
    '5/2/2024': {'event_name': 'RRR Week', 'categories': ['is_rrr_week']},
    '5/3/2024': {'event_name': 'RRR Week', 'categories': ['is_rrr_week']},
    '5/6/2024': {'event_name': 'Finals Week', 'categories': ['is_finals_week']},
    '5/7/2024': {'event_name': 'Finals Week', 'categories': ['is_finals_week']},
    '5/8/2024': {'event_name': 'Finals Week', 'categories': ['is_finals_week']},
    '5/9/2024': {'event_name': 'Finals Week', 'categories': ['is_finals_week']},
    '5/10/2024': {'event_name': 'Finals Week', 'categories': ['is_finals_week']},
    '5/11/2024': {'event_name': 'Commencement', 'categories': ['is_student_event']},
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
                        {date} - {upcomingEvents[date]['event_name']}
                    </p>
                ))}
            </p>
        </div>
    )
}