-- postgres/init.sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    stock_quantity INTEGER NOT NULL
);

INSERT INTO products (name, description, price, stock_quantity) VALUES
('OTel T-Shirt', 'A comfy t-shirt for observability enthusiasts.', 25.00, 100),
('K8s Beanie', 'Stay warm while managing your clusters.', 15.50, 50),
('Docker Mug', 'The perfect mug for your containerized coffee.', 12.00, 200);
