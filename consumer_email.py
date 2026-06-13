import pika
import json
import time
from models import Contact

CLOUDAMQP_URL = "amqps://pgmpbrse:iHll_miGHbybFUcYQLRM626x44mj0En0@collie.lmq.cloudamqp.com/pgmpbrse"

def callback(ch, method, properties, body):
    data = json.loads(body)
    contact_id = data.get('contact_id')
    contact = Contact.objects(id=contact_id).first()

    if contact:
        print(f" Надійшло завдання: Надіслати EMAIL для {contact.fullname} ({contact.email})")
        time.sleep(1)  # Імітація відправки листа
        contact.update(set__is_sent=True)
        print(f"✨ EMAIL успішно надіслано для {contact.fullname}. Статус в базі: True")
    else:
        print(f"❌ Контакт з ID {contact_id} не знайдено.")

    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    params = pika.URLParameters(CLOUDAMQP_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='email_queue')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='email_queue', on_message_callback=callback)

    print('🚀 Консумер EMAIL запущений і чекає на повідомлення...')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n Зупинка консумера EMAIL...')