const CartItem = ({ item, onRemove, onUpdateQuantity }) => {
  return (
    <div className="flex items-center gap-4">
      <div className="w-24 h-24 bg-gray-100 rounded-md overflow-hidden">
        {item.image ? (
          <img 
            src={item.image} 
            alt={item.name} 
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full bg-gray-200 border-2 border-dashed rounded-xl flex items-center justify-center text-gray-400">
            No Image
          </div>
        )}
      </div>
      
      <div className="flex-grow">
        <h3 className="font-medium">{item.name}</h3>
        {item.size && <p className="text-gray-600 text-sm">Size: {item.size}</p>}
        <p className="font-semibold">${item.price.toFixed(2)}</p>
        
        <div className="flex items-center mt-2">
          <div className="flex border rounded-md">
            <button 
              onClick={() => onUpdateQuantity(item.quantity - 1)}
              className="px-3 py-1 bg-gray-100 hover:bg-gray-200"
            >
              -
            </button>
            <span className="px-3 py-1">{item.quantity}</span>
            <button 
              onClick={() => onUpdateQuantity(item.quantity + 1)}
              className="px-3 py-1 bg-gray-100 hover:bg-gray-200"
            >
              +
            </button>
          </div>
          <button 
            onClick={onRemove}
            className="ml-4 text-red-600 hover:text-red-800 text-sm"
          >
            Remove
          </button>
        </div>
      </div>
    </div>
  );
};

export default CartItem;
