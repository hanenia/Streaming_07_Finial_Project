import csv
from faker import Faker

def generate_flight_data(file_path, num_records=100):
    fake = Faker()
    airlines = ['AA', 'DL', 'UA', 'SW', 'BA']
    
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['flight_number', 'timestamp', 'origin', 'destination']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for _ in range(num_records):
            airline_code = fake.random_element(airlines)
            flight_number = f"{airline_code}{fake.random_int(min=100, max=9999)}"
            writer.writerow({
                'flight_number': flight_number,
                'timestamp': fake.date_time_this_year().isoformat(),
                'origin': fake.city(),
                'destination': fake.city()
            })

if __name__ == "__main__":
    generate_flight_data('data/flight_data.csv', num_records=1000)

