import styles from './styles/Home.module.css';
import React, { useEffect, useState } from 'react'

function Home() {
  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://www.weatherapi.com/weather/widget.ashx?loc=2549438&wid=3&tu=2&div=weatherapi-weather-widget-3';
    script.async = true;

    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, []);

  return (
    <div className={styles.Home}>
      <div className={`${styles.CurrentData} ${styles.mainContent}`}>
          <h1>navigation bar</h1>
      </div>
      <div className={`${styles.SportsSchedule} ${styles.mainContent}`}>
          <h1>sports schedule</h1>
      </div>
      <div className={`${styles.Graph} ${styles.mainContent}`}>
          <h1>graph</h1>
      </div>
      <div className={`${styles.Weather} ${styles.mainContent}`}>
        <div className={`${styles.WeatherWidget}`}>
          <div id="weatherapi-weather-widget-3"></div>
          <script type='text/javascript' src='https://www.weatherapi.com/weather/widget.ashx?loc=2549438&wid=3&tu=2&div=weatherapi-weather-widget-3' async></script>
          <noscript><a href="https://www.weatherapi.com/weather/q/Berkeley-2549438" alt="Hour by hour Oakland weather">10 day hour by hour Oakland weather</a></noscript>
        </div>
      </div>
    </div>
  );
}

export default Home;