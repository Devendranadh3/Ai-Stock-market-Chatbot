# 📈 Stock Market Chatbot

An interactive **Stock Market Chatbot** built using **Streamlit**, **Yahoo Finance (yFinance)**, and **Machine Learning**.  
This chatbot allows users to fetch real-time stock prices, visualize historical trends, compare stocks, predict future prices, and learn stock market concepts using simple natural language queries.


## 🚀 Features

### 💰 Stock Prices
- Fetch latest stock prices in **USD and INR**
- Shows **daily change & percentage**
- Displays company details like sector, market cap, and dividend yield

**Example Queries**
- Show stock price for AAPL  
- What is the latest price of TSLA?


### 📊 Historical Stock Charts
- Interactive price charts using Plotly
- Supported periods:
  - 1 Month
  - 6 Months
  - 1 Year
  - 2 Years
  - 5 Years

**Example Queries**
- Show chart for NVDA  
- Plot AMZN for 5 years


### ⚖️ Stock Comparison
- Compare multiple stocks on a single normalized chart
- Helps analyze relative performance

**Example Queries**
- Compare AAPL vs MSFT  
- Stock comparison: GOOGL, AMZN, TSLA


### 🔮 Stock Price Prediction
- Predict future stock prices using **Linear Regression**
- User-defined prediction days

**Example Queries**
- Predict AAPL stock for next 30 days  
- Forecast NVDA stock

> ⚠️ Predictions are for educational purposes only.


### 📘 Financial Terms Explanation
- Explains common stock market terms

**Example Queries**
- Explain P/E ratio  
- What is dividend?  
- Define market cap


### 🏆 Top Companies by Sector
- Recommends top companies with latest prices

**Available Sectors**
- Technology
- Healthcare
- Finance
- Energy
- Consumer
- Industrial
- Telecommunications
- Real Estate

**Example Queries**
- Recommend top technology companies  
- Top healthcare stocks


### 📚 Learning Resources
- Curated resources for:
  - Beginners
  - Intermediate
  - Advanced learners

**Example Queries**
- Learning resources for beginners  
- Advanced stock market tutorials


### 🗺️ Investment Roadmap
- Step-by-step guide for beginners
- Covers budgeting, diversification, and long-term investing

**Example Queries**
- How do I start investing?  
- Show investment roadmap


## 🧠 Tech Stack

| Technology | Purpose |
|---------|--------|
| Python | Core programming |
| Streamlit | Web UI |
| yFinance | Stock market data |
| Plotly | Interactive charts |
| Pandas & NumPy | Data processing |
| Scikit-learn | Price prediction |
| Regex | Query parsing |


## 📂 Project Structure

stock-market-chatbot/
│
├── app.py
├── README.md
├── requirements.txt


## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

git clone https://github.com/your-username/stock-market-chatbot.git
cd stock-market-chatbot

### 2️⃣ Install Dependencies
pip install -r requirements.txt

### 3️⃣ Run the Application
streamlit run app.py

### 📦 requirements.txt
streamlit
pandas
numpy
yfinance
plotly
scikit-learn

### 🧪 Sample Queries
Show stock price for AAPL
Compare MSFT vs GOOGL
Predict NVDA stock for next 15 days
Explain bull market
Top companies in finance
Learning resources for beginners
