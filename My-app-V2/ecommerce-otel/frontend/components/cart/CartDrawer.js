import { useCart } from '../../lib/cart';
import CartItem from './CartItem';

const CartDrawer = () => {
  const { cart, isCartOpen, setIsCartOpen, cartCount, cartTotal, removeItem, updateQuantity } = useCart();

  if (!isCartOpen) return null;

  return (
    <div className="fixed inset-0 z-50">
      <div 
        className="absolute inset-0 bg-black bg-opacity-50"
        onClick={() => setIsCartOpen(false)}
      />
      
      <div className="absolute right-0 top-0 h-full w-full max-w-md bg-white shadow-xl flex flex-col">
        <div className="p-6 border-b">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-bold">Your Cart ({cartCount})</h2>
            <button onClick={() => setIsCartOpen(false)} className="text-gray-500 hover:text-gray-700">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        
        <div className="flex-grow overflow-y-auto p-6">
          {cartCount === 0 ? (
            <div className="text-center py-12">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              <p className="mt-4 text-gray-600">Your cart is empty</p>
              <button 
                onClick={() => setIsCartOpen(false)}
                className="mt-6 bg-indigo-600 text-white px-6 py-2 rounded-md hover:bg-indigo-700"
              >
                Continue Shopping
              </button>
            </div>
          ) : (
            <>
              <div className="space-y-6">
                {cart.map(item => (
                  <CartItem 
                    key={`${item.id}-${item.size}`} 
                    item={item} 
                    onRemove={() => removeItem(item.id, item.size)}
                    onUpdateQuantity={(qty) => updateQuantity(item.id, item.size, qty)}
                  />
                ))}
              </div>
              
              <div className="mt-8 border-t pt-6">
                <div className="flex justify-between text-lg font-semibold mb-4">
                  <span>Subtotal:</span>
                  <span>${cartTotal.toFixed(2)}</span>
                </div>
                <p className="text-gray-600 text-sm mb-6">
                  Shipping and taxes calculated at checkout.
                </p>
                <button 
                  onClick={() => router.push('/checkout')}
                  className="w-full bg-indigo-600 text-white py-3 rounded-md hover:bg-indigo-700"
                >
                  Proceed to Checkout
                </button>
                <button 
                  onClick={() => setIsCartOpen(false)}
                  className="w-full mt-3 border border-gray-300 text-gray-700 py-3 rounded-md hover:bg-gray-50"
                >
                  Continue Shopping
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default CartDrawer;
