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
