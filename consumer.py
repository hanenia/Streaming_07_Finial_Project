from collections import deque
import pika
import sys
from util_logger import setup_logger

logger, logname = setup_logger(__file__)

def callback(ch, method, properties, body):
    """Define behavior on getting a message."""
    flight_data = eval(body.decode())
    fight_number = flight_data[0]
    flight_from = flight_data[1]
    flight_to = flight_data[2]
    flight_status = flight_data[3]
    logger.info(f"Received flight data: {flight_data}")

    # Acknowledge the message was received and processed
    if flight_status != "On Time":
        logger.info(f" [alert] {fight_number} => FROM: {flight_from} - TO: {flight_to} => FLIGHT {flight_status}!!!")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    """Continuously listen for task messages on a named queue."""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    except Exception as e:
        logger.error(f"Connection to RabbitMQ server failed: {e}")
        sys.exit(1)

    try:
        channel = connection.channel()
        channel.queue_delete(queue='flights')
        channel.queue_declare(queue='flights', durable=True)

        # Limit the number of unacknowledged messages
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='flights', on_message_callback=callback, auto_ack=False)

        logger.info(" [*] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()
    except Exception as e:
        logger.error(f"Something went wrong: {e}")
    except KeyboardInterrupt:
        logger.info("User interrupted the process.")
    finally:
        connection.close()

if __name__ == '__main__':
    main()