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
