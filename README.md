Bitcoin Blockcraft
An Interactive Bitcoin Market Analysis & Blockchain Dashboard

Bitcoin Blockcraft is a high-performance web application built with Streamlit, designed to provide users with a comprehensive suite for Bitcoin market analysis, blockchain data visualization, and portfolio tracking. By leveraging real-time data, the platform offers deep insights into price action and network health through a professional, minimalist interface.

Live Demo Link : https://bitcoin-blockcraft.streamlit.app/

Key Features
1. Real-Time Market Monitoring
Live Price Tracking: Real-time Bitcoin price data fetched via high-reliability exchange APIs.

Historical Trend Analysis: Dynamic charting with configurable timeframes (24h, 7d, 30d, 1y).

Core Market Metrics: Immediate access to Market Cap, 24h Volume, and Circulating Supply.

2. Technical Analysis Suite
Trend Identification: Integrated Moving Averages, including customizable EMA and SMA overlays.

Risk Assessment: Volatility indicators designed to analyze price swings and market stability.

Momentum Oscillators: Standard technical indicators to identify overbought or oversold market conditions.

3. Blockchain & Network Insights
Network Health: Real-time monitoring of block height, network hash rate, and mining difficulty.

On-Chain Activity: Visual data representations of transaction trends and current mempool status.

4. Interactive Investment Simulator
P/L Calculator: Simulate potential returns based on historical entry points and capital allocation.

Virtual Portfolio: A dedicated mockup tool to track a virtual Bitcoin position and monitor performance.

Technical Stack
Frontend/UI: Streamlit

Data Processing: Pandas, NumPy

Visualization: Plotly, Matplotlib

Data Acquisition: Requests (via CoinGecko & Public Blockchain Nodes)

Local Installation
Ensure you have Python 3.8+ installed on your system.

Clone the Repository

Bash
git clone https://github.com/your-username/bitcoin-blockcraft.git
cd bitcoin-blockcraft
Environment Setup
It is recommended to use a virtual environment:

Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies

Bash
pip install -r requirements.txt
Run the Application

Bash
streamlit run app.py
Data Governance & Sources
To ensure data integrity and transparency, this application aggregates information from:

Market Data: CoinGecko API

Network Data: Public Blockchain Explorers and Node APIs

Disclaimer
This application is developed for educational and informational purposes only. The data, metrics, and simulations provided do not constitute financial, investment, or legal advice. Always perform independent research before making financial decisions.

License
Distributed under the MIT License. See LICENSE for more information.
