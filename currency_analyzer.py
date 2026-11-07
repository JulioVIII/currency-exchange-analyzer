import requests
import pandas as pd
from datetime import date, timedelta


# 1. DATE RANGE
end_date = date.today()
start_date = end_date - timedelta(days=30)

print("===== CURRENCY EXCHANGE RATE ANALYZER =====")
print(f"Period: {start_date} to {end_date}")


# 2. API CONNECTION
url = (
    f"https://api.frankfurter.app/"
    f"{start_date}..{end_date}?from=EUR&to=USD,GBP,JPY"
)

try:
    response = requests.get(url, timeout=15)

    # Check if the request was successful
    response.raise_for_status()

    # Convert JSON response into Python dictionary
    data = response.json()

except requests.exceptions.RequestException as error:
    print("Connection error:", error)
    raise SystemExit(1)


# 3. CHECK API DATA
if not data.get("rates"):
    print("No exchange rate data available.")
    raise SystemExit(0)


# 4. CONVERT JSON DATA INTO PANDAS DATAFRAME
df = pd.DataFrame.from_dict(
    data["rates"],
    orient="index"
)

df.index.name = "Date"
df = df.reset_index()

# Convert Date column into datetime format
df["Date"] = pd.to_datetime(df["Date"])

# Sort records by date
df = df.sort_values("Date")


# 5. DISPLAY DATA
print("\n===== EXCHANGE RATE DATA =====")
print(df.to_string(index=False))


# 6. BASIC STATISTICS
currencies = ["USD", "GBP", "JPY"]

print("\n===== AVERAGE EXCHANGE RATES =====")

for currency in currencies:
    print(f"EUR to {currency}: {df[currency].mean():.4f}")


print("\n===== HIGHEST EXCHANGE RATES =====")

for currency in currencies:
    print(f"EUR to {currency}: {df[currency].max():.4f}")


print("\n===== LOWEST EXCHANGE RATES =====")

for currency in currencies:
    print(f"EUR to {currency}: {df[currency].min():.4f}")


# 7. FIRST AND LAST AVAILABLE RATE
print("\n===== RATE CHANGE =====")

for currency in currencies:
    first_rate = df[currency].iloc[0]
    last_rate = df[currency].iloc[-1]

    percentage_change = (
        (last_rate - first_rate) / first_rate
    ) * 100

    print(
        f"{currency}: {percentage_change:.2f}% "
        "change during the period"
    )


# 8. SAVE DATA TO CSV
df.to_csv("exchange_rates.csv", index=False)

print("\nData saved to exchange_rates.csv")


# 9. FINAL SUMMARY
print("\n===== ANALYSIS SUMMARY =====")
print("Number of records:", len(df))
print("Currencies analysed:", len(currencies))
print("First available date:", df["Date"].min().date())
print("Last available date:", df["Date"].max().date())
