import React from 'react';
export default function ProductCard({ product, onAdd }) {
  return (
    <div className="border rounded p-4 flex flex-col">
      <h3 className="font-medium flex-1">{product.name}</h3>
      <p className="text-sm text-gray-500 mb-2">${product.price.toFixed(2)}</p>
      <button onClick={() => onAdd(product.id)} className="bg-indigo-500 text-white px-3 py-1 rounded hover:bg-indigo-600">Add to cart</button>
    </div>
  );
}