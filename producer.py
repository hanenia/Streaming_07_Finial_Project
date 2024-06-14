import csv
import time
import pika, sys, webbrowser
from faker import Faker
from util_logger import setup_logger
logger, logname = setup_logger(__file__)

def offer_rabbitmq_admin_site():
    """Offer to open the RabbitMQ Admin website"""
    ans = input("Would you like to monitor RabbitMQ queues? y or n ")
    print()

    if ans.lower() == "y":
        webbrowser.open_new("http://localhost:15672/#/queues")
        print()

def send_message(channel, queue_name: str, message: tuple):
    try:
        # use the channel to publish a message to the queue
        # every message passes through an exchange
        channel.basic_publish(exchange="", routing_key=queue_name, body=str(message))
        # print a message to the console for the user
        logger.info(f" [x] Sent message to {queue_name} : {message}")
    except pika.exceptions.AMQPConnectionError as e:
        #print(f"Error: Connection to RabbitMQ server failed: {e}")
        logger.info(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)

def produce():
    # faker = Faker()
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declare a durable queue
        channel.queue_delete(queue='flights')
        channel.queue_delete(queue='flight-baggage')
        channel.queue_declare(queue='flights', durable=True)
        channel.queue_declare(queue='flight-baggage', durable=True)

        with open('flight_data.csv', 'r') as file:
            reader = csv.reader(file)
            # Remove the header row
            header = next(reader)
            # for each row in csv declare variable
            for data_row in reader:
                flight_number = data_row[0]
                flight_from = data_row[5]
                flight_to = data_row[6]
                flight_status = data_row[8]
                passenger_name = data_row[9]
                baggage_number = data_row[11]
                baggage_status = data_row[12]
                if flight_status:
                    flight_data = (flight_number, flight_from, flight_to ,flight_status)
                    # Send the message to the queue
                    send_message(channel, 'flights', flight_data)
                if baggage_status:
                    baggage_data = (passenger_name, baggage_number, baggage_status)
                    send_message(channel, 'flight-baggage', baggage_data)

                time.sleep(2)

        # airlines = ['AA', 'DL', 'UA', 'SW', 'BA']

        # for _ in range(10):
        #     flight_data = {
        #         'flight_number': f"{faker.random_element(elements=airlines)}{faker.random_int(min=100, max=9999)}",
        #         'timestamp': faker.date_time_this_year().isoformat(),
        #         'origin': faker.city(),
        #         'destination': faker.city(),
        #         "status": faker.random_element(elements=['on-time', 'delayed', 'cancelled'])
        #     }
            # channel.basic_publish(
            #     exchange='',
            #     routing_key='flights',
            #     body=str(flight_data),
            #     properties=pika.BasicProperties(delivery_mode=2)  # make message persistent
            # )
            # print(f"Sent {flight_data}")
            # send_message(channel, 'flights', flight_data)
            # time.sleep(2)
    
    except pika.exceptions.AMQPConnectionError as e:
        logger.info(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    finally:
        # close the connection to the server
        connection.close()

if __name__ == '__main__':
    show_offer = True
    if show_offer is True:
        offer_rabbitmq_admin_site()
    produce()