import React from 'react';
import ProductCard from './ProductCard';
export default function ProductGrid({ products, onAdd }) {
  return (
    <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 p-4">
      {products.map((p) => (
        <ProductCard key={p.id} product={p} onAdd={onAdd} />
      ))}
    </div>
  );
}