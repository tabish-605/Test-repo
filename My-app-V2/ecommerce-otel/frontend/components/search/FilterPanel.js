const FilterPanel = ({ filters, setFilters }) => {
  const categories = ['electronics', 'clothing', 'home', 'accessories'];
  
  return (
    <div className="bg-white p-6 rounded-lg shadow-sm">
      <h3 className="text-lg font-semibold mb-4">Filters</h3>
      
      <div className="space-y-6">
        <div>
          <h4 className="font-medium mb-2">Category</h4>
          <div className="space-y-2">
            <label className="flex items-center">
              <input
                type="radio"
                name="category"
                checked={filters.category === 'all'}
                onChange={() => setFilters({...filters, category: 'all'})}
                className="mr-2"
              />
              <span>All Categories</span>
            </label>
            
            {categories.map(category => (
              <label key={category} className="flex items-center">
                <input
                  type="radio"
                  name="category"
                  checked={filters.category === category}
                  onChange={() => setFilters({...filters, category})}
                  className="mr-2"
                />
                <span className="capitalize">{category}</span>
              </label>
            ))}
          </div>
        </div>
        
        <div>
          <h4 className="font-medium mb-2">Price Range</h4>
          <div className="space-y-3">
            <div>
              <input
                type="range"
                min="0"
                max="1000"
                value={filters.priceRange[1]}
                onChange={(e) => setFilters({
                  ...filters,
                  priceRange: [filters.priceRange[0], parseInt(e.target.value)]
                })}
                className="w-full"
              />
            </div>
            <div className="flex justify-between text-sm">
              <span>$0</span>
              <span>${filters.priceRange[1]}</span>
            </div>
          </div>
        </div>
        
        <div>
          <h4 className="font-medium mb-2">Minimum Rating</h4>
          <div className="space-y-2">
            {[4, 3, 2, 1, 0].map(rating => (
              <label key={rating} className="flex items-center">
                <input
                  type="radio"
                  name="rating"
                  checked={filters.minRating === rating}
                  onChange={() => setFilters({...filters, minRating: rating})}
                  className="mr-2"
                />
                <span>{rating}+ Stars</span>
              </label>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default FilterPanel;
