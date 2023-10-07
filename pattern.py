import mplfinance as mpf
import pandas as pd
import yfinance as yf

# Define functions to identify candlestick patterns
def is_hammer(row):
    high, low, open, close = row['High'], row['Low'], row['Open'], row['Close']
    condition1 = (high - low) > 3 * (open - close)
    condition2 = (close - low) / (0.001 + high - low) > 0.6 
    condition3 = (open - low) / (0.001 + high - low) > 0.6
    return condition1 and condition2 and condition3

def is_inverted_hammer(row):
    high, low, open, close = row['High'], row['Low'], row['Open'], row['Close']
    condition1 = (high - low) > 3 * (open - close)
    condition2 = (high - low) / (0.001 + high - low) > 0.6
    condition3 = (high - open) / (0.001 + high - low) > 0.6
    return condition1 and condition2 and condition3

def is_doji(row, doji_size):
    high, close, open, low = row['High'], row['Close'], row['Open'], row['Low']
    doji = abs(open - close) <= (high - low) * doji_size
    return doji

# Define the date range
start_date = "2023-01-01"
end_date = "2023-03-01"

# Fetch historical data for Nifty 50 index
nifty_data = yf.Ticker('^NSEI')
nifty_history = nifty_data.history(period="1d", start=start_date, end=end_date)

# Create a DataFrame with 'Open', 'High', 'Low', 'Close' columns
ohlc_df = nifty_history[['Open', 'High', 'Low', 'Close']]

# Add a 'Date' column
ohlc_df['Date'] = ohlc_df.index

doji_size = 0.01

# Identify candlestick patterns
ohlc_df['Hammer'] = ohlc_df.apply(is_hammer, axis=1).astype(bool)
ohlc_df['InvertedHammer'] = ohlc_df.apply(is_inverted_hammer, axis=1).astype(bool)
ohlc_df['Doji'] = ohlc_df.apply(is_doji, axis=1, doji_size=doji_size).astype(bool)


# Create plots with diamond markers based on the identified patterns

if ohlc_df['Hammer'].any():
    hammer_df = ohlc_df[ohlc_df['Hammer']]
    hammer_df = hammer_df.reindex(ohlc_df.index)
    hammer_markers = mpf.make_addplot(hammer_df['High'], scatter=True, markersize=100, marker='D', color='green')
else:
    hammer_markers = None

if ohlc_df['InvertedHammer'].any():
    inverted_hammer_df = ohlc_df[ohlc_df['InvertedHammer']]
    inverted_hammer_df = inverted_hammer_df.reindex(ohlc_df.index)
    inverted_hammer_markers = mpf.make_addplot(inverted_hammer_df['High'], scatter=True, markersize=100, marker='D', color='black')
else:
    inverted_hammer_markers = None


if ohlc_df['Doji'].any():
    Doji_df = ohlc_df[ohlc_df['Doji']]
    Doji_df = Doji_df.reindex(ohlc_df.index)
    Doji_markers = mpf.make_addplot(Doji_df['High'], scatter=True, markersize=100, marker='D', color='red')
    
else:
    Doji_markers = None


condition1 = ohlc_df['Open'].shift(1)> ohlc_df['Close'].shift(1)
condition2 = ohlc_df['Close'] > ohlc_df['Open']
condition3 = ohlc_df['Close'] >= ohlc_df['Open'].shift(1)  
condition4 = ohlc_df['Open']<=ohlc_df['Close'].shift(1)
condition5 = ohlc_df['Close']-ohlc_df['Open']>ohlc_df['Open'].shift(1)-ohlc_df['Close'].shift(1)

# Calculate the conditions for the bullish harami pattern
# Combine the conditions to identify the bullish harami pattern
bull_engulf = condition1 & condition2 & condition3 & condition4 & condition5

# Create an empty DataFrame to hold Bull Harami markers
bullengulf_df = pd.DataFrame(index=ohlc_df.index)
bullengulf_df['BullEngulf'] = bull_engulf
bullengulf_df['BullEngulfHigh'] = ohlc_df['High'][bull_engulf]

# Create Bull Harami markers for the candlestick chart
bullengulf_markers = mpf.make_addplot(bullharami_df['BullEngulfHigh'], scatter=True, markersize=100, marker='D', color='violet')


#Bear engulf

condition1 = ohlc_df['Open'].shift(1)< ohlc_df['Close'].shift(1)
condition2 = ohlc_df['Close'] < ohlc_df['Open']
condition3 = ohlc_df['Close'] <= ohlc_df['Open'].shift(1)  
condition4 = ohlc_df['Open']>=ohlc_df['Close'].shift(1)
condition5 = ohlc_df['Open']-ohlc_df['Close']>ohlc_df['Close'].shift(1)-ohlc_df['Open'].shift(1)

# Calculate the conditions for the bullish harami pattern
# Combine the conditions to identify the bullish harami pattern
bear_engulf = condition1 & condition2 & condition3 & condition4 & condition5

# Create an empty DataFrame to hold Bull Harami markers
bearengulf_df = pd.DataFrame(index=ohlc_df.index)
bearengulf_df['BearEngulf'] = bear_engulf
bearengulf_df['BearEngulfHigh'] = ohlc_df['High'][bear_engulf]

# Create Bull Harami markers for the candlestick chart
bearengulf_markers = mpf.make_addplot(bullharami_df['BearEngulfHigh'], scatter=True, markersize=100, marker='D', color='violet')

#bearharami

condition1 = ohlc_df['Close'].shift(1)> ohlc_df['Open'].shift(1)
condition2 = ohlc_df['Open'] > ohlc_df['Close']
condition3 = ohlc_df['High'] < ohlc_df['High'].shift(1)  
condition4 = ohlc_df['Low']>ohlc_df['Low'].shift(1)


# Calculate the conditions for the bullish harami pattern
# Combine the conditions to identify the bullish harami pattern
bear_harami = condition1 & condition2 & condition3 & condition4

# Create an empty DataFrame to hold Bull Harami markers
bearharami_df = pd.DataFrame(index=ohlc_df.index)
bearharami_df['BearHarami'] = bear_harami
bearharami_df['BearHaramiHigh'] = ohlc_df['High'][bear_harami]

# Create Bull Harami markers for the candlestick chart
bearharami_markers = mpf.make_addplot(bearharami_df['BearHaramiHigh'], scatter=True, markersize=100, marker='D', color='red')

#bull harami

condition1 = ohlc_df['Open'].shift(1)> ohlc_df['Close'].shift(1)
condition2 = ohlc_df['Close'] > ohlc_df['Open']
condition3 = ohlc_df['High'] < ohlc_df['High'].shift(1)  
condition4 = ohlc_df['Low']>ohlc_df['Low'].shift(1)


# Calculate the conditions for the bullish harami pattern
# Combine the conditions to identify the bullish harami pattern
bull_harami = condition1 & condition2 & condition3 & condition4

# Create an empty DataFrame to hold Bull Harami markers
bullharami_df = pd.DataFrame(index=ohlc_df.index)
bullharami_df['BullHarami'] = bull_harami
bullharami_df['BullHaramiHigh'] = ohlc_df['High'][bull_harami]

# Create Bull Harami markers for the candlestick chart
bullharami_markers = mpf.make_addplot(bullharami_df['BullHaramiHigh'], scatter=True, markersize=100, marker='D', color='red')

mpf.plot(ohlc_df, type='candle', title='Nifty 50 Index Candlestick Patterns',
         ylabel='Price', figscale=1.5, style='yahoo',
         addplot=[hammer_markers, inverted_hammer_markers, Doji_markers,bearengulf_markers,bullengulf_markers,bearharami_markers,bullharami_markers])
