CREATE TABLE IF NOT EXISTS products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  description TEXT,
  price NUMERIC(10,2)
);
INSERT INTO products (name, description, price) VALUES
('OTel T-Shirt','Comfy cotton tee',25.00),
('K8s Beanie','Stay warm while kubing',15.50),
('Docker Mug','Sip while you ship',12.00)
ON CONFLICT DO NOTHING;
