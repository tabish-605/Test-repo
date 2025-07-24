// frontend/src/App.js
import React, { useState } from 'react';
import ProductList from './components/ProductList';
import Cart from './components/Cart';
import './App.css';

function App() {
  const [cartItems, setCartItems] = useState([]);

  const handleAddToCart = (product) => {
    fetch('http://localhost:8000/api/cart/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ product_id: product[0], quantity: 1 }),
    }).then(() => {
        setCartItems([...cartItems, product]);
    });
  };

  const handleCheckout = () => {
    fetch('http://localhost:8000/api/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ items: cartItems }),
    }).then(response => {
        if (response.ok) {
            alert('Checkout successful!');
            setCartItems([]);
        } else {
            alert('Checkout failed!');
        }
    });
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>ObservaStore</h1>
      </header>
      <main>
        <ProductList onAddToCart={handleAddToCart} />
        <Cart cartItems={cartItems} onCheckout={handleCheckout} />
      </main>
    </div>
  );
}

export default App;
