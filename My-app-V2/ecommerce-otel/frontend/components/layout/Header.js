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
