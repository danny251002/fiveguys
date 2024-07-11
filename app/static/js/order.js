// app/static/js/order.js

document.addEventListener("DOMContentLoaded", function () {
  const orderForm = document.getElementById("order-form");
  const cartItems = document.getElementById("cart-items");
  const cartTotal = document.getElementById("cart-total");
  let total = 0;

  orderForm.addEventListener("change", function (e) {
    if (e.target.type === "number" || e.target.type === "checkbox") {
      updateCart();
    }
  });

  function updateCart() {
    cartItems.innerHTML = "";
    total = 0;

    const inputs = orderForm.querySelectorAll('input[type="number"]');
    inputs.forEach((input) => {
      const quantity = parseInt(input.value);
      if (quantity > 0) {
        const menuItem = input.closest(".menu-item");
        const itemName = menuItem.querySelector("h3").textContent;
        const itemPrice = parseFloat(input.dataset.price);
        let subtotal = quantity * itemPrice;

        const customizations = [];
        const customizationOptions = menuItem.querySelectorAll(
          '.customization-options input[type="checkbox"]:checked'
        );
        customizationOptions.forEach((option) => {
          const optionName = option.nextElementSibling.textContent
            .split("(")[0]
            .trim();
          const optionPrice = parseFloat(
            option.nextElementSibling.textContent.match(/\$(\d+\.\d+)/)[1]
          );
          customizations.push(optionName);
          subtotal += quantity * optionPrice;
        });

        const li = document.createElement("li");
        li.textContent = `${quantity}x ${itemName}${
          customizations.length ? " (" + customizations.join(", ") + ")" : ""
        } - $${subtotal.toFixed(2)}`;
        cartItems.appendChild(li);

        total += subtotal;
      }
    });

    cartTotal.textContent = total.toFixed(2);
  }
});
