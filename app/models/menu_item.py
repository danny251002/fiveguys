# app/models/menu_item.py

from app import db

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(200))
    is_customizable = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<MenuItem {self.name}>'

class CustomizationOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    menu_item = db.relationship('MenuItem', backref=db.backref('customization_options', lazy=True))

    def __repr__(self):
        return f'<CustomizationOption {self.name}>'