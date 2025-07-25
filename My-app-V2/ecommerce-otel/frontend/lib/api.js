export const fetchProducts = async () => {
  const response = await fetch('/api/products');
  return await response.json();
};

export const fetchProduct = async (slug) => {
  const response = await fetch(`/api/products/${slug}`);
  return await response.json();
};

export const addToCart = async (item) => {
  const response = await fetch('/api/cart', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(item)
  });
  return await response.json();
};
