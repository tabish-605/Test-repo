<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PyShop - Python Ecommerce Platform</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.js"></script>
    <style>
        :root {
            --primary: #4a6de5;
            --primary-dark: #3a5bd9;
            --secondary: #f8f9fa;
            --dark: #343a40;
            --light: #f8f9fa;
            --success: #28a745;
            --danger: #dc3545;
            --warning: #ffc107;
            --gray: #6c757d;
            --light-gray: #e9ecef;
            --border: #dee2e6;
            --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            --transition: all 0.3s ease;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Poppins', sans-serif;
            background-color: #f5f7fb;
            color: var(--dark);
            line-height: 1.6;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 15px;
        }

        /* Header Styles */
        header {
            background-color: white;
            box-shadow: var(--shadow);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .header-top {
            background-color: var(--dark);
            color: white;
            padding: 8px 0;
            font-size: 14px;
        }

        .header-main {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 0;
        }

        .logo {
            font-size: 24px;
            font-weight: 700;
            color: var(--primary);
            display: flex;
            align-items: center;
        }

        .logo i {
            margin-right: 8px;
        }

        .search-bar {
            flex-grow: 1;
            max-width: 600px;
            margin: 0 20px;
            position: relative;
        }

        .search-bar input {
            width: 100%;
            padding: 12px 20px;
            border: 1px solid var(--border);
            border-radius: 30px;
            font-size: 16px;
            outline: none;
            transition: var(--transition);
        }

        .search-bar input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(74, 109, 229, 0.2);
        }

        .search-bar button {
            position: absolute;
            right: 5px;
            top: 5px;
            background: var(--primary);
            color: white;
            border: none;
            border-radius: 30px;
            padding: 7px 20px;
            cursor: pointer;
            transition: var(--transition);
        }

        .search-bar button:hover {
            background: var(--primary-dark);
        }

        .header-icons {
            display: flex;
            gap: 20px;
        }

        .header-icon {
            position: relative;
            cursor: pointer;
            color: var(--dark);
            font-size: 20px;
        }

        .icon-badge {
            position: absolute;
            top: -8px;
            right: -8px;
            background: var(--danger);
            color: white;
            border-radius: 50%;
            width: 18px;
            height: 18px;
            font-size: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        /* Navigation */
        nav {
            background-color: var(--primary);
            padding: 15px 0;
        }

        .nav-menu {
            display: flex;
            list-style: none;
            gap: 25px;
        }

        .nav-menu li a {
            color: white;
            text-decoration: none;
            font-weight: 500;
            transition: var(--transition);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .nav-menu li a:hover {
            color: var(--light-gray);
        }

        /* Hero Section */
        .hero {
            background: linear-gradient(135deg, #4a6de5 0%, #6a11cb 100%);
            color: white;
            padding: 80px 0;
            margin-bottom: 40px;
            border-radius: 0 0 20px 20px;
        }

        .hero-content {
            max-width: 600px;
        }

        .hero h1 {
            font-size: 48px;
            margin-bottom: 20px;
            line-height: 1.2;
        }

        .hero p {
            font-size: 18px;
            margin-bottom: 30px;
            opacity: 0.9;
        }

        .btn {
            display: inline-block;
            padding: 12px 30px;
            background-color: white;
            color: var(--primary);
            border-radius: 30px;
            text-decoration: none;
            font-weight: 600;
            transition: var(--transition);
            border: none;
            cursor: pointer;
            font-size: 16px;
        }

        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        }

        .btn-primary {
            background-color: var(--primary);
            color: white;
        }

        .btn-primary:hover {
            background-color: var(--primary-dark);
        }

        /* Categories */
        .section-title {
            font-size: 28px;
            margin-bottom: 30px;
            position: relative;
            padding-bottom: 15px;
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 60px;
            height: 4px;
            background: var(--primary);
            border-radius: 2px;
        }

        .categories {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }

        .category-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: var(--shadow);
            transition: var(--transition);
            cursor: pointer;
        }

        .category-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        }

        .category-card i {
            font-size: 36px;
            color: var(--primary);
            margin-bottom: 15px;
        }

        .category-card h3 {
            font-size: 18px;
        }

        /* Products */
        .products {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 30px;
            margin-bottom: 50px;
        }

        .product-card {
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: var(--shadow);
            transition: var(--transition);
            position: relative;
        }

        .product-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
        }

        .product-badge {
            position: absolute;
            top: 10px;
            left: 10px;
            background: var(--danger);
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
        }

        .product-img {
            height: 200px;
            width: 100%;
            object-fit: cover;
            border-bottom: 1px solid var(--border);
        }

        .product-info {
            padding: 20px;
        }

        .product-title {
            font-size: 18px;
            margin-bottom: 10px;
            font-weight: 600;
        }

        .product-price {
            color: var(--primary);
            font-weight: 700;
            font-size: 20px;
            margin-bottom: 15px;
        }

        .product-price .old-price {
            color: var(--gray);
            text-decoration: line-through;
            font-size: 16px;
            margin-right: 8px;
        }

        .product-rating {
            color: var(--warning);
            margin-bottom: 15px;
        }

        .product-actions {
            display: flex;
            gap: 10px;
        }

        .action-btn {
            flex: 1;
            padding: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: var(--transition);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .add-to-cart {
            background: var(--primary);
            color: white;
        }

        .add-to-cart:hover {
            background: var(--primary-dark);
        }

        .wishlist {
            background: var(--light-gray);
            color: var(--dark);
        }

        .wishlist:hover {
            background: var(--border);
        }

        /* Cart Modal */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 1000;
            justify-content: center;
            align-items: flex-start;
            padding-top: 50px;
            overflow: auto;
        }

        .modal-content {
            background: white;
            border-radius: 10px;
            width: 90%;
            max-width: 800px;
            max-height: 80vh;
            overflow-y: auto;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            animation: modalOpen 0.3s ease;
        }

        @keyframes modalOpen {
            from { opacity: 0; transform: translateY(-50px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .modal-header {
            padding: 20px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .modal-title {
            font-size: 24px;
            font-weight: 600;
        }

        .close-modal {
            background: none;
            border: none;
            font-size: 24px;
            cursor: pointer;
            color: var(--gray);
        }

        .modal-body {
            padding: 20px;
        }

        .cart-items {
            margin-bottom: 20px;
        }

        .cart-item {
            display: flex;
            padding: 15px 0;
            border-bottom: 1px solid var(--border);
            gap: 20px;
        }

        .cart-item-img {
            width: 100px;
            height: 100px;
            object-fit: cover;
            border-radius: 8px;
        }

        .cart-item-details {
            flex-grow: 1;
        }

        .cart-item-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 5px;
        }

        .cart-item-price {
            color: var(--primary);
            font-weight: 700;
            margin-bottom: 10px;
        }

        .cart-item-actions {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .quantity-btn {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            border: 1px solid var(--border);
            background: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .quantity-input {
            width: 40px;
            text-align: center;
            border: 1px solid var(--border);
            border-radius: 5px;
            padding: 5px;
        }

        .remove-item {
            background: none;
            border: none;
            color: var(--danger);
            cursor: pointer;
            margin-left: 15px;
        }

        .cart-summary {
            background: var(--light);
            padding: 20px;
            border-radius: 10px;
        }

        .summary-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            padding: 8px 0;
        }

        .summary-total {
            font-size: 20px;
            font-weight: 700;
            border-top: 1px solid var(--border);
            padding-top: 15px;
            margin-top: 10px;
        }

        .checkout-btn {
            width: 100%;
            padding: 15px;
            background: var(--primary);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
            margin-top: 20px;
        }

        .checkout-btn:hover {
            background: var(--primary-dark);
        }

        /* Footer */
        footer {
            background: var(--dark);
            color: white;
            padding: 60px 0 30px;
            margin-top: 60px;
        }

        .footer-content {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }

        .footer-column h3 {
            font-size: 20px;
            margin-bottom: 20px;
            position: relative;
            padding-bottom: 10px;
        }

        .footer-column h3::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 40px;
            height: 3px;
            background: var(--primary);
        }

        .footer-links {
            list-style: none;
        }

        .footer-links li {
            margin-bottom: 12px;
        }

        .footer-links a {
            color: #aaa;
            text-decoration: none;
            transition: var(--transition);
        }

        .footer-links a:hover {
            color: white;
            padding-left: 5px;
        }

        .social-icons {
            display: flex;
            gap: 15px;
            margin-top: 20px;
        }

        .social-icon {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: #444;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            text-decoration: none;
            transition: var(--transition);
        }

        .social-icon:hover {
            background: var(--primary);
            transform: translateY(-3px);
        }

        .footer-bottom {
            text-align: center;
            padding-top: 30px;
            border-top: 1px solid #444;
            color: #aaa;
            font-size: 14px;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .header-main {
                flex-direction: column;
                gap: 15px;
            }
            
            .search-bar {
                width: 100%;
                max-width: none;
                margin: 15px 0;
            }
            
            .hero h1 {
                font-size: 36px;
            }
            
            .nav-menu {
                flex-wrap: wrap;
                justify-content: center;
            }
        }
        
        /* Loading indicator */
        .loader {
            border: 5px solid #f3f3f3;
            border-top: 5px solid var(--primary);
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 2s linear infinite;
            margin: 50px auto;
            display: none;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .pyodide-loading {
            text-align: center;
            padding: 20px;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <!-- Header Section -->
    <header>
        <div class="header-top">
            <div class="container">
                <div class="text-center">Free shipping on orders over $50!</div>
            </div>
        </div>
        <div class="container">
            <div class="header-main">
                <div class="logo">
                    <i class="fas fa-shopping-bag"></i>
                    <span>PyShop</span>
                </div>
                <div class="search-bar">
                    <input type="text" id="search-input" placeholder="Search for products...">
                    <button id="search-btn"><i class="fas fa-search"></i></button>
                </div>
                <div class="header-icons">
                    <div class="header-icon" id="user-icon">
                        <i class="fas fa-user"></i>
                    </div>
                    <div class="header-icon" id="wishlist-icon">
                        <i class="fas fa-heart"></i>
                        <span class="icon-badge">3</span>
                    </div>
                    <div class="header-icon" id="cart-icon">
                        <i class="fas fa-shopping-cart"></i>
                        <span class="icon-badge" id="cart-count">0</span>
                    </div>
                </div>
            </div>
        </div>
        <nav>
            <div class="container">
                <ul class="nav-menu">
                    <li><a href="#"><i class="fas fa-home"></i> Home</a></li>
                    <li><a href="#"><i class="fas fa-tag"></i> Deals</a></li>
                    <li><a href="#"><i class="fas fa-mobile-alt"></i> Electronics</a></li>
                    <li><a href="#"><i class="fas fa-tshirt"></i> Fashion</a></li>
                    <li><a href="#"><i class="fas fa-home"></i> Home & Kitchen</a></li>
                    <li><a href="#"><i class="fas fa-dumbbell"></i> Sports</a></li>
                    <li><a href="#"><i class="fas fa-book"></i> Books</a></li>
                </ul>
            </div>
        </nav>
    </header>

    <!-- Hero Section -->
    <section class="hero">
        <div class="container">
            <div class="hero-content">
                <h1>Summer Sale Up To 50% Off</h1>
                <p>Discover amazing deals on our latest collection. Limited time offer!</p>
                <a href="#" class="btn">Shop Now</a>
            </div>
        </div>
    </section>

    <!-- Main Content -->
    <main class="container">
        <!-- Pyodide Loading Indicator -->
        <div id="pyodide-loading" class="pyodide-loading">
            <div class="loader"></div>
            <p>Initializing Python environment...</p>
        </div>
        
        <!-- Categories -->
        <section id="categories-section" style="display: none;">
            <h2 class="section-title">Shop By Category</h2>
            <div class="categories" id="categories-container">
                <!-- Categories will be populated by Python -->
            </div>
        </section>

        <!-- Featured Products -->
        <section id="featured-section" style="display: none;">
            <h2 class="section-title">Featured Products</h2>
            <div class="products" id="featured-products">
                <!-- Products will be populated by Python -->
            </div>
        </section>

        <!-- Top Deals -->
        <section id="deals-section" style="display: none;">
            <h2 class="section-title">Top Deals</h2>
            <div class="products" id="deals-products">
                <!-- Products will be populated by Python -->
            </div>
        </section>
    </main>

    <!-- Shopping Cart Modal -->
    <div class="modal" id="cart-modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-title">Your Shopping Cart</h3>
                <button class="close-modal">&times;</button>
            </div>
            <div class="modal-body">
                <div class="cart-items" id="cart-items">
                    <!-- Cart items will be populated by Python -->
                </div>
                <div class="cart-summary">
                    <div class="summary-row">
                        <span>Subtotal:</span>
                        <span id="cart-subtotal">$0.00</span>
                    </div>
                    <div class="summary-row">
                        <span>Shipping:</span>
                        <span id="cart-shipping">$5.99</span>
                    </div>
                    <div class="summary-row">
                        <span>Tax:</span>
                        <span id="cart-tax">$0.00</span>
                    </div>
                    <div class="summary-row summary-total">
                        <span>Total:</span>
                        <span id="cart-total">$0.00</span>
                    </div>
                    <button class="checkout-btn">Proceed to Checkout</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-column">
                    <h3>PyShop</h3>
                    <p>Your one-stop shop for all your needs. We offer quality products at competitive prices with fast shipping.</p>
                    <div class="social-icons">
                        <a href="#" class="social-icon"><i class="fab fa-facebook-f"></i></a>
                        <a href="#" class="social-icon"><i class="fab fa-twitter"></i></a>
                        <a href="#" class="social-icon"><i class="fab fa-instagram"></i></a>
                        <a href="#" class="social-icon"><i class="fab fa-pinterest"></i></a>
                    </div>
                </div>
                <div class="footer-column">
                    <h3>Quick Links</h3>
                    <ul class="footer-links">
                        <li><a href="#">Home</a></li>
                        <li><a href="#">About Us</a></li>
                        <li><a href="#">Products</a></li>
                        <li><a href="#">Deals</a></li>
                        <li><a href="#">Contact</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>Customer Service</h3>
                    <ul class="footer-links">
                        <li><a href="#">FAQ</a></li>
                        <li><a href="#">Shipping Policy</a></li>
                        <li><a href="#">Returns & Exchanges</a></li>
                        <li><a href="#">Track Order</a></li>
                        <li><a href="#">Privacy Policy</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>Contact Us</h3>
                    <ul class="footer-links">
                        <li><i class="fas fa-map-marker-alt"></i> 123 Python Street, Code City</li>
                        <li><i class="fas fa-phone"></i> (123) 456-7890</li>
                        <li><i class="fas fa-envelope"></i> info@pyshop.com</li>
                        <li><i class="fas fa-clock"></i> Mon-Fri: 9AM - 6PM</li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2023 PyShop. All rights reserved. Designed with <i class="fas fa-heart"></i> using Python</p>
            </div>
        </div>
    </footer>

    <script>
        // Initialize Pyodide and run Python code
        async function initializePyodide() {
            const loader = document.querySelector('.loader');
            const loadingText = document.querySelector('.pyodide-loading p');
            loader.style.display = 'block';
            
            try {
                // Load Pyodide
                loadingText.textContent = "Downloading Pyodide runtime...";
                let pyodide = await loadPyodide({
                    indexURL: "https://cdn.jsdelivr.net/pyodide/v0.23.4/full/"
                });
                
                loadingText.textContent = "Installing Python packages...";
                await pyodide.loadPackage("micropip");
                
                loadingText.textContent = "Initializing ecommerce application...";
                const micropip = pyodide.pyimport("micropip");
                await micropip.install("jsonschema");
                
                // Run the Python ecommerce application code
                await pyodide.runPython(`
                    import js
                    import json
                    import random
                    from js import localStorage, document, console

                    # Product data model
                    class Product:
                        def __init__(self, id, name, price, category, image, rating, discount=0, stock=100):
                            self.id = id
                            self.name = name
                            self.price = price
                            self.category = category
                            self.image = image
                            self.rating = rating
                            self.discount = discount
                            self.stock = stock
                            self.discounted_price = round(price * (1 - discount/100), 2) if discount else price
                        
                        def to_dict(self):
                            return {
                                "id": self.id,
                                "name": self.name,
                                "price": self.price,
                                "discounted_price": self.discounted_price,
                                "discount": self.discount,
                                "category": self.category,
                                "image": self.image,
                                "rating": self.rating,
                                "stock": self.stock
                            }

                    # Shopping Cart
                    class Cart:
                        def __init__(self):
                            self.items = {}
                            self.load_from_storage()
                        
                        def add_item(self, product, quantity=1):
                            if product.id in self.items:
                                self.items[product.id]['quantity'] += quantity
                            else:
                                self.items[product.id] = {
                                    "product": product.to_dict(),
                                    "quantity": quantity
                                }
                            self.save_to_storage()
                            self.update_cart_display()
                        
                        def remove_item(self, product_id):
                            if product_id in self.items:
                                del self.items[product_id]
                                self.save_to_storage()
                                self.update_cart_display()
                        
                        def update_quantity(self, product_id, quantity):
                            if product_id in self.items:
                                if quantity > 0:
                                    self.items[product_id]['quantity'] = quantity
                                else:
                                    self.remove_item(product_id)
                                self.save_to_storage()
                                self.update_cart_display()
                        
                        def clear_cart(self):
                            self.items = {}
                            self.save_to_storage()
                            self.update_cart_display()
                        
                        def get_total(self):
                            total = 0
                            for item in self.items.values():
                                total += item['product']['discounted_price'] * item['quantity']
                            return total
                        
                        def get_item_count(self):
                            return sum(item['quantity'] for item in self.items.values())
                        
                        def save_to_storage(self):
                            localStorage.setItem("cart", json.dumps(self.items))
                        
                        def load_from_storage(self):
                            cart_data = localStorage.getItem("cart")
                            if cart_data:
                                self.items = json.loads(cart_data)
                        
                        def update_cart_display(self):
                            # Update cart count badge
                            document.getElementById("cart-count").innerText = str(self.get_item_count())
                            
                            # Update cart modal if open
                            if document.getElementById("cart-modal").style.display == "flex":
                                self.render_cart_items()

                        def render_cart_items(self):
                            cart_items_div = document.getElementById("cart-items")
                            cart_items_div.innerHTML = ""
                            
                            if not self.items:
                                cart_items_div.innerHTML = """
                                    <div class="text-center py-10">
                                        <i class="fas fa-shopping-cart" style="font-size: 48px; margin-bottom: 20px; opacity: 0.3;"></i>
                                        <h3>Your cart is empty</h3>
                                        <p>Start shopping to add items to your cart</p>
                                    </div>
                                """
                                return
                            
                            for item_id, item in self.items.items():
                                product = item['product']
                                quantity = item['quantity']
                                
                                cart_item = document.createElement("div")
                                cart_item.className = "cart-item"
                                cart_item.innerHTML = f"""
                                    <img src="{product['image']}" alt="{product['name']}" class="cart-item-img">
                                    <div class="cart-item-details">
                                        <h3 class="cart-item-title">{product['name']}</h3>
                                        <p class="cart-item-price">${product['discounted_price']:.2f} {f'<span style="text-decoration: line-through; color: #999; margin-left: 8px;">${product["price"]:.2f}</span>' if product['discount'] else ''}</p>
                                        <div class="cart-item-actions">
                                            <button class="quantity-btn minus" data-id="{product['id']}">-</button>
                                            <input type="number" class="quantity-input" value="{quantity}" min="1" data-id="{product['id']}">
                                            <button class="quantity-btn plus" data-id="{product['id']}">+</button>
                                            <button class="remove-item" data-id="{product['id']}"><i class="fas fa-trash"></i></button>
                                        </div>
                                    </div>
                                """
                                cart_items_div.appendChild(cart_item)
                            
                            # Add event listeners to cart controls
                            for btn in document.querySelectorAll(".quantity-btn.minus"):
                                btn.addEventListener("click", lambda e: self.update_quantity(e.target.dataset.id, self.items[e.target.dataset.id]['quantity'] - 1))
                            
                            for btn in document.querySelectorAll(".quantity-btn.plus"):
                                btn.addEventListener("click", lambda e: self.update_quantity(e.target.dataset.id, self.items[e.target.dataset.id]['quantity'] + 1))
                            
                            for input in document.querySelectorAll(".quantity-input"):
                                input.addEventListener("change", lambda e: self.update_quantity(e.target.dataset.id, int(e.target.value)))
                            
                            for btn in document.querySelectorAll(".remove-item"):
                                btn.addEventListener("click", lambda e: self.remove_item(e.target.dataset.id))
                            
                            # Update cart summary
                            subtotal = self.get_total()
                            shipping = 5.99 if subtotal < 50 else 0
                            tax = round(subtotal * 0.08, 2)
                            total = subtotal + shipping + tax
                            
                            document.getElementById("cart-subtotal").innerText = f"${subtotal:.2f}"
                            document.getElementById("cart-shipping").innerText = f"${shipping:.2f}" if shipping > 0 else "FREE"
                            document.getElementById("cart-tax").innerText = f"${tax:.2f}"
                            document.getElementById("cart-total").innerText = f"${total:.2f}"

                    # Sample product data
                    def generate_products():
                        products = []
                        
                        # Electronics
                        products.append(Product(1, "Wireless Bluetooth Headphones", 129.99, "Electronics", "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=600&h=400&q=80", 4.5, 15))
                        products.append(Product(2, "Smartphone X Pro", 899.99, "Electronics", "https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=600&h=400&q=80", 4.8))
                        products.append(Product(3, "4K Ultra HD Smart TV", 649.99, "Electronics", "https://images.unsplash.com/photo-1571415060716-baff5f717c37?auto=format&fit=crop&w=600&h=400&q=80", 4.6, 20))
                        products.append(Product(4, "Laptop Pro 2023", 1299.99, "Electronics", "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=600&h=400&q=80", 4.7))
                        
                        # Fashion
                        products.append(Product(5, "Men's Casual Shirt", 39.99, "Fashion", "https://images.unsplash.com/photo-1525507119028-ed4c629a60a3?auto=format&fit=crop&w=600&h=400&q=80", 4.3, 10))
                        products.append(Product(6, "Women's Summer Dress", 59.99, "Fashion", "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?auto=format&fit=crop&w=600&h=400&q=80", 4.5))
                        products.append(Product(7, "Running Shoes", 89.99, "Fashion", "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=600&h=400&q=80", 4.6, 25))
                        
                        # Home & Kitchen
                        products.append(Product(8, "Coffee Maker", 79.99, "Home", "https://images.unsplash.com/photo-1506619216599-9d16d0903dfd?auto=format&fit=crop&w=600&h=400&q=80", 4.4))
                        products.append(Product(9, "Air Fryer", 129.99, "Home", "https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?auto=format&fit=crop&w=600&h=400&q=80", 4.7, 15))
                        products.append(Product(10, "Blender Set", 49.99, "Home", "https://images.unsplash.com/photo-1560343090-f0409e92791a?auto=format&fit=crop&w=600&h=400&q=80", 4.2))
                        
                        # Books
                        products.append(Product(11, "Python Programming Book", 34.99, "Books", "https://images.unsplash.com/photo-1544947950-fa07a98d237f?auto=format&fit=crop&w=600&h=400&q=80", 4.9))
                        products.append(Product(12, "Best Science Fiction 2023", 19.99, "Books", "https://images.unsplash.com/photo-1495640388908-05fa85288e61?auto=format&fit=crop&w=600&h=400&q=80", 4.5, 10))
                        
                        return products

                    # Render product cards
                    def render_products(products, container_id):
                        container = document.getElementById(container_id)
                        container.innerHTML = ""
                        
                        for product in products:
                            card = document.createElement("div")
                            card.className = "product-card"
                            card.innerHTML = f"""
                                {f'<span class="product-badge">-{product.discount}%</span>' if product.discount else ''}
                                <img src="{product.image}" alt="{product.name}" class="product-img">
                                <div class="product-info">
                                    <h3 class="product-title">{product.name}</h3>
                                    <div class="product-price">
                                        {f'<span class="old-price">${product.price:.2f}</span>' if product.discount else ''}
                                        ${product.discounted_price:.2f}
                                    </div>
                                    <div class="product-rating">
                                        {'<i class="fas fa-star"></i>' * int(product.rating)}
                                        {'<i class="fas fa-star-half-alt"></i>' if product.rating % 1 >= 0.5 else ''}
                                        {'<i class="far fa-star"></i>' * (5 - int(product.rating) - (1 if product.rating % 1 >= 0.5 else 0))}
                                        <span class="ml-2">({product.rating})</span>
                                    </div>
                                    <div class="product-actions">
                                        <button class="action-btn add-to-cart" data-id="{product.id}">
                                            <i class="fas fa-shopping-cart"></i> Add to Cart
                                        </button>
                                        <button class="action-btn wishlist">
                                            <i class="fas fa-heart"></i>
                                        </button>
                                    </div>
                                </div>
                            """
                            container.appendChild(card)
                        
                        # Add event listeners to Add to Cart buttons
                        for btn in document.querySelectorAll(".add-to-cart"):
                            btn.addEventListener("click", lambda e: cart.add_item(next(p for p in all_products if p.id == int(e.target.dataset.id))))

                    # Render categories
                    def render_categories(categories):
                        container = document.getElementById("categories-container")
                        container.innerHTML = ""
                        
                        for category in categories:
                            card = document.createElement("div")
                            card.className = "category-card"
                            card.innerHTML = f"""
                                <i class="{category.icon}"></i>
                                <h3>{category.name}</h3>
                            """
                            container.appendChild(card)

                    # Initialize the application
                    all_products = generate_products()
                    cart = Cart()
                    
                    # Categories data
                    categories = [
                        {"name": "Electronics", "icon": "fas fa-mobile-alt"},
                        {"name": "Fashion", "icon": "fas fa-tshirt"},
                        {"name": "Home & Kitchen", "icon": "fas fa-home"},
                        {"name": "Books", "icon": "fas fa-book"},
                        {"name": "Sports", "icon": "fas fa-dumbbell"},
                        {"name": "Gaming", "icon": "fas fa-gamepad"}
                    ]
                    
                    # Render UI elements
                    render_categories(categories)
                    render_products(all_products[:8], "featured-products")
                    render_products(random.sample(all_products, 4) + [p for p in all_products if p.discount > 0][:4], "deals-products")
                    
                    # Update cart display
                    cart.update_cart_display()
                    
                    # Show UI sections
                    document.getElementById("categories-section").style.display = "block"
                    document.getElementById("featured-section").style.display = "block"
                    document.getElementById("deals-section").style.display = "block"
                    
                    # Hide loading indicator
                    document.getElementById("pyodide-loading").style.display = "none"

                    # Cart modal functionality
                    def open_cart():
                        document.getElementById("cart-modal").style.display = "flex"
                        cart.render_cart_items()

                    def close_cart():
                        document.getElementById("cart-modal").style.display = "none"

                    # Add event listeners
                    document.getElementById("cart-icon").addEventListener("click", open_cart)
                    document.querySelector(".close-modal").addEventListener("click", close_cart)

                    # Close modal when clicking outside
                    document.getElementById("cart-modal").addEventListener("click", lambda e: close_cart() if e.target == document.getElementById("cart-modal") else None)

                    # Search functionality
                    def search_products():
                        query = document.getElementById("search-input").value.lower()
                        if not query:
                            # Reset to default view if search is empty
                            render_products(all_products[:8], "featured-products")
                            render_products(random.sample(all_products, 4) + [p for p in all_products if p.discount > 0][:4], "deals-products")
                            document.querySelector("#featured-section .section-title").innerText = "Featured Products"
                            return
                        
                        # Filter products by name or category
                        results = [p for p in all_products 
                                  if query in p.name.lower() or query in p.category.lower()]
                        
                        # Clear featured and deals sections
                        document.getElementById("featured-products").innerHTML = ""
                        document.getElementById("deals-products").innerHTML = ""
                        
                        # Render search results in featured section
                        render_products(results, "featured-products")
                        
                        # Update section title
                        document.querySelector("#featured-section .section-title").innerText = f"Search Results for '{query}'"

                    document.getElementById("search-btn").addEventListener("click", search_products)
                    document.getElementById("search-input").addEventListener("keypress", lambda e: search_products() if e.key == "Enter" else None)
                `);
                
                // Hide loading indicator
                document.getElementById('pyodide-loading').style.display = 'none';
            } catch (error) {
                console.error("Error initializing Pyodide:", error);
                loadingText.textContent = "Error loading application. Please refresh the page.";
                loader.style.display = 'none';
            }
        }

        // Start the Pyodide initialization
        initializePyodide();
    </script>
</body>
</html>
