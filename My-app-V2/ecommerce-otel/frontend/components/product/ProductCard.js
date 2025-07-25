import Link from 'next/link';
import RatingStars from '../ui/RatingStars';
import { useCart } from '../../lib/cart';

const ProductCard = ({ product }) => {
  const { addToCart } = useCart();
  
  const handleAddToCart = (e) => {
    e.preventDefault();
    e.stopPropagation();
    addToCart({
      ...product,
      quantity: 1,
      size: product.sizes?.[0] || 'One Size'
    });
  };

  return (
    <Link href={`/products/${product.slug}`}>
      <a className="group block overflow-hidden transition-transform hover:scale-[1.02]">
        <div className="relative">
          <div className="aspect-square bg-gray-100 rounded-lg overflow-hidden">
            {product.image ? (
              <img 
                src={product.image} 
                alt={product.name} 
                className="w-full h-full object-cover transition-transform group-hover:scale-105"
              />
            ) : (
              <div className="w-full h-full bg-gray-200 border-2 border-dashed rounded-xl flex items-center justify-center text-gray-400">
                No Image
              </div>
            )}
          </div>
          
          <button 
            onClick={handleAddToCart}
            className="absolute bottom-4 right-4 bg-white rounded-full p-2 shadow-md opacity-0 group-hover:opacity-100 transition-opacity"
            aria-label="Add to cart"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M3 1a1 1 0 000 2h1.22l.305 1.222a.997.997 0 00.01.042l1.358 5.43-.893.892C3.74 11.846 4.632 14 6.414 14H15a1 1 0 000-2H6.414l1-1H14a1 1 0 00.894-.553l3-6A1 1 0 0017 3H6.28l-.31-1.243A1 1 0 005 1H3zM16 16.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0zM6.5 18a1.5 1.5 0 100-3 1.5 1.5 0 000 3z" />
            </svg>
          </button>
          
          {product.onSale && (
            <div className="absolute top-4 left-4 bg-red-500 text-white text-xs font-bold px-2 py-1 rounded">
              SALE
            </div>
          )}
        </div>
        
        <div className="p-4">
          <h3 className="font-semibold text-lg mb-1 group-hover:text-indigo-600">{product.name}</h3>
          <div className="flex items-center mb-2">
            <RatingStars rating={product.rating} />
            <span className="ml-2 text-gray-600 text-sm">({product.reviewCount})</span>
          </div>
          
          <div className="flex items-center gap-2">
            <span className="font-semibold">${product.price.toFixed(2)}</span>
            {product.originalPrice && (
              <span className="text-gray-500 text-sm line-through">${product.originalPrice.toFixed(2)}</span>
            )}
          </div>
        </div>
      </a>
    </Link>
  );
};

export default ProductCard;
