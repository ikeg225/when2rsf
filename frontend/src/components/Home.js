import styles from './styles/Home.module.css'
import React, { useEffect, useState } from 'react'
import UpcomingEvents, { upcomingEvents } from './UpcomingEvents'
import { Line } from 'react-chartjs-2'
import Axios from 'axios'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'
import 'chartjs-adapter-date-fns'
import 'chartjs-adapter-moment'
import { setupCache } from 'axios-cache-interceptor'

const axios = setupCache(Axios);

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export const options = {
  responsive: true,
  elements: {
    line: {
      tension: 0.3,
      pointHoverRadius: 3
    }
  },
  plugins: {
    legend: {
      display: false
    },
    title: {
      display: true,
      text: "RSF Capcity Prediction",
      color: "#D9D9D9",
    },
  },
  scales: {
    y: {
      min: 0,
      max: 110,
      title: {
        display: true,
        align: "center",
        text: "Capacity Percentage",
        color: "#D9D9D9",
      },
      ticks: {
        color: "#D9D9D9",
      },
      grid: {
        color: "#4E5B70"
      },
    },
    x: {
      title: {
        display: true,
        align: "center",
        text: "Time",
        color: "#D9D9D9",
      },
      ticks: {
        color: "#D9D9D9",
      },
      grid: {
        color: "#4E5B70"
      },
    }
  }
};


const labels = ['7:00AM', '8:00AM', '9:00AM', '10:00AM', '11:00AM', '12:00PM', '1:00PM', '2:00PM', '3:00PM', '4:00PM',
'5:00PM', '6:00PM', '7:00PM', '8:00PM', '9:00PM', '10:00PM', '11:00PM'];

function extractTimes(input) {
  const timePattern = /(\d{1,2})\s*(a\.m\.|p\.m\.)\s*-\s*(\d{1,2})\s*(a\.m\.|p\.m\.)/i;
  const match = input.match(timePattern);

  if (!match) {
    return "CLOSED"
  }

  let [_, startHour, startPeriod, endHour, endPeriod] = match;

  // Convert to standard time format
  startHour = startHour.length === 1 ? `0${startHour}` : startHour;
  endHour = endHour.length === 1 ? `0${endHour}` : endHour;

  const startTime = `${startHour}:00 ${startPeriod.toUpperCase().replace(/\./g, '')}`;
  const endTime = `${endHour}:00 ${endPeriod.toUpperCase().replace(/\./g, '')}`;

  return { startTime, endTime };
}

function createTimeLabels(startTime, endTime) {
  function parseTime(timeStr) {
      const [time, period] = timeStr.split(' ');
      let [hours, minutes] = time.split(':').map(Number);

      if (period === 'PM' && hours < 12) hours += 12;
      if (period === 'AM' && hours === 12) hours = 0;

      return new Date(2000, 0, 1, hours, minutes); // Date is arbitrary
  }

  function formatTime(date) {
      let hours = date.getHours();
      let minutes = date.getMinutes();
      const period = hours >= 12 ? 'PM' : 'AM';

      hours = hours % 12;
      hours = hours ? hours : 12; // Convert hour '0' to '12'
      minutes = minutes < 10 ? '0' + minutes : minutes;

      return `${hours}:${minutes}${period}`;
  }

  const start = parseTime(startTime);
  const end = parseTime(endTime);
  const labels = [];
  let current = new Date(start);

  while (current <= end) {
      labels.push(formatTime(current));
      current = new Date(current.getTime() + 60 * 60000); // Add 60 minutes
  }

  return labels;
}


const test = extractTimes("Monday, Nov. 27	7 a.m. - 11 p.m.")

console.log(createTimeLabels(test.startTime, test.endTime))


function Home() {
  const getForecast = async () => {
    try {
      const response = await axios.get(`https://api.weatherapi.com/v1/forecast.json?key=${process.env.REACT_APP_WEATHER_API_KEY}`, {
        params: {
          q: "Berkeley",
          days: 2,
          aqi: "yes",
          alerts: "no"
        }
      });
      console.log('Forecast Data Retrieved');
      return response.data.forecast;
    } catch (error) {
      console.error('Error fetching weather data:', error);
      // Depending on how you want to handle errors, you might throw the error or return null/undefined.
      throw error;
    }
  }

  function createParameters(day, isTomorrow) {
    const currentDate = new Date();
    const today = currentDate.toLocaleDateString('en-US');

    const today2 = new Date();
    if (isTomorrow) {
        today2.setDate(today2.getDate() + 1);
    }
    let dayOfWeek = today2.getDay(); 

    const arr = []
    for (const hour of [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]) {
      const hourJSON = day.hour[hour]
      arr.push({
        day_of_week: dayOfWeek + 1,
        temperature: hourJSON.temp_f,
        temp_feel: hourJSON.feelslike_f,
        wind_mph: hourJSON.wind_mph,
        wind_degree: hourJSON.wind_degree,
        pressure_mb: hourJSON.pressure_mb,
        precipitation_mm: hourJSON.precip_mm,
        humidity: hourJSON.humidity,
        cloudiness: hourJSON.cloud,
        uv_index: hourJSON.uv,
        gust_mph: hourJSON.gust_mph,
        school_break: today in upcomingEvents ? (upcomingEvents[today]['categories'].contains('school_break') ? 1 : 0) : 0,
        is_holiday: today in upcomingEvents ? (upcomingEvents[today]['categories'].contains('is_holiday') ? 1 : 0) : 0,
        is_rrr_week: today in upcomingEvents ? (upcomingEvents[today]['categories'].contains('is_rrr_week') ? 1 : 0) : 0,
        is_finals_week: today in upcomingEvents ? (upcomingEvents[today]['categories'].contains('is_finals_week') ? 1 : 0) : 0,
        is_student_event: today in upcomingEvents ? (upcomingEvents[today]['categories'].contains('is_student_event') ? 1 : 0) : 0,
        hour: hour
      })
    }

    return arr
  }

  async function makePrediction(parameter) {
    const headers = { 
      'Content-type':'application/json', 
      'Accept':'application/json'
    };
    let pred = 0;

    await axios.put('https://api.when2rsf.com/predict', parameter, { headers })
      .then(response => {
        pred = (response.data.prediction / 150) * 100;
      }, response => {
        console.log(response)
      })
    
    return pred
  }

  const [today, setTodaysPredictions] = useState([])
  const [tomorrow, setTomorrowsPredictions] = useState([])

  useEffect(() => {
    const fetchData = async () => {
      const data = await getForecast();

      const todaysPredicted = []
      for (const parameter of await createParameters(data.forecastday[0], false)) {
        const pred = await makePrediction(parameter)
        todaysPredicted.push(pred)
      }
      setTodaysPredictions(todaysPredicted)

      const tomorrowsPredicted = []
      for (const parameter of await createParameters(data.forecastday[1], true)) {
        const pred = await makePrediction(parameter)
        tomorrowsPredicted.push(pred)
      }
      setTomorrowsPredictions(tomorrowsPredicted)
    }

    fetchData();
  }, []);

  const [timeData, setTimeData] = useState(today)
  const [todaySelected, setTodaySelected] = useState(true)

  const data = {
      labels,
      datasets: [
        {
          data: timeData,
          borderColor: 'rgb(53, 162, 235)',
          backgroundColor: "#D9D9D9",
        },
      ],
    }
  
  useEffect(() => {
    setTimeData(today)
  }, [today])
  
  useEffect(() => {
    // Create a script element
    const script = document.createElement('script');
    script.src = 'https://app2.weatherwidget.org/js/?id=ww_6d0678363ff5a';
    script.async = true;

    // Append the script to the body
    document.body.appendChild(script);

    // Perform cleanup
    return () => {
      // Remove the script from the body
      document.body.removeChild(script);
    };
  }, []);

  const todayDate = new Date()
  const tomorrowDate = new Date(todayDate)
  tomorrowDate.setDate(tomorrowDate.getDate() + 1)

  return (
    <div className={styles.Home}>
      <div className={styles.top}>
        <div className={`${styles.UpcomingEvents} ${styles.eventsBackground}`}>
            <UpcomingEvents />
        </div>
        <div className={`${styles.Weather} ${styles.weatherBackground}}`}>
          <div>
            <div id="ww_6d0678363ff5a" v='1.3' loc='auto' a='{"t":"horizontal","lang":"en","sl_lpl":1,"ids":[],"font":"Times","sl_ics":"one_a","sl_sot":"fahrenheit","cl_bkg":"image","cl_font":"#FFFFFF","cl_cloud":"#FFFFFF","cl_persp":"#81D4FA","cl_sun":"#FFC107","cl_moon":"#FFC107","cl_thund":"#FF5722"}'>
                More forecasts: <a href="https://oneweather.org/toronto/30_days/" id="ww_6d0678363ff5a_u" target="_blank" rel="noreferrer">Weather 30 days Toronto</a>
            </div>
          </div>
        </div>
      </div>
      <div className={`${styles.Graph} ${styles.mainContent} ${styles.graphBackground}`}>
        <div className={`${styles.buttonContainer}`}>
          <button 
            className={`${styles.timeButton} ${todaySelected ? styles.buttonSelected : ''}`} 
            onClick={() => {setTimeData(today); setTodaySelected(true)}}
          >
            Today ({todayDate.toLocaleDateString('en-US')})
          </button>
          <button 
            className={`${styles.timeButton} ${!todaySelected ? styles.buttonSelected : ''}`} 
            onClick={() => {setTimeData(tomorrow); setTodaySelected(false)}}
          >
            Tomorrow ({tomorrowDate.toLocaleDateString('en-US')})
          </button>
          </div>
          <Line data={data} options={options}/>
      </div>
    </div>
  );
}

export default Home;