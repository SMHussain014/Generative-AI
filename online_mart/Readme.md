Designing an Online Mart with six microservices involves carefully defining each service, their responsibilities, and how they will interact with each other. Here's a high-level overview of the architecture, including the use of Kafka for messaging and a database for persistent storage.

### Microservices Overview

1. **Products Service**: Manages product listings, including creation, updates, and deletions.
2. **Orders Service**: Handles order creation, status updates, and order history.
3. **Payments Service**: Manages payment processing and transactions.
4. **Inventory Service**: Keeps track of stock levels, updates inventory on order placement, and manages stock replenishments.
5. **Notifications Service**: Sends notifications to users about order status, payment confirmations, and other events.
6. **Users Service**: Manages user information, authentication, and authorization.

### Interconnectivity and Data Flow

Each microservice will communicate with others either directly through REST APIs or indirectly via Kafka for asynchronous messaging. Here is how they connect:

1. **Products Service**:
   - REST API: CRUD operations on products.
   - Kafka: Publishes events for product updates (e.g., price change, new product).

2. **Orders Service**:
   - REST API: Order creation, updates, and queries.
   - Kafka: Consumes product updates for real-time pricing and availability, publishes order events (e.g., order created, order shipped).

3. **Payments Service**:
   - REST API: Payment processing endpoints.
   - Kafka: Consumes order creation events, publishes payment status events (e.g., payment successful, payment failed).

4. **Inventory Service**:
   - REST API: Inventory queries and updates.
   - Kafka: Consumes order events to update inventory, publishes inventory updates.

5. **Notifications Service**:
   - REST API: Notification management (optional).
   - Kafka: Consumes events from orders, payments, and inventory to send notifications.

6. **Users Service**:
   - REST API: User registration, authentication, profile management.
   - Kafka: Publishes user-related events (e.g., new user registration).

### Kafka Topics

- **ProductEvents**: Published by Products Service (e.g., product created, updated, deleted).
- **OrderEvents**: Published by Orders Service (e.g., order created, order updated).
- **PaymentEvents**: Published by Payments Service (e.g., payment successful, payment failed).
- **InventoryEvents**: Published by Inventory Service (e.g., stock level changed).
- **NotificationEvents**: Published by various services for notifications.
- **UserEvents**: Published by Users Service (e.g., user registered).

### Database Design

Each microservice will have its own database to maintain loose coupling and separation of concerns. Common databases used in microservices architecture include relational databases like MySQL or PostgreSQL and NoSQL databases like MongoDB or Cassandra. 

- **Products DB**: Stores product details (product ID, name, description, price, stock status).
- **Orders DB**: Stores order details (order ID, user ID, product IDs, order status, total amount).
- **Payments DB**: Stores payment transactions (payment ID, order ID, user ID, payment status, amount).
- **Inventory DB**: Stores inventory data (product ID, quantity available).
- **Notifications DB**: Stores notification logs (notification ID, user ID, message, status).
- **Users DB**: Stores user details (user ID, username, password, email, address).

### Inter-Service Communication Example

1. **Order Creation Flow**:
   - User Service authenticates the user and sends a request to Orders Service.
   - Orders Service creates an order and publishes an `OrderCreated` event to Kafka.
   - Inventory Service consumes the `OrderCreated` event, updates stock levels, and publishes an `InventoryUpdated` event.
   - Payments Service consumes the `OrderCreated` event and processes the payment, then publishes a `PaymentSuccessful` event.
   - Notifications Service consumes the `OrderCreated`, `InventoryUpdated`, and `PaymentSuccessful` events and sends appropriate notifications to the user.

### Technologies

- **Microservices Framework**: Spring Boot, Node.js, or similar.
- **Database**: MySQL, PostgreSQL, MongoDB, etc.
- **Message Broker**: Apache Kafka.
- **API Gateway**: For routing requests to appropriate microservices.
- **Authentication/Authorization**: JWT, OAuth 2.0.
- **Containerization**: Docker, Kubernetes for orchestration.
- **Monitoring and Logging**: Prometheus, Grafana, ELK Stack.

### Diagram

Below is a simplified representation of the architecture:

```
                   +------------+
                   |  API       |
                   |  Gateway   |
                   +------------+
                         |
       +---------+--------+---------+---------+--------+---------+
       |         |        |         |         |        |         |
+------+------+ +----+ +-------+ +-------+ +----+ +--------+ +-------+
| Products   | |Orders| |Payments| |Inventory| |Users| |Notifications|
|  Service   | |Service| |Service | |Service  | |Service| |Service     |
+------------+ +----+ +-------+ +-------+ +----+ +--------+ +-------+
                         |
                 +---------------+
                 |     Kafka     |
                 +---------------+
                         |
  +--------+-----------+--------+---------+--------+--------+--------+
  |ProductEvents|OrderEvents|PaymentEvents|InventoryEvents|NotificationEvents|UserEvents|
  +--------+-----------+--------+---------+--------+--------+--------+
                         |
        +---------+--------+---------+---------+--------+---------+
        |         |        |         |         |        |         |
+--------+ +--------+ +--------+ +--------+ +--------+ +--------+
|ProductDB| |OrderDB| |PaymentDB| |InventoryDB| |UsersDB| |NotificationDB|
+--------+ +--------+ +--------+ +--------+ +--------+ +--------+
```

This architecture ensures a decoupled, scalable, and maintainable system where each service can evolve independently.



Sure, here is the complete code for all six microservices using FastAPI, SQLModel, Kafka, and Protobuf.

### Step 1: Protobuf Definitions
First, create a `protos` directory and define the Protobuf message format.

**protos/messages.proto**:
```proto
syntax = "proto3";

message Product {
  int32 id = 1;
  string name = 2;
  float price = 3;
  int32 stock = 4;
}

message Order {
  int32 id = 1;
  int32 user_id = 2;
  int32 product_id = 3;
  int32 quantity = 4;
  string status = 5;
}

message Payment {
  int32 id = 1;
  int32 order_id = 2;
  float amount = 3;
  string status = 4;
}

message User {
  int32 id = 1;
  string username = 2;
  string email = 3;
}
```

### Step 2: Services Implementation
Here's the implementation of each service with separate Kafka producers and consumers, using FastAPI and SQLModel.

### Products Service
### Orders Service
**orders_service.py**:
```python
from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, create_engine, Session, select
from kafka import KafkaProducer, KafkaConsumer
import messages_pb2
import threading

app = FastAPI()
DATABASE_URL = "sqlite:///orders.db"
engine = create_engine(DATABASE_URL)

class Order(SQLModel, table=True):
    id: int
    user_id: int
    product_id: int
    quantity: int
    status: str = "pending"

SQLModel.metadata.create_all(engine)

def get_kafka_producer():
    return KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: x.SerializeToString()
    )

producer = get_kafka_producer()

@app.post("/orders/")
def create_order(order: Order):
    with Session(engine) as session:
        session.add(order)
        session.commit()
        session.refresh(order)
    order_event = messages_pb2.Order(
        id=order.id, user_id=order.user_id, product_id=order.product_id, quantity=order.quantity, status=order.status
    )
    producer.send('OrderEvents', order_event)
    return order

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    with Session(engine) as session:
        order = session.exec(select(Order).where(Order.id == order_id)).first()
        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

def consume_product_events():
    consumer = KafkaConsumer(
        'ProductEvents',
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda x: messages_pb2.Product().ParseFromString(x)
    )
    for message in consumer:
        product_event = message.value
        print(f"Received Product event: {product_event}")

if __name__ == "__main__":
    threading.Thread(target=consume_product_events).start()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
```

### Payments Service
**payments_service.py**:
```python
from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, create_engine, Session, select
from kafka import KafkaProducer, KafkaConsumer
import messages_pb2
import threading

app = FastAPI()
DATABASE_URL = "sqlite:///payments.db"
engine = create_engine(DATABASE_URL)

class Payment(SQLModel, table=True):
    id: int
    order_id: int
    amount: float
    status: str = "completed"

SQLModel.metadata.create_all(engine)

def get_kafka_producer():
    return KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: x.SerializeToString()
    )

producer = get_kafka_producer()

@app.post("/payments/")
def process_payment(payment: Payment):
    with Session(engine) as session:
        session.add(payment)
        session.commit()
        session.refresh(payment)
    payment_event = messages_pb2.Payment(
        id=payment.id, order_id=payment.order_id, amount=payment.amount, status=payment.status
    )
    producer.send('PaymentEvents', payment_event)
    return payment

@app.get("/payments/{payment_id}")
def get_payment(payment_id: int):
    with Session(engine) as session:
        payment = session.exec(select(Payment).where(Payment.id == payment_id)).first()
        if payment is None:
            raise HTTPException(status_code=404, detail="Payment not found")
        return payment

def consume_order_events():
    consumer = KafkaConsumer(
        'OrderEvents',
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda x: messages_pb2.Order().ParseFromString(x)
    )
    for message in consumer:
        order_event = message.value
        print(f"Received Order event: {order_event}")

if __name__ == "__main__":
    threading.Thread(target=consume_order_events).start()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
```

### Inventory Service
**inventory_service.py**:
```python
from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, create_engine, Session, select
from kafka import KafkaProducer, KafkaConsumer
import messages_pb2
import threading

app = FastAPI()
DATABASE_URL = "sqlite:///inventory.db"
engine = create_engine(DATABASE_URL)

class Inventory(SQLModel, table=True):
    id: int
    product_id: int
    quantity: int

SQLModel.metadata.create_all(engine)

def get_kafka_producer():
    return KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: x.SerializeToString()
    )

producer = get_kafka_producer()

@app.get("/inventory/{product_id}")
def get_inventory(product_id: int):
    with Session(engine) as session:
        inventory = session.exec(select(Inventory).where(Inventory.product_id == product_id)).first()
        if inventory is None:
            raise HTTPException(status_code=404, detail="Product not found in inventory")
        return inventory

def consume_order_events():
    consumer = KafkaConsumer(
        'OrderEvents',
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda x: messages_pb2.Order().ParseFromString(x)
    )
    for message in consumer:
        order_event = message.value
        print(f"Received Order event: {order_event}")
        with Session(engine) as session:
            inventory = session.exec(select(Inventory).where(Inventory.product_id == order_event.product_id)).first()
            if inventory and inventory.quantity >= order_event.quantity:
                inventory.quantity -= order_event.quantity
                session.add(inventory)
                session.commit()
                inventory_event = messages_pb2.Inventory(
                    id=inventory.id, product_id=inventory.product_id, quantity=inventory.quantity
                )
                producer.send('InventoryEvents', inventory_event)
            else:
                print('Not enough inventory!')

if __name__ == "__main__":
    threading.Thread(target=consume_order_events).start()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
```

### Notifications Service
**notifications_service.py**:
```python
from fastapi import FastAPI
from kafka import KafkaConsumer
import messages_pb2
import threading

app = FastAPI()

def send_notification(message):
    print(f"Sending notification: {message}")

def consume_order_events():
    consumer = KafkaConsumer(
        'OrderEvents',
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda x: messages_pb2.Order().ParseFromString(x)
    )
    for message in consumer:
        order_event = message.value
        send_notification(f"Order created: {order_event.id}")

def consume_payment_events