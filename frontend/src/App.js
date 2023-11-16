import styles from './App.module.css';
import Navbar from './components/Navbar';

function App() {
  return (
    <div className={styles.App}>
      <Navbar />
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
          <h1>d</h1>
      </div>
    </div>
  );
}

export default App;
