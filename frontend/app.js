const API_URL = "http://localhost:8000";


async function loadProducts() {

    const response = await fetch(
        `${API_URL}/api/v1/products`
    );

    const products =
        await response.json();

    const container =
        document.getElementById(
            "products"
        );

    container.innerHTML = "";

    products.forEach(product => {

        const div =
            document.createElement(
                "div"
            );

        div.className = "card";

        div.innerHTML = `
            <h3>${product.name}</h3>

            <p>
                ₹${product.price}
            </p>

            <button
                onclick="createOrder(${product.id})"
            >
                Buy
            </button>
        `;

        container.appendChild(div);
    });
}


async function createOrder(productId) {

    const response = await fetch(
        `${API_URL}/api/v1/orders`,
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({
                product_id: productId,
                quantity: 1
            })
        }
    );

    const result =
        await response.json();

    alert(
        `Order ${result.order.id} created`
    );

    loadOrders();
}


async function loadOrders() {

    const response = await fetch(
        `${API_URL}/api/v1/orders`
    );

    const orders =
        await response.json();

    const container =
        document.getElementById(
            "orders"
        );

    container.innerHTML = "";

    orders.forEach(order => {

        const div =
            document.createElement(
                "div"
            );

        div.className = "card";

        div.innerHTML = `
            <strong>
                Order ${order.id}
            </strong>

            <p>
                Product:
                ${order.product_id}
            </p>

            <p>
                Quantity:
                ${order.quantity}
            </p>

            <p>
                Total:
                ₹${order.total_price}
            </p>

            <p>
                Status:
                ${order.status}
            </p>
        `;

        container.appendChild(div);
    });
}


loadProducts();
loadOrders();
