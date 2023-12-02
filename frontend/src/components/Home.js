import styles from './styles/Home.module.css';
import React, { useEffect, useState } from 'react'
import UpcomingEvents from './UpcomingEvents';
import { Line } from 'react-chartjs-2';
// import faker from 'faker';
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
      current = new Date(current.getTime() + 30 * 60000); // Add 30 minutes
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

  const getForcast = () => {
    Axios.get(`http://api.weatherapi.com/v1/forcast.json?key=${process.env.REACT_APP_WEATHER_API_KEY}`, {params: {q: "Berkeley", days: 2, aqi: "yes", alerts: "no"}})
      .then(response => {
        console.log(response.data.forcast)
      })
      .catch(error => {
        console.log(error)
      })
  }

  console.log(getForcast())

  let todays_events = {
    'is_holiday' : false,
    'is_rrr_week' : false,
    'is_finals_week' : false,
    'is_student_event' : false
  }
  
  const currentDate = new Date();
  // const formattedDate = currentDate.toLocaleDateString('en-US');
  
  if (upcomingEvents[today]['categories'].contains('is_holiday')) {
    todays_events['is_holiday'] = true;
  } else if (upcomingEvents[today]['categories'].contains('is_rrr_week')) {
    todays_events['is_rrr_week'] = true;
  } else if (upcomingEvents[today]['categories'].contains('is_finals_week')) {
    todays_events['is_finals_week'] = true;
  } else if (upcomingEvents[today]['categories'].contains('is_student_event')) {
    todays_events['is_student_event'] = true;
  }


  // ['day_of_week', 'temperature', 'temp_feel', 'weather_code', 'wind_mph', 'wind_degree', 'pressure_mb', 'precipitation_mm', 'humidity', 'cloudiness', 'uv_index', 'gust_mph', 'school_break', 'is_holiday', 'is_rrr_week', 'is_finals_week', 'is_student_event', 'hour']

  const weatherParameters = {
    day_of_week : currentDate.getDay + 1,
    temperature: "bjbh",
    school_break : todays_events['is_holiday'],
    is_rrr_week : todays_events['is_rrr_week'],
    is_finals_week : todays_events['is_finals_week'],
    is_student_event : todays_events['is_student_event'],
    hour : currentDate.getHours(),
  }  


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

  const today = [
    47, 12, 85, 33, 76, 55, 97, 28, 64, 10, 
    82, 5, 91, 59, 39, 73, 21, 44, 88, 34, 
    67, 18, 50, 3, 79, 26, 62, 9, 81, 57, 
    38, 72, 20
  ]

  const tomorrow = [
    12, 34, 56, 78, 21, 43, 65, 87, 9, 31, 
    53, 75, 97, 19, 41, 63, 85, 7, 29, 51, 
    73, 95, 17, 39, 61, 83, 5, 27, 49, 71, 
    93, 15, 37
  ]


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
      <div className={`${styles.CurrentData} ${styles.mainContent}`}>
          <h1>navigation bar</h1>
      </div>
      <div className={`${styles.UpcomingEvents} ${styles.mainContent}`}>
          <h1>upcoming events</h1>
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