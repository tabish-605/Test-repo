
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import List
import os

# OpenTelemetry imports
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db:5432/postgres")

engine = create_engine(DATABASE_URL, echo=True)

class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    image: str | None = None

class CartItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str
    product_id: int
    quantity: int = 1

class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str
    total: float

def init_db():
    SQLModel.metadata.create_all(engine)

# OpenTelemetry setup
resource = Resource(attributes={SERVICE_NAME: "fastapi-backend"})
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector:4318", insecure=True))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

app = FastAPI()

FastAPIInstrumentor.instrument_app(app)
SQLAlchemyInstrumentor().instrument(engine=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_session():
    with Session(engine) as session:
        yield session

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/products", response_model=List[Product])
def list_products(session: Session = Depends(get_session)):
    return session.exec(select(Product)).all()

@app.post("/products", response_model=Product)
def create_product(product: Product, session: Session = Depends(get_session)):
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@app.get("/cart/{user_id}")
def get_cart(user_id: str, session: Session = Depends(get_session)):
    items = session.exec(select(CartItem).where(CartItem.user_id == user_id)).all()
    return items

@app.post("/cart/{user_id}")
def add_to_cart(user_id: str, item: CartItem, session: Session = Depends(get_session)):
    item.user_id = user_id
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@app.post("/orders/{user_id}")
def create_order(user_id: str, session: Session = Depends(get_session)):
    items = session.exec(select(CartItem).where(CartItem.user_id == user_id)).all()
    if not items:
        raise HTTPException(status_code=400, detail="Cart empty")
    total = sum(i.quantity * session.get(Product, i.product_id).price for i in items)
    order = Order(user_id=user_id, total=total)
    session.add(order)
    session.exec(select(CartItem).where(CartItem.user_id == user_id)).delete()
    session.commit()
    return {"order_id": order.id, "total": total}
