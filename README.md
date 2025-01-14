<h1>Crypto Price App</h1>

<h2>Overview</h2>
The Crypto Price App is a Streamlit-based web application that allows users to track and visualize cryptocurrency prices and related metrics in real-time. It leverages the CoinMarketCap API to fetch data for the top 100 cryptocurrencies, providing users with a comprehensive view of the crypto market. The app is designed to be user-friendly, interactive, and visually appealing, making it a great tool for both casual users and crypto enthusiasts.


<h2>Features</h2>

<h3>1. Real-Time Cryptocurrency Data</h3>

Fetches real-time data for the top 100 cryptocurrencies from CoinMarketCap.

Displays key metrics such as:

Current price in USD, BTC, or ETH.

Percentage change over 1 hour, 24 hours, and 7 days.

Market capitalization, 24-hour trading volume, circulating supply, total supply, and max supply.

Users can select their preferred currency for price display (USD, BTC, or ETH).

<h3>2. Interactive Data Filtering and Sorting</h3>

Users can filter cryptocurrencies by selecting specific coins from a multiselect dropdown.

The app allows sorting of data by percentage change over 1 hour, 24 hours, or 7 days.

Users can also limit the number of coins displayed using a slider (from 1 to 100).

<h3>3. Visualization of Price Changes</h3>

The app provides a bar plot to visualize the percentage price changes for the selected cryptocurrencies.

The bar plot is color-coded:

Green bars indicate positive price changes.

Red bars indicate negative price changes.

Users can choose the time frame for the percentage change (1 hour, 24 hours, or 7 days).

<h3>4. Detailed Coin Information</h3>

Users can select a specific cryptocurrency to view detailed information, including:

Coin description.

Logo (if available).

Website URL (if available).

The app also displays a 7-day price change graph and a 24-hour volume graph for the selected coin (simulated data in this version).

<h3>5. CSV Download</h3>

Users can download the displayed cryptocurrency data as a CSV file for offline analysis.

<h3>6. User-Friendly Interface</h3>

The app features a clean and intuitive layout with:

A sidebar for user inputs (e.g., API key, currency selection, coin filtering).

A main content area for displaying data and visualizations.

The app is responsive and works well on both desktop and mobile devices.

<h2>How It Works</h2>

<h3>1. API Integration</h3>
 
The app uses the CoinMarketCap API to fetch real-time cryptocurrency data.

Users need to provide their own API key (available for free from CoinMarketCap) to access the data.

The API key is securely passed to the app via a text input field in the sidebar.

<h3>2. Data Processing</h3>

The app processes the JSON response from the API and extracts relevant data such as price, percentage changes, market cap, and volume.

The data is then organized into a Pandas DataFrame for easy manipulation and display.

<h3>3. Visualization</h3>

The app uses Matplotlib and Plotly to create interactive visualizations.

The bar plot for percentage price changes is generated using Matplotlib, while the 7-day price change and 24-hour volume graphs are created using Plotly.

<h3>4. Simulated Historical Data</h3>

Since the CoinMarketCap API does not provide historical price data directly, the app simulates historical data for the 7-day price change and 24-hour volume graphs using random data.

In a real-world scenario, you would replace this with actual historical data from a suitable API or database.

