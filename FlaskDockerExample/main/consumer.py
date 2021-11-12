import pika, json
from main import Product, db
params = pika.URLParameters('amqps://dowzsxzj:UT7_s888elZ3FCRdD1CjiHY9S9aQPI81@cow.rmq2.cloudamqp.com/dowzsxzj')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')

def callback(ch, method, properties, body):
    print('Receieved in admin')
    # print(body)
    data = json.loads(body)
    print(data)

    if properties.content_type == 'product_created':
        # create a n object with SQLAlchemy
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print("Product created")

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print("Product updated")

    elif properties.content_type == 'product_delelted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print("Product deleted")
        
channel.basic_consume(queue='main', on_message_callback=callback)

print('Started Consuming')

channel.start_consuming()

channel.close()