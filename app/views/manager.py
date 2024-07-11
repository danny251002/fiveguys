# app/views/manager.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.menu_item import MenuItem
from app import db

bp = Blueprint('manager', __name__, url_prefix='/manager')

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'manager':
        flash('Access denied. Manager privileges required.')
        return redirect(url_for('home'))
    return render_template('manager/dashboard.html')

@bp.route('/menu', methods=['GET', 'POST'])
@login_required
def menu():
    if current_user.role != 'manager':
        flash('Access denied. Manager privileges required.')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        category = request.form['category']
        image_url = request.form['image_url']

        new_item = MenuItem(name=name, description=description, price=price, category=category, image_url=image_url)
        db.session.add(new_item)
        db.session.commit()
        flash('New menu item added successfully.')
        return redirect(url_for('manager.menu'))

    menu_items = MenuItem.query.all()
    return render_template('manager/menu.html', menu_items=menu_items)

@bp.route('/menu/delete/<int:id>', methods=['POST'])
@login_required
def delete_menu_item(id):
    if current_user.role != 'manager':
        flash('Access denied. Manager privileges required.')
        return redirect(url_for('home'))

    item = MenuItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Menu item deleted successfully.')
    return redirect(url_for('manager.menu'))