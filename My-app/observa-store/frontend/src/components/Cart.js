// frontend/src/components/Cart.js
import React from 'react';

const Cart = ({ cartItems, onCheckout }) => {
  return (
    <div>
      <h2>Shopping Cart</h2>
      <ul>
        {cartItems.map((item, index) => (
          <li key={index}>{item[1]}</li>
        ))}
      </ul>
      <button onClick={onCheckout} disabled={cartItems.length === 0}>
        Checkout
      </button>
    </div>
  );
};

export default Cart;
