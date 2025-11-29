import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression
import re

st.set_page_config(
    page_title="Stock Market Chatbot",
    layout="wide",
    
    initial_sidebar_state="expanded"
)

USD_TO_INR = 82.0


FEATURE_KEYWORDS = {
    "stock_price": ["price", "stock price", "share price", "current price", "latest price", "quote", "cost"],
    "chart": ["chart", "graph", "history", "historical", "plot", "trend"],
    "compare": ["compare", "vs", "versus", "comparison", "relative performance"],
    "financial_terms": ["explain", "definition", "meaning", "what is", "define", "term", "financial term"],
    "prediction": ["predict", "forecast", "estimate", "future price", "price prediction", "price forecast"],
    "top_companies": ["top companies", "recommend", "best companies", "leading companies", "top stocks", "sector leaders"],
    "learning_resources": ["learning", "resources", "tutorial", "course", "guide", "education", "study"],
    "investment_roadmap": ["roadmap", "how to start", "begin investing", "investment steps", "investment guide", "start investing"]
}


financial_terms = {
    "stock": "A stock represents ownership in a company. When you buy a stock, you're buying a piece of that company.",
    "dividend": "A dividend is a payment made by a corporation to its shareholders, usually as a distribution of profits.",
    "market cap": "Market capitalization is the total value of a company's outstanding shares of stock.",
    "p/e ratio": "Price-to-earnings ratio is a valuation ratio of a company's current share price compared to its per-share earnings.",
    "bear market": "A bear market is when a market experiences prolonged price declines, typically when prices fall 20% or more.",
    "bull market": "A bull market is a period of time in financial markets when the price of an asset rises continuously.",
    "volatility": "Volatility refers to the amount of uncertainty or risk about the size of changes in a security's value.",
    "etf": "An Exchange Traded Fund (ETF) is a type of investment fund that tracks an index, sector, commodity, or other asset.",
    "blue chip": "Blue chip stocks are shares in large, well-established companies with a history of reliable performance.",
    "index": "A stock market index measures the performance of a group of stocks representing a particular segment of the market."
}

learning_resources = {
    "beginners": [
        "Investopedia - Stock Market Basics: https://www.investopedia.com/investing/how-to-start-investing/",
        "Khan Academy - Finance and Capital Markets: https://www.khanacademy.org/economics-finance-domain/core-finance",
        "The Balance - Investing for Beginners: https://www.thebalance.com/investing-for-beginners-4073643"
    ],
    "intermediate": [
        "A Random Walk Down Wall Street by Burton Malkiel",
        "MIT OpenCourseWare - Finance Theory I: https://ocw.mit.edu/courses/sloan-school-of-management/15-401-finance-theory-i-fall-2008/",
        "Morningstar's Investing Classroom: https://www.morningstar.com/start-investing"
    ],
    "advanced": [
        "Security Analysis by Benjamin Graham",
        "The Intelligent Investor by Benjamin Graham",
        "Yale University's Financial Markets Course: https://www.coursera.org/learn/financial-markets-global"
    ]
}

top_companies = {
    "technology": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"],
    "healthcare": ["JNJ", "PFE", "UNH", "ABBV", "MRK"],
    "finance": ["JPM", "BAC", "V", "MA", "BRK-B"],
    "consumer": ["PG", "KO", "PEP", "WMT", "COST"],
    "energy": ["XOM", "CVX", "COP", "SLB", "EOG"],
    "industrial": ["HON", "CAT", "UPS", "DE", "MMM"],
    "telecommunications": ["T", "VZ", "TMUS", "CMCSA", "NFLX"],
    "real estate": ["AMT", "PLD", "CCI", "EQIX", "SPG"]
}

investment_roadmap = [
    {"title": "1. Educate Yourself", "description": "Learn stock market basics through books, online courses, and tutorials. Understand terms like stocks, bonds, mutual funds, ETFs, dividends, and market indices."},
    {"title": "2. Set Clear Financial Goals", "description": "Define what you want to achieve (retirement, buying a home, etc.), your time horizon, and risk tolerance. Different goals require different investment approaches."},
    {"title": "3. Create a Budget", "description": "Determine how much money you can invest regularly. Start small if needed - even $50-100 per month is a good beginning."},
    {"title": "4. Build an Emergency Fund First", "description": "Before investing in stocks, save 3-6 months of living expenses in a readily accessible account for emergencies."},
    {"title": "5. Open a Brokerage Account", "description": "Research and select a brokerage firm that suits your needs. Consider factors like fees, minimum deposits, research tools, and user interface."},
    {"title": "6. Start with Index Funds or ETFs", "description": "For beginners, low-cost index funds or ETFs that track the overall market (like S&P 500) are often recommended as they provide instant diversification."},
    {"title": "7. Understand and Practice Diversification", "description": "Don't put all your money in one stock or sector. Spread investments across different assets to reduce risk."},
    {"title": "8. Begin Regular Investing", "description": "Consider dollar-cost averaging - investing a fixed amount regularly regardless of market conditions to reduce the impact of volatility."},
    {"title": "9. Monitor and Learn, But Don't Obsess", "description": "Check your investments periodically, but avoid daily monitoring which can lead to emotional decisions. The stock market is for long-term wealth building."},
    {"title": "10. Gradually Expand Your Portfolio", "description": "As you gain confidence and knowledge, you might want to add individual stocks or other investment vehicles to your portfolio."}
]

features = [
    {
        "name": "Stock Prices",
        "description": "Get current stock prices by asking about any ticker symbol.",
        "examples": [
            "Show stock price for AAPL",
            "What is the latest price of MSFT?",
            "Give me the share price of TSLA"
        ],
        "icon": "💰"
    },
    {
        "name": "Historical Charts",
        "description": "View stock price history charts over different time periods.",
        "examples": [
            "Show chart for AMZN",
            "Display historical trend for NVDA",
            "Plot the graph for GOOGL"
        ],
        "icon": "📊"
    },
    {
        "name": "Stock Comparison",
        "description": "Compare multiple stocks on the same chart to see relative performance.",
        "examples": [
            "Compare AAPL vs MSFT",
            "Show relative performance of TSLA and AMZN",
            "Stock comparison: GOOGL, MSFT, AAPL"
        ],
        "icon": "⚖️"
    },
    {
        "name": "Financial Terms",
        "description": "Learn about various financial and investment terms.",
        "examples": [
            "Explain P/E ratio",
            "What is dividend mean?",
            "Define market cap"
        ],
        "icon": "📘"
    },
    {
        "name": "Stock Prediction",
        "description": "Get simple predictions of future stock prices based on historical trends.",
        "examples": [
            "Predict NVDA stock for next 30 days",
            "Forecast AMZN stock",
            "Estimate AAPL stock"
        ],
        "icon": "🔮"
    },
    {
        "name": "Top Companies",
        "description": "Get recommendations for top companies by sector.",
        "examples": [
            "Recommend top technology companies",
            "Show top companies in healthcare ",
            " recommend top companies"
        ],
        "icon": "🏆"
    },
    {
        "name": "Learning Resources",
        "description": "Access curated resources to learn about investing at different expertise levels.",
        "examples": [
            "Show learning resources for beginners",
            "Advanced stock market tutorials"
        ],
        "icon": "📚"
    },
    {
        "name": "Investment Roadmap",
        "description": "Get a step-by-step guide on how to start investing in the stock market.",
        "examples": [
            "Show investment roadmap",
            "How do I start investing?",
            "Investment steps for beginners"
        ],
        "icon": "🗺️"
    }
]


def get_stock_data(ticker, period="1y"):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        info = stock.info
        if hist.empty:
            return None, None
        return hist, info
    except Exception:
        return None, None

def format_company_price(ticker):
    hist, info = get_stock_data(ticker)
    if hist is not None and not hist.empty:
        price = hist['Close'].iloc[-1]
        price_inr = price * USD_TO_INR
        return f"{ticker}: ${price:.2f} (₹{price_inr:.2f})"
    else:
        return f"{ticker}: Price unavailable"

def format_company_info(info):
    name = info.get('longName') or info.get('shortName') or "N/A"
    sector = info.get('sector', "N/A")
    market_cap = info.get('marketCap')
    market_cap_str = f"${market_cap / 1e9:.2f}B" if market_cap else "N/A"
    dividend_yield = info.get('dividendYield')
    dividend_str = f"{dividend_yield*100:.2f}%" if dividend_yield else "N/A"
    long_business_summary = info.get('longBusinessSummary', "No company bio available.")
    info_text = (
        f"**Company Name:** {name}\n\n"
        f"**Sector:** {sector}\n\n"
        f"**Market Cap:** {market_cap_str}\n\n"
        f"**Dividend Yield:** {dividend_str}\n\n"
        f"**Business Summary:**\n{long_business_summary}\n"
    )
    return info_text

def extract_tickers(text):
    return re.findall(r'\b[A-Z]{1,5}\b', text)

def match_feature(message_lower):
    for feature, keywords in FEATURE_KEYWORDS.items():
        for kw in keywords:
            if kw in message_lower:
                return feature
    return None

def plot_stock_chart(hist, ticker):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name=ticker))
    fig.update_layout(
        title=f"{ticker} Price Chart",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        legend_title="Ticker"
    )
    return fig

def compare_stocks(tickers, period="1y"):
    fig = go.Figure()
    valid_tickers = []
    for ticker in tickers:
        hist, _ = get_stock_data(ticker, period)
        if hist is not None and not hist.empty:
            norm_prices = hist['Close'] / hist['Close'].iloc[0] * 100
            fig.add_trace(go.Scatter(
                x=hist.index, y=norm_prices,
                mode='lines', name=ticker
            ))
            valid_tickers.append(ticker)
    if not valid_tickers:
        return None
    fig.update_layout(
        title=f"Stock Comparison: {', '.join(valid_tickers)}",
        xaxis_title="Date",
        yaxis_title="Normalized Price (Start=100)",
        legend_title="Ticker"
    )
    return fig

def predict_stock_price(hist, days=30):
    try:
        hist = hist.reset_index()
        hist['Date_ordinal'] = pd.to_datetime(hist['Date']).map(datetime.toordinal)
        X = hist['Date_ordinal'].values.reshape(-1, 1)
        y = hist['Close'].values
        model = LinearRegression()
        model.fit(X, y)
        last_date = hist['Date'].iloc[-1]
        future_dates = [last_date + timedelta(days=i) for i in range(1, days+1)]
        future_ordinals = np.array([d.toordinal() for d in future_dates]).reshape(-1, 1)
        predictions = model.predict(future_ordinals)
        return future_dates, predictions
    except Exception:
        return None, np.array([])

def plot_prediction(hist, ticker, future_dates, predictions):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name="Historical"))
    fig.add_trace(go.Scatter(x=future_dates, y=predictions, mode='lines', name="Prediction"))
    fig.update_layout(
        title=f"{ticker} Price Prediction",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        legend_title="Type"
    )
    return fig

def process_message(message):
    message_lower = message.lower()
    tickers = extract_tickers(message)
    feature = match_feature(message_lower)

    if "manual" in message_lower:
        manual = "**User Manual:**\n\n"
        for f in features:
            feature_key = f["name"].lower().replace(" ", "_")
            keywords = FEATURE_KEYWORDS.get(feature_key, [])
            manual += f"### {f['icon']} {f['name']}\n"
            manual += f"{f['description']}\n\n"
            manual += f"**Keywords:** {', '.join(keywords)}\n\n"
            manual += "**Examples:**\n"
            for ex in f['examples']:
                manual += f"- {ex}\n"
            manual += "\n---\n\n"
        return manual, None

    if feature == "financial_terms":
        for term, explanation in financial_terms.items():
            if term in message_lower:
                return f"**{term.title()}**: {explanation}", None
        return "❌ Sorry, financial term not found. Try another term.", None

    if feature == "learning_resources":
        level = "beginners"
        if "intermediate" in message_lower:
            level = "intermediate"
        elif "advanced" in message_lower:
            level = "advanced"
        resources_text = f"**{level.title()} Learning Resources:**\n\n"
        for res in learning_resources[level]:
            resources_text += f"- {res}\n"
        return resources_text, None

    if feature == "investment_roadmap":
        roadmap_text = "**Investment Roadmap:**\n\n"
        for step in investment_roadmap:
            roadmap_text += f"**{step['title']}**\n{step['description']}\n\n"
        return roadmap_text, None

    if feature == "top_companies":
        sector = None
        for s in top_companies.keys():
            if s in message_lower:
                sector = s
                break
        if sector:
            companies_text = f"**Top {sector.title()} Companies (with latest prices):**\n\n"
            for ticker in top_companies[sector]:
                companies_text += f"- {format_company_price(ticker)}\n"
            return companies_text, None
        else:
            sectors_text = "**Available Sectors:**\n\n"
            for s in top_companies.keys():
                sectors_text += f"- {s.title()}\n"
            return sectors_text, None

    if feature == "stock_price" and tickers:
        ticker = tickers[0]
        hist, info = get_stock_data(ticker)
        if hist is not None and not hist.empty and info is not None:
            current_price_usd = hist['Close'].iloc[-1]
            price_change = hist['Close'].iloc[-1] - hist['Close'].iloc[-2]
            pct_change = (price_change / hist['Close'].iloc[-2]) * 100
            direction = "📈" if price_change > 0 else "📉"
            current_price_inr = current_price_usd * USD_TO_INR
            info_text = format_company_info(info)
            response = (
                f"{ticker} Current Price: ${current_price_usd:.2f} (₹{current_price_inr:.2f}) {direction}\n\n"
                f"Change: ${price_change:.2f} ({pct_change:.2f}%)\n\n"
                f"{info_text}"
            )
            return response, None
        else:
            return f"❌ Could not retrieve price data for {ticker}.", None

    if feature == "chart" and tickers:
        ticker = tickers[0]
        period = "1y"
        if any(p in message_lower for p in ["5y", "five year", "five years"]):
            period = "5y"
        elif any(p in message_lower for p in ["2y", "two year", "two years"]):
            period = "2y"
        elif any(p in message_lower for p in ["6m", "six month", "six months"]):
            period = "6mo"
        elif any(p in message_lower for p in ["1m", "one month"]):
            period = "1mo"
        hist, _ = get_stock_data(ticker, period)
        if hist is not None and not hist.empty:
            chart = plot_stock_chart(hist, ticker)
            return f"Here's the {period} chart for {ticker}:", chart
        else:
            return f"❌ Could not retrieve chart data for {ticker}.", None

    if feature == "compare" and len(tickers) > 1:
        period = "1y"
        chart = compare_stocks(tickers, period)
        if chart:
            return f"Here's a comparison of {', '.join(tickers)}:", chart
        else:
            return f"❌ Could not compare stocks {', '.join(tickers)}.", None

    if feature == "prediction":
        if tickers:
            ticker = tickers[0]
            days = 30
            days_match = re.search(r'(\d+)\s*days?', message_lower)
            if days_match:
                days = int(days_match.group(1))
            hist, _ = get_stock_data(ticker)
            if hist is not None and not hist.empty:
                future_dates, predictions = predict_stock_price(hist, days)
                if future_dates is not None and predictions.size > 0:
                    chart = plot_prediction(hist, ticker, future_dates, predictions)
                    return f"Here's the {days}-day price prediction for {ticker}:", chart
                else:
                    return f"❌ Prediction failed for {ticker}.", None
            else:
                return f"❌ Could not retrieve data for {ticker}.", None

    return "❌ Sorry, I couldn't understand your request. Try asking about stock prices, charts, comparison, or type 'manual' for help.", None

# --- Streamlit UI ---

if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ""
if 'last_example' not in st.session_state:
    st.session_state['last_example'] = ""

st.title(" Stock Market chatbot")
st.markdown("Ask me about stock prices, charts, comparisons, financial terms, predictions, and more!")

st.sidebar.header("Features & Examples")

for f in features:
    with st.sidebar.expander(f"{f['icon']} {f['name']}", expanded=False):
        st.sidebar.markdown(f"_{f['description']}_")
        for example in f["examples"]:
            if st.button(example, key=f"btn_{f['name']}_{example}"):
                st.session_state['user_input'] = example
                st.session_state['last_example'] = example

user_input = st.text_input("Type your query here:", value=st.session_state['user_input'], key="main_input")
if user_input != st.session_state['user_input']:
    st.session_state['user_input'] = user_input

if user_input:
    response, chart = process_message(user_input)
    st.markdown(response)
    if chart is not None:
        st.plotly_chart(chart, use_container_width=True)
