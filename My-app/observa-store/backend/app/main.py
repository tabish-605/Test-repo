# backend/app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import trace
from .instrumentation import setup_tracing
from .db import get_db_connection
import random
import time

app = FastAPI()

# Setup OpenTelemetry Tracing
setup_tracing(app)

# CORS configuration to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tracer = trace.get_tracer(__name__)

@app.get("/api/products")
def get_products():
    with tracer.start_as_current_span("get_all_products") as span:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, price FROM products;")
        products = cur.fetchall()
        cur.close()
        conn.close()
        span.set_attribute("products.count", len(products))
    return {"products": products}

@app.post("/api/cart/add")
def add_to_cart(item: dict):
    product_id = item.get("product_id")
    quantity = item.get("quantity")

    with tracer.start_as_current_span("add_to_cart") as span:
        span.set_attribute("product.id", product_id)
        span.set_attribute("product.quantity", quantity)

        # Simulate inventory check
        with tracer.start_as_current_span("check_inventory") as inventory_span:
            time.sleep(random.uniform(0.05, 0.1))
            inventory_span.set_attribute("inventory.status", "in_stock")

        # Simulate adding to cart database
        time.sleep(random.uniform(0.1, 0.2))

    return {"status": "success", "message": f"Added {quantity} of product {product_id} to cart."}

@app.post("/api/checkout")
def checkout(order: dict):
    with tracer.start_as_current_span("checkout_process") as span:
        items = order.get("items", [])
        span.set_attribute("order.item_count", len(items))

        # Simulate payment processing
        with tracer.start_as_current_span("payment_gateway") as payment_span:
            time.sleep(random.uniform(0.2, 0.5))
            if random.random() < 0.1: # 10% chance of failure
                payment_span.set_status(trace.Status(trace.StatusCode.ERROR, "Payment failed"))
                raise HTTPException(status_code=500, detail="Payment processing failed")
            payment_span.set_attribute("payment.status", "approved")

        # Simulate order creation in DB
        time.sleep(random.uniform(0.1, 0.3))

    return {"status": "success", "order_id": random.randint(1000, 9999)}
