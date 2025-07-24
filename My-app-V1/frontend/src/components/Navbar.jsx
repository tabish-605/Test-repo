import React from 'react';
export default function Navbar({ cartCount, onCheckout }) {
  return (
    <nav className="bg-indigo-600 text-white p-4 flex items-center justify-between">
      <h1 className="font-semibold text-xl">Observa-Lite</h1>
      <button onClick={onCheckout} className="relative">
        Cart ({cartCount})
      </button>
    </nav>
  );
}