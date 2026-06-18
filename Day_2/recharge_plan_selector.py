# Ask user for their budget and usage preference (calls / data / both).
# Recommend the best recharge plan from 3 options 
# show what they save vs the next plan. 

plans = {
    "calls": [
        {"name": "Basic", "price": 199, "calls": "Unlimited", "data": "100MB/day", "validity": "28 days"},
        {"name": "Mid", "price": 239, "calls": "Unlimited", "data": "300MB/day", "validity": "28 days"},
        {"name": "Premium", "price": 299, "calls": "Unlimited", "data": "500MB/day", "validity": "56 days"}
    ],

    "data": [
        {"name": "Basic", "price": 199, "data": "1GB/day", "caxx`lls": "100 mins/day", "validity": "28 days"},
        {"name": "Mid", "price": 239, "data": "1.5GB/day", "calls": "Unlimited", "validity": "28 days"},
        {"name": "Premium", "price": 299, "data": "2GB/day", "calls": "Unlimited", "validity": "56 days"}
    ],

    "both": [
        {"name": "Basic", "price": 199, "data": "1GB/day", "calls": "Unlimited", "sms": "100/day", "validity": "28 days"},
        {"name": "Mid", "price": 239, "data": "1.5GB/day", "calls": "Unlimited", "sms": "100/day", "validity": "28 days"},
        {"name": "Premium", "price": 299, "data": "2GB/day", "calls": "Unlimited", "sms": "100/day", "validity": "56 days"}
    ]
}

budget = int(input("Enter your budget (₹): "))
preference = input("Enter preference (calls/data/both): ").lower()

if preference not in plans:
    print("Invalid preference entered.")
else:
    available_plans = plans[preference]

    affordable = [plan for plan in available_plans if plan["price"] <= budget]

    if not affordable:
        print(f"Sorry, no plans available for ₹{budget}.")
        print(f"Minimum budget needed: ₹{available_plans[0]['price']}")
    else:
        best = affordable[-1]

        print(f"\nBest Plan: ₹{best['price']} ({best['name']})")

        if preference == "calls":
            print(f"Features: {best['calls']} calls, "f"{best['data']}, {best['validity']}")

        elif preference == "data":
            print(f"Features: {best['data']}, "f"{best['validity']}, {best['calls']} calls")

        else:
            print(f"Features: {best['data']}, "f"{best['calls']} calls, "f"{best['sms']} SMS/day, "f"{best['validity']}" )

        current_index = available_plans.index(best)

        if current_index < len(available_plans) - 1:
            next_plan = available_plans[current_index + 1]
            savings = next_plan["price"] - best["price"]

            print(f"You save ₹{savings} vs the ₹{next_plan['price']} "f"plan (out of budget)")
        else:
            print("You save ₹0 (this is the top plan!)")

        if current_index > 0:
            lower_plan = available_plans[current_index - 1]

            if preference in ["data", "both"]:
                current_data = float(best["data"].replace("GB/day", ""))
                lower_data = float(lower_plan["data"].replace("GB/day", ""))

                extra = current_data - lower_data

                print(f"Extra data vs ₹{lower_plan['price']} plan: "f"+{extra}GB/day")

            else:
                print( f"Extra data vs ₹{lower_plan['price']} plan: "f"{lower_plan['data']} → {best['data']}")

        else:
            print("No lower plan to compare against.")
