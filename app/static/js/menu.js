document.addEventListener("DOMContentLoaded", function () {
  const addToCartButtons = document.querySelectorAll(".add-to-cart");

  addToCartButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const itemId = this.getAttribute("data-id");
      addToCart(itemId);
    });
  });

  function addToCart(itemId) {
    console.log(`Item ${itemId} added to cart`);
    // TODO: Implement actual cart functionality
    alert("Item added to cart!");
  }
});
