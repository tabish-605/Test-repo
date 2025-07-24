export async function fetchJson(url, opts = {}) {
  const res = await fetch(url, opts);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
export const api = {
  products: () => fetchJson('/api/products'),
  addToCart: (productId) => fetchJson('/api/cart/add', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ product_id: productId, quantity: 1 }) }),
  checkout: () => fetchJson('/api/checkout', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({}) }),
};