import './style.css';
import './otel.js';
import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import Navbar from './components/Navbar.jsx';
import ProductGrid from './components/ProductGrid.jsx';
import { api } from './api.js';

function App() {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);

  useEffect(() => {
    api.products().then((data) => setProducts(data.products || []));
  }, []);

  const addToCart = (id) => {
    api.addToCart(id).then(() => setCart([...cart, id]));
  };

  const checkout = () => {
    api.checkout().then(() => {
      alert('Checkout complete');
      setCart([]);
    }).catch(() => alert('Checkout failed (simulated)'));
  };

  return (
    <>
      <Navbar cartCount={cart.length} onCheckout={checkout} />
      <ProductGrid products={products} onAdd={addToCart} />
    </>
  );
}

const container = document.getElementById('root');
createRoot(container).render(<App />);
