import React from 'react'
import Navbar from './Navbar'
import Graph from './Graph'
import SportsSchedule from './SportsSchedule'
import Weather from './Weather'
import CurrentData from './CurrentData'

const App = () => {
    return(
        <div className = "App">
            <Navbar />
            <div className = 'content'>
                <CurrentData />
                <SportsSchedule />
                <Graph />
                <Weather />
            </div>
        </div>
    )
}
export default App