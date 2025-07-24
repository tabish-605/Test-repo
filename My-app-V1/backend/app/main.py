from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import select
from random import random
from .db import init_db, get_session, engine
from .models import Product
from .instrumentation import setup_tracing
from sqlmodel import Session

app = FastAPI()
setup_tracing(app, engine)

@app.on_event('startup')
def on_startup():
    init_db()
    # seed demo data
    with Session(engine) as s:
        if not s.exec(select(Product)).first():
            s.add_all([
                Product(name='OTel T-Shirt', price=25.0, description='Comfy cotton tee'),
                Product(name='K8s Beanie', price=15.5, description='Stay warm while kubing'),
                Product(name='Docker Mug', price=12.0, description='Sip while you ship'),
            ])
            s.commit()

@app.get('/api/products')
def get_products(session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    return {"products": products}

@app.post('/api/cart/add')
def add_to_cart(item: dict):
    return {"status": "ok"}

@app.post('/api/checkout')
async def checkout(simulate_failure: bool = False):
    if random() < 0.1 or simulate_failure:
        raise HTTPException(status_code=500, detail="Payment failed (simulated)")
    return {"status": "success"}
