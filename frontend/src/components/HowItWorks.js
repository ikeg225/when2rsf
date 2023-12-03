const HowItWorks = () => {
    return(
        <div>
            <h1>How It Works</h1>
            <h2>Working with the Data</h2>
            <p>Our process begins by collecting data from various sources, including the <a href="https://recwell.berkeley.edu/rsf-weight-room-crowd-meter/" target="_blank" rel="noopener noreferrer">RSF crowd-o-meter API</a> and external factors such as weather conditions and school events. Using Python scripts and tools like Chrome Developer Tools, we gather data at 30-minute intervals, ensuring a comprehensive dataset for analysis.</p>
            <p>Once collected, our team meticulously cleans and organizes the data. This involves handling missing values, removing inconsistencies, and standardizing formats across different data sources. We ensure the dataset is accurate, reliable, and ready for analysis.</p>
            <h2>Utilizing Models for Predictions</h2>
            <p>Our predictive models are built using a Random Forest Classifier with Scikit-learn. These models undergo rigorous training on the cleaned dataset. We experiment with different algorithms to determine the most accurate approach for predicting RSF capacity percentages based on time, weather, school events, and other influential factors.</p>
            <p>Once the models are trained and validated, they become capable of forecasting RSF capacity percentages at different times throughout the day. These predictions are based on historical data and real-time factors, enabling users to identify the least crowded times to visit the gym.</p>
            <h2>Displaying Predictions</h2>
            <p>Our website provides an intuitive user interface designed using React. Through this interface, users can access predictions displayed in a user-friendly format. We aim to present this information in a clear, digestible manner, allowing users to plan their gym visits effectively.</p>
        </div>
    )
}

export default HowItWorks