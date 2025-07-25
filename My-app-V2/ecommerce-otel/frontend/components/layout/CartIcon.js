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
