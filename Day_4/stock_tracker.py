import random

SAMPLE_PRICES = [
    412, 398, 425, 441, 389, 402, 418,   # week 1
    375, 361, 390, 410, 430, 445, 420,   # week 2
    438, 452, 467, 455, 471, 480, 462,   # week 3
    449, 435, 460, 475, 488, 495, 479,   # week 4
    502, 515,                             # extra days
]


def max_profit(prices: list) -> tuple:
    """One pass O(n). Returns (buy_day, sell_day, profit)."""
    min_price  = prices[0]
    min_day    = 0
    best_buy   = 0
    best_sell  = 0
    max_profit = 0

    for i, price in enumerate(prices[1:], start=1):
        if price < min_price:
            min_price = price
            min_day   = i
        gain = price - min_price
        if gain > max_profit:
            max_profit = gain
            best_buy   = min_day
            best_sell  = i

    return best_buy, best_sell, max_profit


def moving_average(prices: list, window: int = 7) -> list:
    """Sliding window. Returns list of (start_day, avg)."""
    result = []
    for i in range(len(prices) - window + 1):
        avg = sum(prices[i : i + window]) / window
        result.append((i, round(avg, 2)))
    return result


def most_volatile_week(prices: list, window: int = 7) -> tuple:
    """Max (high - low) swing in any 7-day window. Returns (start_day, swing)."""
    best_start = 0
    best_swing = 0

    for i in range(len(prices) - window + 1):
        week   = prices[i : i + window]
        swing  = max(week) - min(week)
        if swing > best_swing:          # strictly greater keeps earlier week on tie
            best_swing = swing
            best_start = i

    return best_start, best_swing


def print_report(prices: list) -> None:
    print(f"\nPrices ({len(prices)} days):")
    for i in range(0, len(prices), 7):
        week = prices[i : i + 7]
        print(f"  Week {i // 7 + 1}: {week}")

    buy, sell, profit = max_profit(prices)
    print(f"\nMax Profit:")
    print(f"  Buy  Day {buy + 1:>2}  @ Rs.{prices[buy]}")
    print(f"  Sell Day {sell + 1:>2}  @ Rs.{prices[sell]}")
    print(f"  Profit: Rs.{profit}")

    avgs = moving_average(prices)
    print(f"\n7-Day Moving Averages:")
    for start, avg in avgs:
        print(f"  Day {start + 1:>2}-{start + 7:>2}: {avg}")

    week_start, swing = most_volatile_week(prices)
    week_prices = prices[week_start : week_start + 7]
    print(f"\nMost Volatile Week:")
    print(f"  Days {week_start + 1}–{week_start + 7}: {week_prices}")
    print(f"  Swing: Rs.{swing}  (high {max(week_prices)} – low {min(week_prices)})")


if __name__ == "__main__":
    choice = input("Use sample prices? (y/n, default y): ").strip().lower()

    if choice == "n":
        raw = input("Enter 30 comma-separated prices: ")
        try:
            prices = [float(x.strip()) for x in raw.split(",")]
            if len(prices) < 7:
                print("Need at least 7 prices. Using sample data.")
                prices = SAMPLE_PRICES
        except ValueError:
            print("Invalid input. Using sample data.")
            prices = SAMPLE_PRICES
    else:
        prices = SAMPLE_PRICES

    print_report(prices)