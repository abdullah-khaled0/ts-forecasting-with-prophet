# Import necessary libraries
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
from prophet import Prophet

# Function to load data from Yahoo Finance
def load_data(ticker, period="max", interval="1d"):
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    df = df.reset_index()
    df.columns = df.columns.str.lower()
    
    # Remove timezone information from the date column
    df['date'] = pd.to_datetime(df['date']).dt.tz_localize(None)
    
    return df

# Function to filter data by date range
def filter_data_by_date(df, start_date, end_date):
    # Ensure the start and end date are in datetime format
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    df_filtered = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    return df_filtered

# Function to aggregate data by selected period (daily, monthly, yearly)
def aggregate_data(df, period):
    if period == 'Monthly':
        df_agg = df.resample('M', on='date').mean().reset_index()
    elif period == 'Yearly':
        df_agg = df.resample('Y', on='date').mean().reset_index()
    else:
        df_agg = df
    return df_agg

# Function to plot candlestick chart
def plot_candlestick(df):
    trace = go.Candlestick(
        x=df['date'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        increasing=dict(line=dict(color='#58FA58')),
        decreasing=dict(line=dict(color='#FA5858'))
    )

    layout = {
        'title': f"Stock Historical Price",
        'xaxis': {'title': 'Date', 'rangeslider': {'visible': False}},
        'yaxis': {'title': 'Stock Price (USD$)'}
    }

    fig = go.Figure(data=[trace], layout=layout)
    st.plotly_chart(fig)

# Function to forecast stock prices
def forecast_stock(df, periods):
    st.write("## Stock Price Forecast")
    # Prepare data for Prophet
    df_prophet = df[['date', 'close']].rename(columns={'date': 'ds', 'close': 'y'})
    
    model = Prophet()
    model.fit(df_prophet)

    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)

    # Plot forecast
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], mode='lines', name='Lower CI', line=dict(dash='dash')))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], mode='lines', name='Upper CI', fill='tonexty'))
    
    fig.update_layout(title="Price Forecast with Confidence Intervals", xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(fig)

    # Plot forecast components
    fig_components = model.plot_components(forecast)
    st.pyplot(fig_components)

# Streamlit app layout
def main():
    st.title("Stock Price Analysis and Forecasting App📈")

    # Sidebar input for stock ticker
    st.sidebar.header("Stock Data Filters")
    ticker = st.sidebar.text_input("Enter the stock ticker:", "AMZN")

    # Sidebar input for data frequency
    interval = st.sidebar.selectbox("Select data frequency:", ["1d", "1wk", "1mo"])

    # Load stock data
    df = load_data(ticker, interval=interval)

    # Sidebar input for date range filter, restricted to available data
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
    end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

    if start_date > end_date:
        st.error("Error: End date must fall after start date.")
        return

    df_filtered = filter_data_by_date(df, start_date, end_date)

    # Sidebar input for selecting metrics to display
    metrics = ['Close', 'High', 'Low', 'Volume']
    selected_metrics = st.sidebar.multiselect("Select metrics to display:", metrics, default=['Close'])

    # Sidebar input for aggregation period
    period = st.sidebar.selectbox("Select aggregation period:", ['Daily', 'Monthly', 'Yearly'])

    # Aggregate data by selected period
    df_agg = aggregate_data(df_filtered, period)

    # Show brief description of filtered data
    st.write("### Data Overview")
    st.dataframe(df_agg.describe())

    # Display candlestick chart for the selected period
    plot_candlestick(df_agg)

    # Sidebar input for forecast period
    forecast_period = st.sidebar.slider("Select the forecast period (in days):", 30, 365, step=30)

    # Forecasting using Prophet
    forecast_stock(df_filtered, periods=forecast_period)

if __name__ == "__main__":
    main()
