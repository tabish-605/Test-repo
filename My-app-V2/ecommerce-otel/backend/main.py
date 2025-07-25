import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource

# Initialize tracing
resource = Resource(attributes={
    "service.name": "ecommerce-backend"
})
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(
    endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT") + "/v1/traces"
))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

app = FastAPI()

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database models
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, index=True)
    description = Column(Text)
    price = Column(Float, nullable=False)
    category = Column(String(50))
    image = Column(String(200))
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    sizes = Column(String(100))

# Create tables (in production, use migrations instead)
Base.metadata.create_all(bind=engine)

# Sample data
def init_db():
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Product).count() == 0:
            products = [
                Product(
                    name="Wireless Bluetooth Headphones",
                    slug="wireless-bluetooth-headphones",
                    description="Premium noise-cancelling wireless headphones",
                    price=129.99,
                    category="electronics",
                    image="https://via.placeholder.com/300",
                    rating=4.5,
                    review_count=120,
                    sizes="One Size"
                ),
                Product(
                    name="Running Shoes",
                    slug="running-shoes",
                    description="Lightweight running shoes with extra cushioning",
                    price=89.99,
                    category="clothing",
                    image="https://via.placeholder.com/300",
                    rating=4.2,
                    review_count=85,
                    sizes="S,M,L,XL"
                ),
                Product(
                    name="Smart Watch",
                    slug="smart-watch",
                    description="Track your fitness and stay connected",
                    price=199.99,
                    category="electronics",
                    image="https://via.placeholder.com/300",
                    rating=4.7,
                    review_count=210,
                    sizes="One Size"
                ),
                Product(
                    name="Cotton T-Shirt",
                    slug="cotton-t-shirt",
                    description="Comfortable everyday t-shirt",
                    price=24.99,
                    category="clothing",
                    image="https://via.placeholder.com/300",
                    rating=4.0,
                    review_count=45,
                    sizes="S,M,L,XL"
                ),
                Product(
                    name="Desk Lamp",
                    slug="desk-lamp",
                    description="Adjustable LED desk lamp",
                    price=39.99,
                    category="home",
                    image="https://via.placeholder.com/300",
                    rating=4.3,
                    review_count=67,
                    sizes="One Size"
                )
            ]
            db.add_all(products)
            db.commit()
    finally:
        db.close()

# Initialize sample data
init_db()

@app.get("/")
def read_root():
    return {"message": "E-commerce API is running"}

@app.get("/api/products")
def get_products():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("get-all-products"):
        db = SessionLocal()
        try:
            products = db.query(Product).all()
            return products
        finally:
            db.close()

@app.get("/api/products/{slug}")
def get_product(slug: str):
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("get-product-by-slug") as span:
        span.set_attribute("product.slug", slug)
        db = SessionLocal()
        try:
            product = db.query(Product).filter(Product.slug == slug).first()
            if product is None:
                raise HTTPException(status_code=404, detail="Product not found")
            return product
        finally:
            db.close()

@app.post("/api/cart")
def add_to_cart(item: dict):
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("add-to-cart"):
        # In a real application, this would update the database
        # For this demo, we'll just log and return success
        return {"status": "success", "message": "Item added to cart"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
