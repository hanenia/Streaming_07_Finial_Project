from collections import deque
import pika
import sys
from util_logger import setup_logger

logger, logname = setup_logger(__file__)

def callback(ch, method, properties, body):
    """Define behavior on getting a message."""
    baggage_data = eval(body.decode())
    passenger_name = baggage_data[0]
    baggage_number = baggage_data[1]
    baggage_status = baggage_data[2]
    logger.info(f"Received baggage data: {baggage_data}")

    # Acknowledge the message was received and processed
    if baggage_status == "Delivered":
        logger.info(f" [alert] {baggage_number} => BAGGAGE FOR: {passenger_name} is {baggage_status}!!!")
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
        channel.queue_delete(queue='flight-baggage')
        channel.queue_declare(queue='flight-baggage', durable=True)

        # Limit the number of unacknowledged messages
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='flight-baggage', on_message_callback=callback, auto_ack=False)

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