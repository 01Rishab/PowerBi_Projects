from fastapi import FastAPI
import random
from datetime import datetime, timedelta

app = FastAPI(title="Logistics Ops API")

REGIONS = ["North", "South", "East", "West"]
STATUSES = ["Pending", "Shipped", "Delayed", "Delivered"]

def generate_order(order_id: int):
    order_date = datetime.now() - timedelta(days=random.randint(1, 30))
    expected_delivery = order_date + timedelta(days=random.randint(2, 7))
    status = random.choice(STATUSES)
    actual_delivery = None
    if status == "Delivered":
        actual_delivery = expected_delivery + timedelta(days=random.choice([-1, 0, 0, 1, 2, 3]))

    return {
        "order_id": order_id,
        "region": random.choice(REGIONS),
        "status": status,
        "order_date": order_date.strftime("%Y-%m-%d"),
        "expected_delivery": expected_delivery.strftime("%Y-%m-%d"),
        "actual_delivery": actual_delivery.strftime("%Y-%m-%d") if actual_delivery else None,
    }

# In-memory dataset, generated once at startup
orders_db = [generate_order(i) for i in range(1, 501)]

@app.get("/orders")
def get_orders():
    return orders_db

@app.get("/refresh")
def refresh_orders():
    """Simulates new activity by regenerating a batch of orders."""
    global orders_db
    orders_db = [generate_order(i) for i in range(1, 501)]
    return {"message": "Orders refreshed", "count": len(orders_db)}