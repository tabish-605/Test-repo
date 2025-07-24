
import { useEffect, useState } from 'react'
export default function Home() {
  const [products, setProducts] = useState([])
  useEffect(() => {
    fetch('http://localhost:8000/products').then(res => res.json()).then(setProducts)
  }, [])
  return (
    <main>
      <h1>Products</h1>
      <ul>
        {products.map((p:any) => (
          <li key={p.id}>{p.name} - ${p.price}</li>
        ))}
      </ul>
    </main>
  )
}
