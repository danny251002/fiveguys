from app import create_app, db
from app.models.menu_item import MenuItem

app = create_app()

def add_menu_items():
    with app.app_context():
        # Check if items already exist
        if MenuItem.query.count() > 0:
            print("Menu items already exist. Skipping...")
            return

        new_items = [
            MenuItem(
                name="Creamy Milkshake",
                description="Rich and creamy milkshake made with premium ice cream",
                price=4.99,
                category="Drink",
                image_url="milkshake.jpg"
            ),
            MenuItem(
                name="Crispy Onion Rings",
                description="Golden-brown onion rings with a crunchy batter",
                price=3.99,
                category="Side",
                image_url="onion-rings.jpg"
            ),
            MenuItem(
                name="Deluxe Pasta",
                description="Al dente pasta with a savory sauce and fresh herbs",
                price=12.99,
                category="Main",
                image_url="pasta.jpg"
            ),
            MenuItem(
                name="Gourmet Pizza",
                description="Thin-crust pizza with premium toppings and melted cheese",
                price=14.99,
                category="Main",
                image_url="pizza.jpg"
            ),
            MenuItem(
                name="Best Burger",
                description="Angus Beef burger with our SECRET souce",
                price=10.99,
                category="Main",
                image_url="burger.jpeg"
            )
        ]

        db.session.add_all(new_items)
        db.session.commit()
        print("New menu items added successfully!")

if __name__ == "__main__":
    add_menu_items()