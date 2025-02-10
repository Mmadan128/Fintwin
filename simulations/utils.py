import yfinance as yf

def get_stock_data(stock_symbols):
    # Download stock data for the symbols
    data = yf.download(stock_symbols, period="1d", group_by='ticker', auto_adjust=True)
    
    if data.empty:
        return [], []  # Return empty lists if no data is retrieved

    stock_changes = []
    for symbol in stock_symbols:
        # Check if the data for each symbol is available
        stock_data = data[symbol]
        if stock_data.empty:
            continue
        
        open_price = stock_data['Open'][0]
        close_price = stock_data['Close'][0]
        change_percent = ((close_price - open_price) / open_price) * 100
        stock_changes.append((symbol, change_percent))

    # Separate gainers and losers
    gainers = [stock for stock in stock_changes if stock[1] > 0]
    losers = [stock for stock in stock_changes if stock[1] < 0]

    # Sort gainers and losers
    gainers = sorted(gainers, key=lambda x: x[1], reverse=True)
    losers = sorted(losers, key=lambda x: x[1])

    return gainers, losers
