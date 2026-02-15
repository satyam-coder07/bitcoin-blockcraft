Bitcoin Blockcraft: Market & Network Analysis Engine

Live Demo: [Explore the Interactive Dashboard](https://bitcoin-blockcraft.streamlit.app/)

Live Features

Real-Time Market Monitoring: Dynamic Bitcoin price tracking with sub-minute refresh rates using high-reliability exchange APIs.

On-Chain Telemetry: Direct visualization of blockchain health, including hash rate fluctuations and mempool congestion.

Profit/Loss Simulation: Interactive engine allowing users to simulate portfolio performance using weighted historical entry points.

Technical Overlay: Toggleable EMA/SMA indicators and volatility bands for advanced trend identification.

Project Context (2026)

This repository serves as an advanced implementation of a financial telemetry dashboard focused on the intersection of FinTech and Data Engineering.

It demonstrates how raw, high-frequency JSON market and blockchain data can be transformed into structured, actionable intelligence through interactive visualization.

Prototype Objectives

The goal of this engine is to demonstrate a robust architecture for handling real-time financial data streams.

By unifying market price action with underlying blockchain health checks, the tool provides a holistic view of the Bitcoin ecosystem.

Core Objectives

Unified Data Schema: Structured ingestion of market and blockchain data using Python dataclasses for type-safe processing.

High-Fidelity Visualization: Interactive time-series charts (via Plotly) featuring dynamic threshold markers and volatility analysis.

Simulation Logic: Weighted calculation engine for historical price backtracking and portfolio modeling.

Zero-Cost Execution: Fully optimized to run using open-source libraries and public API tiers (no paid credentials required).

🏗 Technical Architecture

The dashboard follows a modular and scalable Python structure:

Data Acquisition Layer

Handles asynchronous API polling for:

Market price feeds

Blockchain network telemetry

Processing Engine

Utilizes Pandas and NumPy

Performs real-time mathematical transformations

Computes technical indicators (EMA, SMA, volatility bands)

Visualization Layer

Built using Plotly

Hover-active time-series analysis

Interactive threshold markers and spike detection

State Management

Powered by Streamlit Session State

Maintains portfolio allocations and simulation inputs during runtime

⚙ Installation & Usage
1. Clone the Repository

'''bash
git clone https://github.com/satyam-coder07/bitcoin-blockcraft.git

cd bitcoin-blockcraft
'''

2. Install Dependencies

'''bash
pip install -r requirements.txt
'''

3. Launch the Analysis Engine

'''bash
streamlit run app.py
'''

Implementation Details

Frontend/UI: Streamlit (Customized CSS for professional layout)

Data Processing: Pandas, NumPy

Visualization: Plotly

Connectivity: Requests / API polling logic

Environment: Python 3.9+

Disclaimer

This repository is intended strictly for educational and informational purposes.

It provides a framework for financial data visualization and simulation and does not constitute financial, trading, or investment advice.

License

Distributed under the MIT License.
