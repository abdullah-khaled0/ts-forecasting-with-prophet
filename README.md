# Time Series Forecast with Prophet

![](https://www.timescale.com/blog/content/images/2022/06/candlesticks-2.png)

## 📚 Introduction
This repository demonstrates a time series forecasting project using **Prophet**, Facebook's open-source library designed for forecasting tasks. In this project, we aim to forecast stock prices. It's important to note that historical prices alone do not indicate whether a price will rise or fall. Instead, we will leverage additional variables and utilize machine learning techniques for stock price prediction, going beyond mere historical analysis.

## 🔍 Summary about Prophet
Facebook's research team developed Prophet to provide an accessible implementation of forecasting methods. As noted in their blog, high-quality forecasting data produced by analysts is rarely seen, which motivated the creation of this library. Prophet offers an approachable way for both experts and non-experts to utilize advanced time series forecasting concepts. It closely resembles the Scikit-Learn API, making it familiar for Python users. For more detailed insights, you can refer to the [Prophet Blog](https://facebook.github.io/prophet/).


## 📈 Streamlit App
This project includes a **Streamlit** app that provides an interactive interface for stock price analysis and forecasting.

### Features
- Load stock data from Yahoo Finance using a stock ticker.
- Visualize historical stock prices with candlestick charts.
- Filter data by date range and aggregate it by daily, monthly, or yearly intervals.
- Forecast future stock prices using the Prophet model with user-defined forecast periods.
- Display statistical metrics of the selected data.

### How to Run the App
To run the Streamlit app, use the following command in your terminal:

```bash
streamlit run app.py
