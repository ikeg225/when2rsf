import styles from './styles/Home.module.css';
import React, { useEffect, useState } from 'react'
import UpcomingEvents, { upcomingEvents } from './UpcomingEvents';
import { Line } from 'react-chartjs-2';
import Axios from 'axios';
// import faker from 'fa
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import 'chartjs-adapter-date-fns'
import 'chartjs-adapter-moment'

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
      text: "12 Hour RSF Capcity Prediction",
      color: "#D9D9D9",
    },
  },
  scales: {
    y: {
      min: 0,
      max: 100,
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


const labels = ['7:00AM', '7:30AM', '8:00AM', '8:30AM', '9:00AM', '9:30AM', '10:00AM', '10:30AM', '11:00AM',
'11:30AM', '12:00PM', '12:30PM', '1:00PM', '1:30PM', '2:00PM', '2:30PM', '3:00PM', '3:30PM', '4:00PM', '4:30PM',
'5:00PM', '5:30PM', '6:00PM', '6:30PM', '7:00PM', '7:30PM', '8:00PM', '8:30PM', '9:00PM', '9:30PM', '10:00PM', '10:30PM', '11:00PM'];

function extractTimes(input) {
  const timePattern = /(\d{1,2})\s*(a\.m\.|p\.m\.)\s*-\s*(\d{1,2})\s*(a\.m\.|p\.m\.)/i;
  const match = input.match(timePattern);

  if (!match) {
      throw new Error('Invalid time format');
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

  // figure out how to use axios to make api calls 
  // figure out how to use the weather api to get future weather data
  // figure out what times you need tha future weather data
  // then use axios on future weather api with specified times

  // use school event data, get current date, return a list of booleans in the following order ['is_holiday', 'is_rrr_week', 'is_finals_week', 'is_student_event']

  const getForecast = async () => {
    try {
      const response = await Axios.get(`http://api.weatherapi.com/v1/forecast.json?key=${process.env.REACT_APP_WEATHER_API_KEY}`, {
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
    if (dayOfWeek === 0) dayOfWeek = 7; 

    return day.hour.map(hour => ({
      day_of_week: dayOfWeek,
      temperature: hour.temp_f,
      temp_feel: hour.feelslike_f,
      wind_mph: hour.wind_mph,
      wind_degree: hour.wind_degree,
      pressure_mb: hour.pressure_mb,
      precipitation_mm: hour.precip_mm,
      humidity: hour.humidity,
      cloudiness: hour.cloud,
      uv_index: hour.uv,
      gust_mph: hour.gust_mph,
      school_break: today in upcomingEvents ? (upcomingEvents[today]['categories'].contains('school_break') ? 1 : 0) : 0,
      is_holiday: today in upcomingEvents ? (upcomingEvents[today]['categories'].contains('is_holiday') ? 1 : 0) : 0,
      is_rrr_week: today in upcomingEvents ? (upcomingEvents[today]['categories'].contains('is_rrr_week') ? 1 : 0) : 0,
      is_finals_week: today in upcomingEvents ? (upcomingEvents[today]['categories'].contains('is_finals_week') ? 1 : 0) : 0,
      is_student_event: today in upcomingEvents ? (upcomingEvents[today]['categories'].contains('is_student_event') ? 1 : 0) : 0,
      hour: hour
    }));
  }

  function makePrediction(parameter) {
    Axios.put('https://api.when2rsf.com/predict', parameter)
      .then(response => {
        console.log(response)
        return;
      }, response => {
        console.log(response)
      })
  }

  const [today, setTodaysPredictions] = useState([])
  const [tomorrow, setTomorrowsPredictions] = useState([])
  const [error, setError] = useState([])

  useEffect(() => {
    const fetchData = async () => {
      const data = await getForecast();

      for (const parameter in await createParameters(data.forecastday[0], false)) {
        setTodaysPredictions(prevState => [...prevState, makePrediction(parameter)])
      }

      for (const parameter in await createParameters(data.forecastday[1], true)) {
        console.log(parameter)
        setTodaysPredictions(prevState => [...prevState, makePrediction(parameter)])
      }


        // .then(data => {
        //   // const parameters = {
        //   //   "today": createParameters(data.forecastday[0], false), 
        //   //   "tomorrow": createParameters(data.forecastday[1], true)
        //   // }
        //   // console.log(parameters)

        //   for (const parameter in await createParameters(data.forecastday[0], false)) {
        //     setTodaysPredictions(prevState => [...prevState, makePrediction(parameter)])
        //   }

        //   for (const parameter in createParameters(data.forecastday[1], true)) {
        //     console.log(parameter)
        //     setTodaysPredictions(prevState => [...prevState, makePrediction(parameter)])
        //   }

        //   // for (const key in parameters) {
        //   //   const values = parameters[key]
        //   //   for (let i = 0; i < values.length; i++) {
        //   //     if (key == "today") {
        //   //       console.log(values[i])
        //   //       setTodaysPredictions(prevState => [...prevState, makePrediction(values[i])]);
        //   //     } else if (key == "tomorrow") {
        //   //       setTomorrowsPredictions(prevState => [...prevState, makePrediction(values[i])]);
        //   //     }
        //   //   }
        //   // }
        // })
        // .catch(err => {
        //   setError(err.message);
        // });
    }

    fetchData();
  }, []);

  const [timeData, setTimeData] = useState([
    // default time data
  ])
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
  };

  // Widget
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
      <div className={`${styles.UpcomingEvents} ${styles.mainContent}`}>
          <UpcomingEvents />
      </div>
      <div className={`${styles.Graph} ${styles.mainContent}`}>
        <div className={`${styles.buttonContainer}`}>
          <button 
            className={`${styles.timeButton} ${todaySelected ? styles.buttonSelected : ''}`} 
            onClick={() => {setTimeData(today); setTodaySelected(true)}}
          >
            Today
          </button>
          <button 
            className={`${styles.timeButton} ${!todaySelected ? styles.buttonSelected : ''}`} 
            onClick={() => {setTimeData(tomorrow); setTodaySelected(false)}}
          >
            Tomorrow
          </button>
          </div>
          <Line data={data} options={options}/>
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