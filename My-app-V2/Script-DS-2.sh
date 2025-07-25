#!/bin/bash

# Create project structure
mkdir -p ecommerce-otel/{frontend,backend,collector,prometheus,grafana/provisioning/datasources}

# Frontend structure
mkdir -p ecommerce-otel/frontend/{components,lib,pages,public/images,styles}
mkdir -p ecommerce-otel/frontend/components/{layout,product,cart,checkout,search,ui}
mkdir -p ecommerce-otel/frontend/pages/{products,account,auth}

# Backend structure
mkdir -p ecommerce-otel/backend/routers

# Create Docker Compose file
cat > ecommerce-otel/docker-compose.yml <<'EOL'
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
    depends_on:
      - backend
      - otel-collector

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/ecommerce
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
    depends_on:
      - postgres
      - otel-collector

  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: ecommerce
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres-data:/var/lib/postgresql/data

  otel-collector:
    image: otel/opentelemetry-collector-contrib:0.60.0
    command: ["--config=/etc/otel-collector-config.yaml"]
    volumes:
      - ./collector/otel-collector-config.yaml:/etc/otel-collector-config.yaml
    ports:
      - "4317:4317"   # OTLP gRPC
      - "8889:8889"   # Prometheus metrics

  jaeger:
    image: jaegertracing/all-in-one:1.40
    ports:
      - "16686:16686"

  prometheus:
    image: prom/prometheus:v2.36.0
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana:9.0.2
    volumes:
      - ./grafana/provisioning:/etc/grafana/provisioning
    ports:
      - "3001:3000"
    environment:
      - GF_AUTH_ANONYMOUS_ENABLED=true
      - GF_AUTH_ANONYMOUS_ORG_ROLE=Admin

volumes:
  postgres-data:
EOL

# Create OTel Collector config
cat > ecommerce-otel/collector/otel-collector-config.yaml <<'EOL'
receivers:
  otlp:
    protocols:
      grpc:
      http:

exporters:
  jaeger:
    endpoint: "jaeger:14250"
    tls:
      insecure: true
  prometheus:
    endpoint: "0.0.0.0:8889"
    namespace: ecommerce
  logging:
    loglevel: debug

processors:
  batch:

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [jaeger, logging]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus, logging]
EOL

# Create Prometheus config
cat > ecommerce-otel/prometheus/prometheus.yml <<'EOL'
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'otel-collector'
    scrape_interval: 5s
    static_configs:
      - targets: ['otel-collector:8889']
EOL

# Create Grafana datasource config
mkdir -p ecommerce-otel/grafana/provisioning/datasources
cat > ecommerce-otel/grafana/provisioning/datasources/datasource.yml <<'EOL'
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
EOL

# =============================
# FRONTEND FILES (ESCAPED SYNTAX)
# =============================

# Create Next.js config
cat > ecommerce-otel/frontend/next.config.js <<'EOL'
/** @type {import('next').NextConfig} */
module.exports = {
  reactStrictMode: true,
  images: {
    domains: ['via.placeholder.com'],
  },
  experimental: {
    instrumentationHook: true,
  },
}
EOL

# Create package.json
cat > ecommerce-otel/frontend/package.json <<'EOL'
{
  "name": "ecommerce-frontend",
  "version": "1.0.0",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "@opentelemetry/api": "^1.4.1",
    "@opentelemetry/auto-instrumentations-node": "^0.39.4",
    "@opentelemetry/exporter-trace-otlp-http": "^0.45.0",
    "@opentelemetry/sdk-node": "^0.45.0",
    "next": "13.4.12",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "react-icons": "^4.10.1"
  },
  "devDependencies": {
    "autoprefixer": "^10.4.14",
    "postcss": "^8.4.27",
    "tailwindcss": "^3.3.3"
  }
}
EOL

# Create Tailwind config
cat > ecommerce-otel/frontend/styles/tailwind.config.js <<'EOL'
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          600: '#4f46e5',
          700: '#4338ca',
        },
      },
    },
  },
  plugins: [],
}
EOL

# Create global CSS
cat > ecommerce-otel/frontend/styles/globals.css <<'EOL'
@tailwind base;
@tailwind components;
@tailwind utilities;

html,
body {
  padding: 0;
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen,
    Ubuntu, Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif;
}

* {
  box-sizing: border-box;
}
EOL

# Create tracing setup
cat > ecommerce-otel/frontend/lib/tracing.js <<'EOL'
const opentelemetry = require('@opentelemetry/sdk-node');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');

const sdk = new opentelemetry.NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT + '/v1/traces'
  }),
  instrumentations: [getNodeAutoInstrumentations()],
  serviceName: 'ecommerce-frontend'
});

sdk.start();
EOL

# Create API helper
cat > ecommerce-otel/frontend/lib/api.js <<'EOL'
export const fetchProducts = async () => {
  const response = await fetch('/api/products');
  return await response.json();
};

export const fetchProduct = async (slug) => {
  const response = await fetch(`/api/products/${slug}`);
  return await response.json();
};

export const addToCart = async (item) => {
  const response = await fetch('/api/cart', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(item)
  });
  return await response.json();
};
EOL

# Create cart context
cat > ecommerce-otel/frontend/lib/cart.js <<'EOL'
import { createContext, useState, useEffect, useContext } from 'react';

const CartContext = createContext();

export function CartProvider({ children }) {
  const [cart, setCart] = useState([]);
  const [isCartOpen, setIsCartOpen] = useState(false);

  useEffect(() => {
    const savedCart = localStorage.getItem('cart');
    if (savedCart) {
      setCart(JSON.parse(savedCart));
    }
  }, []);

  useEffect(() => {
    localStorage.setItem('cart', JSON.stringify(cart));
  }, [cart]);

  const addToCart = (product) => {
    const existingItem = cart.find(item => 
      item.id === product.id && item.size === product.size
    );

    if (existingItem) {
      setCart(cart.map(item => 
        item.id === product.id && item.size === product.size
          ? { ...item, quantity: item.quantity + product.quantity }
          : item
      ));
    } else {
      setCart([...cart, product]);
    }
    setIsCartOpen(true);
  };

  const removeItem = (id, size) => {
    setCart(cart.filter(item => !(item.id === id && item.size === size)));
  };

  const updateQuantity = (id, size, quantity) => {
    if (quantity < 1) return;
    setCart(cart.map(item => 
      item.id === id && item.size === size
        ? { ...item, quantity }
        : item
    ));
  };

  const cartCount = cart.reduce((total, item) => total + item.quantity, 0);
  const cartTotal = cart.reduce((total, item) => total + (item.price * item.quantity), 0);

  return (
    <CartContext.Provider 
      value={{ 
        cart, 
        cartCount, 
        cartTotal, 
        isCartOpen, 
        setIsCartOpen,
        addToCart, 
        removeItem, 
        updateQuantity,
        clearCart: () => setCart([])
      }}
    >
      {children}
    </CartContext.Provider>
  );
}

export const useCart = () => useContext(CartContext);
EOL

# Create layout components
cat > ecommerce-otel/frontend/components/layout/Header.js <<'EOL'
import { useState } from 'react';
import Link from 'next/link';
import { useCart } from '../../lib/cart';
import CartIcon from './CartIcon';
import SearchBar from '../search/SearchBar';

const Header = () => {
  const { setIsCartOpen, cartCount } = useCart();
  
  return (
    <header className="bg-white shadow-md sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center">
          <Link href="/">
            <a className="text-2xl font-bold text-indigo-700">ShopNext</a>
          </Link>
        </div>

        <div className="hidden md:block flex-grow mx-8">
          <SearchBar />
        </div>

        <nav className="hidden md:flex space-x-6">
          <Link href="/products"><a className="text-gray-700 hover:text-indigo-600">Shop</a></Link>
          <Link href="/account/wishlist"><a className="text-gray-700 hover:text-indigo-600">Wishlist</a></Link>
          <Link href="/account/orders"><a className="text-gray-700 hover:text-indigo-600">Orders</a></Link>
        </nav>

        <div className="flex items-center space-x-4">
          <Link href="/auth/login">
            <a className="text-gray-700 hover:text-indigo-600">Sign In</a>
          </Link>
          <button onClick={() => setIsCartOpen(true)}>
            <CartIcon count={cartCount} />
          </button>
        </div>
      </div>
      
      <div className="md:hidden px-4 pb-4">
        <SearchBar />
      </div>
    </header>
  );
};

export default Header;
EOL

cat > ecommerce-otel/frontend/components/layout/CartIcon.js <<'EOL'
import React from 'react';
import { FiShoppingCart } from 'react-icons/fi';

const CartIcon = ({ count = 0 }) => {
  return (
    <div className="relative">
      <FiShoppingCart className="text-2xl text-gray-700" />
      {count > 0 && (
        <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
          {count}
        </span>
      )}
    </div>
  );
};

export default CartIcon;
EOL

cat > ecommerce-otel/frontend/components/layout/Footer.js <<'EOL'
import Link from 'next/link';

const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white py-12">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-xl font-bold mb-4">ShopNext</h3>
            <p className="text-gray-400">
              Your one-stop shop for all your needs. Quality products at affordable prices.
            </p>
          </div>
          
          <div>
            <h4 className="text-lg font-semibold mb-4">Shop</h4>
            <ul className="space-y-2 text-gray-400">
              <li><Link href="/products"><a className="hover:text-white">All Products</a></Link></li>
              <li><Link href="/products?category=electronics"><a className="hover:text-white">Electronics</a></Link></li>
              <li><Link href="/products?category=clothing"><a className="hover:text-white">Clothing</a></Link></li>
              <li><Link href="/products?category=home"><a className="hover:text-white">Home & Garden</a></Link></li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-lg font-semibold mb-4">Customer Service</h4>
            <ul className="space-y-2 text-gray-400">
              <li><Link href="/contact"><a className="hover:text-white">Contact Us</a></Link></li>
              <li><Link href="/faq"><a className="hover:text-white">FAQs</a></Link></li>
              <li><Link href="/shipping"><a className="hover:text-white">Shipping Policy</a></Link></li>
              <li><Link href="/returns"><a className="hover:text-white">Returns & Exchanges</a></Link></li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-lg font-semibold mb-4">Stay Connected</h4>
            <p className="text-gray-400 mb-4">
              Subscribe to our newsletter for the latest updates and offers.
            </p>
            <div className="flex">
              <input 
                type="email" 
                placeholder="Your email" 
                className="px-4 py-2 rounded-l-md w-full text-gray-800"
              />
              <button className="bg-indigo-600 px-4 py-2 rounded-r-md">
                Subscribe
              </button>
            </div>
          </div>
        </div>
        
        <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
          <p>© 2023 ShopNext. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
EOL

# Create product components (ESCAPED SYNTAX)
cat > ecommerce-otel/frontend/components/product/ProductCard.js <<'EOL'
import Link from 'next/link';
import RatingStars from '../ui/RatingStars';
import { useCart } from '../../lib/cart';

const ProductCard = ({ product }) => {
  const { addToCart } = useCart();
  
  const handleAddToCart = (e) => {
    e.preventDefault();
    e.stopPropagation();
    addToCart({
      ...product,
      quantity: 1,
      size: product.sizes?.[0] || 'One Size'
    });
  };

  return (
    <Link href={`/products/${product.slug}`}>
      <a className="group block overflow-hidden transition-transform hover:scale-[1.02]">
        <div className="relative">
          <div className="aspect-square bg-gray-100 rounded-lg overflow-hidden">
            {product.image ? (
              <img 
                src={product.image} 
                alt={product.name} 
                className="w-full h-full object-cover transition-transform group-hover:scale-105"
              />
            ) : (
              <div className="w-full h-full bg-gray-200 border-2 border-dashed rounded-xl flex items-center justify-center text-gray-400">
                No Image
              </div>
            )}
          </div>
          
          <button 
            onClick={handleAddToCart}
            className="absolute bottom-4 right-4 bg-white rounded-full p-2 shadow-md opacity-0 group-hover:opacity-100 transition-opacity"
            aria-label="Add to cart"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M3 1a1 1 0 000 2h1.22l.305 1.222a.997.997 0 00.01.042l1.358 5.43-.893.892C3.74 11.846 4.632 14 6.414 14H15a1 1 0 000-2H6.414l1-1H14a1 1 0 00.894-.553l3-6A1 1 0 0017 3H6.28l-.31-1.243A1 1 0 005 1H3zM16 16.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0zM6.5 18a1.5 1.5 0 100-3 1.5 1.5 0 000 3z" />
            </svg>
          </button>
          
          {product.onSale && (
            <div className="absolute top-4 left-4 bg-red-500 text-white text-xs font-bold px-2 py-1 rounded">
              SALE
            </div>
          )}
        </div>
        
        <div className="p-4">
          <h3 className="font-semibold text-lg mb-1 group-hover:text-indigo-600">{product.name}</h3>
          <div className="flex items-center mb-2">
            <RatingStars rating={product.rating} />
            <span className="ml-2 text-gray-600 text-sm">({product.reviewCount})</span>
          </div>
          
          <div className="flex items-center gap-2">
            <span className="font-semibold">${product.price.toFixed(2)}</span>
            {product.originalPrice && (
              <span className="text-gray-500 text-sm line-through">${product.originalPrice.toFixed(2)}</span>
            )}
          </div>
        </div>
      </a>
    </Link>
  );
};

export default ProductCard;
EOL

# Create UI components
cat > ecommerce-otel/frontend/components/ui/RatingStars.js <<'EOL'
const RatingStars = ({ rating, max = 5 }) => {
  const fullStars = Math.floor(rating);
  const halfStar = rating % 1 >= 0.5;
  const emptyStars = max - fullStars - (halfStar ? 1 : 0);

  return (
    <div className="flex">
      {[...Array(fullStars)].map((_, i) => (
        <svg key={i} className="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
      ))}
      
      {halfStar && (
        <svg className="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
      )}
      
      {[...Array(emptyStars)].map((_, i) => (
        <svg key={i} className="w-5 h-5 text-gray-300" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
      ))}
    </div>
  );
};

export default RatingStars;
EOL

# Create pages
cat > ecommerce-otel/frontend/pages/_app.js <<'EOL'
import { CartProvider } from '../lib/cart';
import Header from '../components/layout/Header';
import Footer from '../components/layout/Footer';
import CartDrawer from '../components/cart/CartDrawer';
import '../styles/globals.css';

function MyApp({ Component, pageProps }) {
  return (
    <CartProvider>
      <div className="flex flex-col min-h-screen">
        <Header />
        <main className="flex-grow">
          <Component {...pageProps} />
        </main>
        <Footer />
        <CartDrawer />
      </div>
    </CartProvider>
  );
}

export default MyApp;
EOL

cat > ecommerce-otel/frontend/pages/index.js <<'EOL'
import { useEffect, useState } from 'react';
import Link from 'next/link';
import ProductCard from '../components/product/ProductCard';
import { fetchProducts } from '../lib/api';
import { trace } from '@opentelemetry/api';

export default function Home() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const tracer = trace.getTracer('home-page');
    const span = tracer.startSpan('fetch-featured-products');
    
    fetchProducts()
      .then(data => {
        setProducts(data.slice(0, 8));
        setLoading(false);
        span.end();
      })
      .catch(err => {
        console.error(err);
        span.recordException(err);
        span.end();
      });
  }, []);

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-12 text-center">
        <p>Loading featured products...</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl p-8 mb-12">
        <div className="max-w-2xl">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Summer Collection 2023</h1>
          <p className="text-xl mb-8">Discover our new arrivals and exclusive offers</p>
          <Link href="/products">
            <a className="bg-white text-indigo-600 font-semibold px-6 py-3 rounded-lg hover:bg-gray-100 transition-colors">
              Shop Now
            </a>
          </Link>
        </div>
      </section>

      {/* Featured Products */}
      <section className="mb-16">
        <div className="flex justify-between items-center mb-8">
          <h2 className="text-3xl font-bold">Featured Products</h2>
          <Link href="/products">
            <a className="text-indigo-600 hover:text-indigo-800 font-medium">
              View All Products →
            </a>
          </Link>
        </div>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {products.map(product => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </section>

      {/* Categories */}
      <section className="mb-16">
        <h2 className="text-3xl font-bold mb-8">Shop by Category</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {['Electronics', 'Clothing', 'Home & Garden'].map(category => (
            <Link key={category} href={`/products?category=${category.toLowerCase()}`}>
              <a className="group">
                <div className="aspect-video bg-gray-200 rounded-xl overflow-hidden relative">
                  <div className="absolute inset-0 bg-black bg-opacity-30 group-hover:bg-opacity-10 transition-all duration-300 flex items-center justify-center">
                    <h3 className="text-2xl font-bold text-white">{category}</h3>
                  </div>
                </div>
              </a>
            </Link>
          ))}
        </div>
      </section>

      {/* Testimonials */}
      <section className="bg-gray-100 rounded-xl p-8">
        <h2 className="text-3xl font-bold mb-8 text-center">What Our Customers Say</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              name: "Alex Johnson",
              text: "The quality of products exceeded my expectations. Fast shipping too!",
              rating: 5
            },
            {
              name: "Maria Garcia",
              text: "Excellent customer service. They helped me choose the perfect gift.",
              rating: 5
            },
            {
              name: "David Smith",
              text: "Great prices and a huge selection. Will definitely shop here again!",
              rating: 4
            }
          ].map((testimonial, index) => (
            <div key={index} className="bg-white p-6 rounded-lg shadow-sm">
              <RatingStars rating={testimonial.rating} />
              <p className="my-4 text-gray-700">{testimonial.text}</p>
              <p className="font-semibold">- {testimonial.name}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
EOL

# Create product listing page
cat > ecommerce-otel/frontend/pages/products/index.js <<'EOL'
import { useState, useEffect } from 'react';
import ProductCard from '../../components/product/ProductCard';
import FilterPanel from '../../components/search/FilterPanel';
import { fetchProducts } from '../../lib/api';
import { trace } from '@opentelemetry/api';

const ProductsPage = () => {
  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    category: 'all',
    priceRange: [0, 1000],
    minRating: 0
  });

  useEffect(() => {
    const tracer = trace.getTracer('products-page');
    const span = tracer.startSpan('fetch-products');
    
    fetchProducts()
      .then(data => {
        setProducts(data);
        setFilteredProducts(data);
        setLoading(false);
        span.end();
      })
      .catch(err => {
        console.error(err);
        span.recordException(err);
        span.end();
      });
  }, []);

  useEffect(() => {
    applyFilters();
  }, [filters]);

  const applyFilters = () => {
    const filtered = products.filter(product => {
      return (
        (filters.category === 'all' || product.category === filters.category) &&
        product.price >= filters.priceRange[0] && 
        product.price <= filters.priceRange[1] &&
        product.rating >= filters.minRating
      );
    });
    setFilteredProducts(filtered);
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-12 text-center">
        <p>Loading products...</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Shop Products</h1>
      
      <div className="flex flex-col md:flex-row gap-8">
        <div className="md:w-1/4">
          <FilterPanel filters={filters} setFilters={setFilters} />
        </div>
        
        <div className="md:w-3/4">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredProducts.map(product => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
          
          {filteredProducts.length === 0 && (
            <div className="text-center py-12">
              <p className="text-xl">No products match your filters</p>
              <button 
                onClick={() => setFilters({
                  category: 'all',
                  priceRange: [0, 1000],
                  minRating: 0
                })}
                className="mt-4 bg-indigo-600 text-white px-4 py-2 rounded-md"
              >
                Reset Filters
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductsPage;
EOL

# =============================
# BACKEND FILES
# =============================

# Create backend requirements
cat > ecommerce-otel/backend/requirements.txt <<'EOL'
fastapi==0.100.1
uvicorn==0.23.2
sqlalchemy==2.0.20
psycopg2-binary==2.9.7
python-dotenv==1.0.0
opentelemetry-api==1.19.0
opentelemetry-sdk==1.19.0
opentelemetry-exporter-otlp-proto-http==1.19.0
opentelemetry-instrumentation-fastapi==0.41b0
opentelemetry-instrumentation-sqlalchemy==0.41b0
EOL

# Create main backend file
cat > ecommerce-otel/backend/main.py <<'EOL'
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
EOL

# Create Dockerfile for frontend
cat > ecommerce-otel/frontend/Dockerfile <<'EOL'
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000

CMD ["node", "server.js"]
EOL

# Create Dockerfile for backend
cat > ecommerce-otel/backend/Dockerfile <<'EOL'
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOL

# Create README
cat > ecommerce-otel/README.md <<'EOL'
# E-commerce with Full-Stack Observability

This project demonstrates a modern e-commerce application with full-stack observability using OpenTelemetry.

## Features

- Modern responsive e-commerce UI (React/Next.js)
- Product listing with filtering and search
- Product detail pages with reviews
- Shopping cart functionality
- Multi-step checkout process
- Backend API (Python FastAPI)
- PostgreSQL database
- OpenTelemetry instrumentation
- Jaeger for tracing
- Prometheus for metrics
- Grafana for visualization

## Architecture

![Architecture Diagram](https://i.imgur.com/5XeW5rE.png)

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone this repository
2. Navigate to the project directory
3. Run the application:

```bash
docker-compose up --build

EOL

cat > ecommerce-otel/frontend/components/cart/CartDrawer.js <<'EOL'
import { useCart } from '../../lib/cart';
import CartItem from './CartItem';

const CartDrawer = () => {
  const { cart, isCartOpen, setIsCartOpen, cartCount, cartTotal, removeItem, updateQuantity } = useCart();

  if (!isCartOpen) return null;

  return (
    <div className="fixed inset-0 z-50">
      <div 
        className="absolute inset-0 bg-black bg-opacity-50"
        onClick={() => setIsCartOpen(false)}
      />
      
      <div className="absolute right-0 top-0 h-full w-full max-w-md bg-white shadow-xl flex flex-col">
        <div className="p-6 border-b">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-bold">Your Cart ({cartCount})</h2>
            <button onClick={() => setIsCartOpen(false)} className="text-gray-500 hover:text-gray-700">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        
        <div className="flex-grow overflow-y-auto p-6">
          {cartCount === 0 ? (
            <div className="text-center py-12">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              <p className="mt-4 text-gray-600">Your cart is empty</p>
              <button 
                onClick={() => setIsCartOpen(false)}
                className="mt-6 bg-indigo-600 text-white px-6 py-2 rounded-md hover:bg-indigo-700"
              >
                Continue Shopping
              </button>
            </div>
          ) : (
            <>
              <div className="space-y-6">
                {cart.map(item => (
                  <CartItem 
                    key={`${item.id}-${item.size}`} 
                    item={item} 
                    onRemove={() => removeItem(item.id, item.size)}
                    onUpdateQuantity={(qty) => updateQuantity(item.id, item.size, qty)}
                  />
                ))}
              </div>
              
              <div className="mt-8 border-t pt-6">
                <div className="flex justify-between text-lg font-semibold mb-4">
                  <span>Subtotal:</span>
                  <span>${cartTotal.toFixed(2)}</span>
                </div>
                <p className="text-gray-600 text-sm mb-6">
                  Shipping and taxes calculated at checkout.
                </p>
                <button 
                  onClick={() => router.push('/checkout')}
                  className="w-full bg-indigo-600 text-white py-3 rounded-md hover:bg-indigo-700"
                >
                  Proceed to Checkout
                </button>
                <button 
                  onClick={() => setIsCartOpen(false)}
                  className="w-full mt-3 border border-gray-300 text-gray-700 py-3 rounded-md hover:bg-gray-50"
                >
                  Continue Shopping
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default CartDrawer;
EOL

cat > ecommerce-otel/frontend/components/cart/CartItem.js <<'EOL'
const CartItem = ({ item, onRemove, onUpdateQuantity }) => {
  return (
    <div className="flex items-center gap-4">
      <div className="w-24 h-24 bg-gray-100 rounded-md overflow-hidden">
        {item.image ? (
          <img 
            src={item.image} 
            alt={item.name} 
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full bg-gray-200 border-2 border-dashed rounded-xl flex items-center justify-center text-gray-400">
            No Image
          </div>
        )}
      </div>
      
      <div className="flex-grow">
        <h3 className="font-medium">{item.name}</h3>
        {item.size && <p className="text-gray-600 text-sm">Size: {item.size}</p>}
        <p className="font-semibold">${item.price.toFixed(2)}</p>
        
        <div className="flex items-center mt-2">
          <div className="flex border rounded-md">
            <button 
              onClick={() => onUpdateQuantity(item.quantity - 1)}
              className="px-3 py-1 bg-gray-100 hover:bg-gray-200"
            >
              -
            </button>
            <span className="px-3 py-1">{item.quantity}</span>
            <button 
              onClick={() => onUpdateQuantity(item.quantity + 1)}
              className="px-3 py-1 bg-gray-100 hover:bg-gray-200"
            >
              +
            </button>
          </div>
          <button 
            onClick={onRemove}
            className="ml-4 text-red-600 hover:text-red-800 text-sm"
          >
            Remove
          </button>
        </div>
      </div>
    </div>
  );
};

export default CartItem;
EOL

cat > ecommerce-otel/frontend/components/search/FilterPanel.js <<'EOL'
const FilterPanel = ({ filters, setFilters }) => {
  const categories = ['electronics', 'clothing', 'home', 'accessories'];
  
  return (
    <div className="bg-white p-6 rounded-lg shadow-sm">
      <h3 className="text-lg font-semibold mb-4">Filters</h3>
      
      <div className="space-y-6">
        <div>
          <h4 className="font-medium mb-2">Category</h4>
          <div className="space-y-2">
            <label className="flex items-center">
              <input
                type="radio"
                name="category"
                checked={filters.category === 'all'}
                onChange={() => setFilters({...filters, category: 'all'})}
                className="mr-2"
              />
              <span>All Categories</span>
            </label>
            
            {categories.map(category => (
              <label key={category} className="flex items-center">
                <input
                  type="radio"
                  name="category"
                  checked={filters.category === category}
                  onChange={() => setFilters({...filters, category})}
                  className="mr-2"
                />
                <span className="capitalize">{category}</span>
              </label>
            ))}
          </div>
        </div>
        
        <div>
          <h4 className="font-medium mb-2">Price Range</h4>
          <div className="space-y-3">
            <div>
              <input
                type="range"
                min="0"
                max="1000"
                value={filters.priceRange[1]}
                onChange={(e) => setFilters({
                  ...filters,
                  priceRange: [filters.priceRange[0], parseInt(e.target.value)]
                })}
                className="w-full"
              />
            </div>
            <div className="flex justify-between text-sm">
              <span>$0</span>
              <span>${filters.priceRange[1]}</span>
            </div>
          </div>
        </div>
        
        <div>
          <h4 className="font-medium mb-2">Minimum Rating</h4>
          <div className="space-y-2">
            {[4, 3, 2, 1, 0].map(rating => (
              <label key={rating} className="flex items-center">
                <input
                  type="radio"
                  name="rating"
                  checked={filters.minRating === rating}
                  onChange={() => setFilters({...filters, minRating: rating})}
                  className="mr-2"
                />
                <span>{rating}+ Stars</span>
              </label>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default FilterPanel;
EOL


cat > ecommerce-otel/frontend/components/search/SearchBar.js <<'EOL'
import { useState } from 'react';
import { useRouter } from 'next/router';

const SearchBar = () => {
  const [query, setQuery] = useState('');
  const router = useRouter();

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim()) {
      router.push(`/products?search=${encodeURIComponent(query.trim())}`);
    }
  };

  return (
    <form onSubmit={handleSearch} className="relative">
      <input
        type="text"
        placeholder="Search products..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
      />
      <button 
        type="submit"
        className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-indigo-600"
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </button>
    </form>
  );
};

export default SearchBar;
EOL