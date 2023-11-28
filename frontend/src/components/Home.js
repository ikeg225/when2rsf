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
      text: '12 Hour RSF Capcity Prediction',
      color: '#D9D9D9'
    },
  },
  scales: {
    y: {
      min: 0,
      max: 100,
    }
  }
};

const labels = ['7:00AM', '7:30AM', '8:00AM', '8:30AM', '9:00AM', '9:30AM', '10:00AM', '10:30AM', '11:00AM',
'11:30AM', '12:00PM', '12:30PM', '1:00PM', '1:30PM', '2:00PM', '2:30PM', '3:00PM', '3:30PM', '4:00PM', '4:30PM',
'5:00PM', '5:30PM', '6:00PM', '6:30PM', '7:00PM', '7:30PM', '8:00PM', '8:30PM', '9:00PM', '9:30PM', '10:00PM', '10:30PM', '11:00PM'];
console.log((labels).length)

function Home() {

  const [timeData, setTimeData] = useState([])

  const data = {
    labels,
    datasets: [
      {
        data: [
          47, 12, 85, 33, 76, 55, 97, 28, 64, 10, 
          82, 5, 91, 59, 39, 73, 21, 44, 88, 34, 
          67, 18, 50, 3, 79, 26, 62, 9, 81, 57, 
          38, 72, 20
        ],
        borderColor: 'rgb(53, 162, 235)',
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
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

  // Graph
//   let now = new Date();
//   const minTime = new Date(now)
//   minTime.setMinutes(0, 0, 0)
//   const maxTime = new Date(now)
//   maxTime.setHours(maxTime.getHours() + 12)
//   maxTime.setMinutes(0, 0, 0)
//   if (maxTime < now) {
//     maxTime.setHours(maxTime.getHours() + 1);
// }

//   const chartData = {
//     datasets:[{
//       label: "My Dataset",
//       data: [
//         { x: new Date('2023-11-27T00:00:00'), y: 4}
//       ]
//     }]
//   }

//   const options = {
//     scales: {
//       x: {
//         type: "time",
//         // time: {
//         //   unit: "hour",
//         // },
//         // min: minTime,
//         // max: maxTime
//       },
//       y: {
//         beginAtZero: true
//       }
//     }
//   }

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
          <button>today</button>
          <button>tomorrow</button>
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