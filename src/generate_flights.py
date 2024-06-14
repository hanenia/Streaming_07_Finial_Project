# import csv
# import random
# from faker import Faker

# # Create a Faker instance
# fake = Faker()
# Faker.seed(0)
# # Generate random flight data
# num_flights = 1000  # Specify the number of flights to generate

# # Specify the CSV file path
# csv_file_path = "flight_data.csv"

# # Open the CSV file in write mode
# with open(csv_file_path, mode="w", newline="") as file:
#     # Create a CSV writer
#     writer = csv.writer(file)

#     # Write the header row
#     writer.writerow([
#         "Airline", "Flight Number", "Origin Airport", "Destination Airport",
#         "Departure Time", "Arrival Time", "Aircraft Type", "Seat Number",
#          "Status"
#     ])

#     # Generate and write flight data to the CSV file
#     for _ in range(num_flights):
#         # Generate random flight status
#         status_options = ["On Time", "Delayed", "Cancelled"]
#         status_probabilities = [0.7, 0.15, 0.15]
#         status = random.choices(status_options, weights=status_probabilities)[0]

#         flight_data = [
#             fake.company(),  # Generate a random airline company name
#             fake.bothify(text='FL####', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),  # Generate a random flight number
#             fake.lexify(text='???').upper(),  # Generate a random origin airport code
#             fake.lexify(text='???').upper(),  # Generate a random destination airport code
#             fake.time(),  # Generate a random departure time
#             fake.time(),  # Generate a random arrival time
#             fake.random_element(elements=["regional", "narrowbody", "widebody"]),
#             fake.bothify(text='##?', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),  # Generate a random seat number
#             status
#         ]
#         writer.writerow(flight_data)

# print(f"Flight data has been written to {csv_file_path}")


import csv
from faker import Faker
from datetime import datetime, timedelta
import random

# Create a Faker instance
fake = Faker()

# Generate random flight data
num_flights = 1000  # Specify the number of flights to generate

# Specify the CSV file path
csv_file_path = "flight_data.csv"

# Specify the date range for flights
start_date = datetime(2023, 1, 1)  # Start date (year, month, day)
end_date = datetime(2023, 12, 31)  # End date (year, month, day)

# Open the CSV file in write mode
with open(csv_file_path, mode="w", newline="") as file:
    # Create a CSV writer
    writer = csv.writer(file)

    # Write the header row
    writer.writerow([
        "Flight Number", "Departure Date", "Departure Time", "Arrival Date", "Arrival Time",
        "Origin Airport", "Destination Airport", "Airline", "Status",
        "Passenger Name", "Passenger Email", "Baggage Tag Number", "Baggage Status"
    ])

    # Generate and write flight data to the CSV file
    for _ in range(num_flights):
        # Generate random flight status with 70% probability of being "On Time"
        status_options = ["On Time", "Delayed", "Cancelled"]
        status_probabilities = [0.7, 0.15, 0.15]
        status = random.choices(status_options, weights=status_probabilities)[0]

        # Generate random departure and arrival dates within the specified date range
        departure_date = fake.date_between_dates(date_start=start_date, date_end=end_date)
        arrival_date = fake.date_between_dates(date_start=departure_date, date_end=end_date)

        # Generate random departure and arrival times
        departure_time = fake.time(pattern="%H:%M")
        arrival_time = fake.time(pattern="%H:%M")

        # Generate random baggage status
        baggage_status_options = ["Checked-in", "Loaded", "Unloaded", "Delivered"]
        baggage_status = random.choice(baggage_status_options)

        flight_data = [
            fake.bothify(text='FL####', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),  # Generate a random flight number
            departure_date.strftime("%Y-%m-%d"),  # Format departure date as YYYY-MM-DD
            departure_time,
            arrival_date.strftime("%Y-%m-%d"),  # Format arrival date as YYYY-MM-DD
            arrival_time,
            fake.lexify(text='???').upper(),  # Generate a random origin airport code
            fake.lexify(text='???').upper(),  # Generate a random destination airport code
            fake.company(),  # Generate a random airline company name
            status,
            fake.name(),  # Generate a random passenger name
            fake.email(),  # Generate a random passenger email
            fake.bothify(text='BG####', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),  # Generate a random baggage tag number
            baggage_status
        ]
        writer.writerow(flight_data)

print(f"Flight data has been written to {csv_file_path}")