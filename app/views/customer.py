from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.order import Order, OrderItem, CartItem
from app.models.menu_item import MenuItem
from app import db

bp = Blueprint('customer', __name__, url_prefix='/customer')

@bp.route('/menu')
def menu():
    menu_items = MenuItem.query.all()
    categorized_items = {}
    for item in menu_items:
        if item.category not in categorized_items:
            categorized_items[item.category] = []
        categorized_items[item.category].append(item)
    return render_template('customer/menu.html', categorized_items=categorized_items)

@bp.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    menu_item_id = request.form.get('menu_item_id')
    quantity = int(request.form.get('quantity', 1))
    
    cart_item = CartItem.query.filter_by(user_id=current_user.id, menu_item_id=menu_item_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=current_user.id, menu_item_id=menu_item_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    flash('Item added to cart.')
    return redirect(url_for('customer.menu'))

@bp.route('/cart')
@login_required
def view_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.menu_item.price * item.quantity for item in cart_items)
    return render_template('customer/cart.html', cart_items=cart_items, total=total)

@bp.route('/remove_from_cart/<int:cart_item_id>')
@login_required
def remove_from_cart(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)
    if cart_item.user_id != current_user.id:
        flash('You do not have permission to remove this item.')
        return redirect(url_for('customer.view_cart'))
    
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart.')
    return redirect(url_for('customer.view_cart'))

@bp.route('/place_order', methods=['POST'])
@login_required
def place_order():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Your cart is empty.')
        return redirect(url_for('customer.menu'))
    
    order = Order(user_id=current_user.id, status='pending', total_price=0)
    db.session.add(order)
    
    total_price = 0
    for cart_item in cart_items:
        order_item = OrderItem(
            order=order,
            menu_item_id=cart_item.menu_item_id,
            quantity=cart_item.quantity,
            subtotal=cart_item.menu_item.price * cart_item.quantity
        )
        db.session.add(order_item)
        total_price += order_item.subtotal
    
    order.total_price = total_price
    db.session.commit()
    
    # Clear the cart
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    
    flash('Your order has been placed successfully!')
    return redirect(url_for('customer.order_history'))

@bp.route('/order_history')
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('customer/order_history.html', orders=orders)

@bp.route('/cancel_order/<int:order_id>')
@login_required
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('You do not have permission to cancel this order.')
        return redirect(url_for('customer.order_history'))
    
    if order.status != 'pending':
        flash('Only pending orders can be cancelled.')
        return redirect(url_for('customer.order_history'))
    
    order.status = 'cancelled'
    db.session.commit()
    flash('Your order has been cancelled.')
    return redirect(url_for('customer.order_history'))