// ShopX Cart Logic
let cart = JSON.parse(localStorage.getItem('shopx_cart')) || [];
const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

function updateCartCount() {
    const countElement = document.getElementById('cart-count');
    if (countElement) {
        countElement.textContent = cart.length;
    }
}

function addToCart(productId, name, price, image) {
    const item = { id: productId, name, price, image };
    cart.push(item);
    localStorage.setItem('shopx_cart', JSON.stringify(cart));
    updateCartCount();
    
    // Notification
    showNotification(`${name} added to cart!`);
}

function removeFromCart(index) {
    cart.splice(index, 1);
    localStorage.setItem('shopx_cart', JSON.stringify(cart));
    renderCart();
    updateCartCount();
}

function renderCart() {
    const cartItemsContainer = document.getElementById('cart-items');
    const totalElement = document.getElementById('cart-total');
    
    if (!cartItemsContainer) return;

    if (cart.length === 0) {
        cartItemsContainer.innerHTML = '<p style="text-align:center; padding: 2rem;">Your cart is empty.</p>';
        totalElement.textContent = '$0.00';
        return;
    }

    cartItemsContainer.innerHTML = '';
    let total = 0;

    cart.forEach((item, index) => {
        total += item.price;
        const itemElement = document.createElement('div');
        itemElement.className = 'cart-item glass';
        itemElement.innerHTML = `
            <img src="${item.image}" alt="${item.name}">
            <div class="cart-item-details">
                <h3>${item.name}</h3>
                <p class="price">₦${item.price.toLocaleString()}</p>
            </div>
            <span class="remove-btn" onclick="removeFromCart(${index})">Remove</span>
        `;
        cartItemsContainer.appendChild(itemElement);
    });

    totalElement.textContent = `₦${total.toLocaleString()}`;
}

function showNotification(message) {
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: #58a6ff;
        color: white;
        padding: 1rem 2rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        z-index: 2000;
        animation: slideIn 0.3s ease-out;
    `;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function payWithPaystack() {
    if (cart.length === 0) {
        showNotification("Your cart is empty!");
        return;
    }

    // Capture shipping info from the DOM
    const phone = document.getElementById('checkout-phone')?.value;
    const address = document.getElementById('checkout-address')?.value;
    const city = document.getElementById('checkout-city')?.value;

    if (!phone || !address || !city) {
        showNotification("Please fill all shipping details!");
        return;
    }

    let total = cart.reduce((sum, item) => sum + item.price, 0);
    
    // Optional: Save shipping details to backend via fetch before opening Paystack
    fetch('/checkout_details', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken || ''
        },
        body: `phone=${encodeURIComponent(phone)}&address=${encodeURIComponent(address)}&city=${encodeURIComponent(city)}`
    });

    let handler = PaystackPop.setup({
        key: window.SHOPX_PAYSTACK_KEY,
        email: window.SHOPX_MERCHANT_EMAIL,
        amount: total * 100, // Amount is in Kobo
        currency: 'NGN',
        metadata: {
            custom_fields: [
                { display_name: "Phone Number", variable_name: "phone", value: phone },
                { display_name: "Address", variable_name: "address", value: address },
                { display_name: "City", variable_name: "city", value: city }
            ]
        },
        ref: 'SHOPX_' + Math.floor((Math.random() * 1000000000) + 1),
        onClose: function() {
            showNotification('Window closed.');
        },
        callback: function(response) {
            showNotification('Payment successful! Reference: ' + response.reference);
            // Clear cart on success
            cart = [];
            localStorage.setItem('shopx_cart', JSON.stringify(cart));
            renderCart();
            updateCartCount();
            
            setTimeout(() => {
                window.location.href = '/';
            }, 2000);
        }
    });

    handler.openIframe();
}

// Add animations to CSS dynamically or just assume they exist
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
    @keyframes slideOut { from { transform: translateX(0); opacity: 1; } to { transform: translateX(100%); opacity: 0; } }
`;
document.head.appendChild(style);

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    updateCartCount();
    renderCart();
});
