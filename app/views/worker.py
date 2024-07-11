from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.order import Order
from app import db

bp = Blueprint('worker', __name__, url_prefix='/worker')

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'worker':
        flash('Access denied. Worker privileges required.')
        return redirect(url_for('main.home'))
    return render_template('worker/dashboard.html')

@bp.route('/orders')
@login_required
def orders():
    if current_user.role != 'worker':
        flash('Access denied. Worker privileges required.')
        return redirect(url_for('main.home'))
    
    pending_orders = Order.query.filter_by(status='pending').order_by(Order.created_at.desc()).all()
    return render_template('worker/orders.html', orders=pending_orders)

@bp.route('/completed_orders')
@login_required
def completed_orders():
    if current_user.role != 'worker':
        flash('Access denied. Worker privileges required.')
        return redirect(url_for('main.home'))
    
    completed_orders = Order.query.filter_by(status='completed').order_by(Order.created_at.desc()).all()
    return render_template('worker/completed_orders.html', orders=completed_orders)

@bp.route('/complete_order/<int:order_id>', methods=['POST'])
@login_required
def complete_order(order_id):
    if current_user.role != 'worker':
        flash('Access denied. Worker privileges required.')
        return redirect(url_for('main.home'))

    order = Order.query.get_or_404(order_id)
    if order.status == 'pending':
        order.status = 'completed'
        db.session.commit()
        flash('Order marked as completed.')
    else:
        flash('This order has already been completed.')
    return redirect(url_for('worker.orders'))