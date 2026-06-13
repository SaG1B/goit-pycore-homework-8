import pika
import json
from faker import Faker
from models import Contact

fake = Faker()

# Твоє хмарне підключення до CloudAMQP
CLOUDAMQP_URL = "amqps://pgmpbrse:iHll_miGHbybFUcYQLRM626x44mj0En0@collie.lmq.cloudamqp.com/pgmpbrse"

def main():
    # Підключаємося до хмарного RabbitMQ
    params = pika.URLParameters(CLOUDAMQP_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # Оголошуємо дві черги
    channel.queue_declare(queue='email_queue')
    channel.queue_declare(queue='sms_queue')

    print("🤖 Producer готовий до генерації контактів...")

    # Генеруємо 10 випадкових контактів
    for _ in range(10):
        method = fake.random_element(elements=('email', 'sms'))
        
        contact = Contact(
            fullname=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            preferred_method=method
        )
        contact.save()  # Зберігаємо в MongoDB Atlas

        message = {'contact_id': str(contact.id)}

        # Розподіляємо по чергах RabbitMQ
        if method == 'email':
            channel.basic_publish(exchange='', routing_key='email_queue', body=json.dumps(message))
            print(f"📧 Відправлено в чергу EMAIL: {contact.fullname}")
        else:
            channel.basic_publish(exchange='', routing_key='sms_queue', body=json.dumps(message))
            print(f"📱 Відправлено в чергу SMS: {contact.fullname}")

    connection.close()
    print("✅ Усі контакти згенеровано та успішно розподілено!")

if __name__ == '__main__':
    main()