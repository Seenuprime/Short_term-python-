# This function identifies stocks that are near their previous high and above or below 400.
#
# Inputs:
#   data: The name of the CSV file containing the list of stock symbols.
#   datato: The name of the CSV file to save the stocks above 400 to.
#   datato1: The name of the CSV file to save the stocks below 400 to.
#
# Outputs:
#   A simple message
#   And creates 2 csv files and stores the Stock names
def get_stocks_below_price(data, datato, datato1):
  # Read the CSV file containing the list of stock symbols.
  df = pd.read_csv(f"{data}.csv")

  # Create two empty lists to store the stock symbols above and below 400.
  above_400 = []
  below_400 = []

  # Iterate over the stock symbols.
  for symbol in stock_symbols:
    # Create the full stock symbol by adding ".NS".
    full_symbol = symbol + ".NS"

    # Download the stock data for the past year.
    stock_data = yf.download(full_symbol, period="1y", progress=True)

    # If there is no data available for the stock, skip it.
    if stock_data.empty:
      print(f"No data available for {symbol}.")
      continue

    # Get the previous high for the stock.
    previous_high = stock_data["High"].max()

    # If there is not enough data available for the stock, skip it.
    if pd.isnull(previous_high):
      print(f"Not enough data available for {symbol}.")
      continue

    # Get the latest close and open prices for the stock.
    latest_close = stock_data["Close"][-1]
    latest_open = stock_data["Open"][-1]

    # Calculate the percentage difference between the latest close and previous high.
    percentage_difference = ((latest_close - previous_high) / previous_high) * 100

    # If the latest close is greater than the latest open, it is a bullish candle.
    if latest_close > latest_open:

      # If the latest close is below 700, above 400, and the percentage difference is within 5%,
      # then the stock is near its previous high and above 400.
      if (
          latest_close < 700
          and latest_close > 400
          and abs(percentage_difference) <= 5
      ):
        above_400.append(symbol)
        print(f"{symbol} is near its previous high and above 400.\n")

      # Otherwise, if the latest close is below 400 and the percentage difference is within 5%,
      # then the stock is near its previous high and below 400.
      elif latest_close < 400 and abs(percentage_difference) <= 5:
        below_400.append(symbol)
        print(f"{symbol} is near its previous high and below 400.\n")

  # Create DataFrames of the stocks above and below 400.
  dataframe = pd.DataFrame({"Stock Names": above_400})
  dataframe1 = pd.DataFrame({"Stock Name": below_400})

  # Save the DataFrames to CSV files.
  dataframe.to_csv(f"{datato}.csv", index=False)
  dataframe1.to_csv(f"{datato1}.csv", index=False)

  # Print a message indicating that the stock names have been saved.
  print(f"Stock names saved to '{datato}.csv' and '{datato1}.csv'.")

