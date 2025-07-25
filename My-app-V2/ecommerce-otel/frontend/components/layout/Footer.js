import Link from 'next/link';

const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white py-12">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-xl font-bold mb-4">ShopNext</h3>
            <p className="text-gray-400">
              Your one-stop shop for all your needs. Quality products at affordable prices.
            </p>
          </div>
          
          <div>
            <h4 className="text-lg font-semibold mb-4">Shop</h4>
            <ul className="space-y-2 text-gray-400">
              <li><Link href="/products"><a className="hover:text-white">All Products</a></Link></li>
              <li><Link href="/products?category=electronics"><a className="hover:text-white">Electronics</a></Link></li>
              <li><Link href="/products?category=clothing"><a className="hover:text-white">Clothing</a></Link></li>
              <li><Link href="/products?category=home"><a className="hover:text-white">Home & Garden</a></Link></li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-lg font-semibold mb-4">Customer Service</h4>
            <ul className="space-y-2 text-gray-400">
              <li><Link href="/contact"><a className="hover:text-white">Contact Us</a></Link></li>
              <li><Link href="/faq"><a className="hover:text-white">FAQs</a></Link></li>
              <li><Link href="/shipping"><a className="hover:text-white">Shipping Policy</a></Link></li>
              <li><Link href="/returns"><a className="hover:text-white">Returns & Exchanges</a></Link></li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-lg font-semibold mb-4">Stay Connected</h4>
            <p className="text-gray-400 mb-4">
              Subscribe to our newsletter for the latest updates and offers.
            </p>
            <div className="flex">
              <input 
                type="email" 
                placeholder="Your email" 
                className="px-4 py-2 rounded-l-md w-full text-gray-800"
              />
              <button className="bg-indigo-600 px-4 py-2 rounded-r-md">
                Subscribe
              </button>
            </div>
          </div>
        </div>
        
        <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
          <p>© 2023 ShopNext. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
