# Take distance (km), weather (clear/rain/storm),
# and time of day (peak/normal) as input.
# Calculate estimated delivery time. 
# show a status message like Zomato does. 


distance = float(input("Distance (km): "))
weather = input("Weather (clear/rain/storm): ").lower()
time_of_day = input("Time (peak/normal): ").lower()

estimated_time = distance * 8

if weather == "rain":
    estimated_time += 6
    status = "Running slightly late due to rain"

elif weather == "storm":
    estimated_time += 15
    status = "Delivery delayed due to severe weather conditions"

else:
    status = "On time"

if time_of_day == "peak":
    estimated_time += 10

    if weather == "clear":
        status = "High demand in your area. Delivery may take longer."
        
print("\n---")
print(f"Estimated delivery: {estimated_time:.0f} mins")
print(f'Status: "{status}"')