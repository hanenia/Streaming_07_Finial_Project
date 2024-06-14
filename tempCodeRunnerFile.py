import pika
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def callback(ch, method, properties, body):
    """Define behavior on getting a message."""
    flight_data = body.decode()
    logger.info(f"Received flight data: {flight_data}")

    # Acknowledge the message was received and processed
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    """Continuously listen for task messages on a named queue."""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    except Exception as e:
        logger.error(f"Connection to RabbitMQ server failed: {e}")
        return

    try:
        channel = connection.channel()
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