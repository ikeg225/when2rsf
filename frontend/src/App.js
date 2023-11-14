import styles from './App.module.css';
import NavBar from './components/NavBar';

function App() {
  return (
    <div className={styles.App}>
      <NavBar />
      <div className={`${styles.CurrentData} ${styles.mainContent}`}>
          <h1>a</h1>
      </div>
      <div className={`${styles.SportsSchedule} ${styles.mainContent}`}>
          <h1>b</h1>
      </div>
      <div className={`${styles.Graph} ${styles.mainContent}`}>
          <h1>c</h1>
      </div>
      <div className={`${styles.Weather} ${styles.mainContent}`}>
          <h1>d</h1>
      </div>
    </div>
  );
}

export default App;
