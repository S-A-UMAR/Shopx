# ShopX - Premium Shoe E-commerce Platform

ShopX is a modern, high-performance web application designed for selling premium footwear. Built with Flask, it features a sleek dark-mode aesthetic, glassmorphic UI elements, and a seamless shopping experience.

## 🚀 Features

- **Dynamic Product Showcasing**: High-resolution sneaker imagery with interactive hover effects and animations.
- **Persistent Shopping Cart**: A client-side cart system powered by `LocalStorage` that retains items even after page refreshes.
- **Glassmorphic Design**: A premium UI utilizing modern CSS techniques like `backdrop-filter`, HSL color systems, and smooth transitions.
- **Multi-Route Navigation**: 
  - **Home**: Featured arrivals and hero promotions.
  - **Shop**: Full catalog with "Add to Cart" functionality.
  - **About**: Brand storytelling and mission statement.
  - **Contact**: Interactive contact form with real-time feedback.
  - **Cart**: Dynamic item management and checkout flow.
- **Responsive Layout**: Optimized for both desktop and mobile viewing.

## 🛠️ Technology Stack

- **Backend**: Python 3 & Flask
- **Frontend**: HTML5, CSS3 (Custom Design System), JavaScript (ES6)
- **Icons**: Phosphor Icons
- **Typography**: Outfit (Google Fonts)
- **Imagery**: Custom AI-generated high-fidelity shoe models.

## 📁 Project Structure

```text
shopx/
├── app.py              # Main Flask application logic
├── static/             # Static assets
│   ├── css/            # Custom stylesheets
│   ├── js/             # Cart and UI logic
│   └── img/            # High-res shoe images
└── templates/          # Jinja2 HTML templates
    ├── base.html       # Shared layout (Navbar/Footer)
    ├── index.html      # Homepage
    ├── products.html   # Product listing
    ├── cart.html       # Shopping cart
    ├── about.html      # Brand story
    └── contact.html    # Contact form
```

## 🏃 How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables** (copy `.env.example`):
   ```bash
   cp .env.example .env
   ```

   At minimum, set `SECRET_KEY`. For local development, default SQLite works if `DATABASE_URL` is left as-is.

3. **Start the Application**:
   ```bash
   python app.py
   ```

4. **Access the Website**:
   Open your browser and navigate to `http://127.0.0.1:5000`

## 📝 Implementation Details

- **Cart Logic**: The shopping cart is handled on the client-side to ensure maximum performance and responsiveness. Data is stored in the browser's `localStorage`.
- **Styling**: The design uses a custom CSS variable system for easy theming (Dark mode by default).
- **Security**: Flask is configured in Debug mode for development, providing detailed error messages and hot-reloading.

---
*Created by ShopX Development Team - 2026*
