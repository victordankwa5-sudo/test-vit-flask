from flask import Blueprint, render_template, redirect, url_for, request, flash, send_from_directory
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from .models import Product, Order, Settings, Brands
from . import db

admin = Blueprint('admin', __name__)

@admin.route('/media/<path:filename>')
def get_image(filename):
    return send_from_directory('../media', filename)

@admin.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.id == 1:
        num_orders = Order.query.order_by('id').all()
        total_orders = len(num_orders)
        brands = Brands.query.order_by(Brands.name).all()
        
        if request.method == 'POST':
            
            productName = request.form.get('product-name')
            previousPrice = request.form.get('previous-price')
            currentPrice = request.form.get('current-price')
            inStock = request.form.get('product-stock')
            productCategory = request.form.get('product-category')
            productBrand = request.form.get('product-brand')
            productDescription = request.form.get('product-des')
            isFlashSale = request.form.get('flash-sale')
            if isFlashSale == 'on':
                isFlashSale = True
            else:
                isFlashSale = False
            
            imageFile = request.files.get('image-file')
            fileName = secure_filename(imageFile.filename)
            filePath = f'./media/{fileName}'
            imageFile.save(filePath)
            
            imageFile2 = request.files.get('image-file-2')
            fileName2 = secure_filename(imageFile2.filename)
            filePath2 = f'./media/{fileName2}'
            imageFile2.save(filePath2)
            
            imageFile3 = request.files.get('image-file-3')
            fileName3 = secure_filename(imageFile3.filename)
            filePath3 = f'./media/{fileName3}'
            imageFile3.save(filePath3)
            
            new_product = Product()
            new_product.name = productName
            new_product.previous_price = previousPrice
            new_product.current_price = currentPrice
            new_product.stock = inStock
            new_product.category = productCategory
            new_product.brand = productBrand
            new_product.description = productDescription
            new_product.flash_sale = isFlashSale
            new_product.image = filePath
            new_product.image2 = filePath2
            new_product.image3 = filePath3
            
            db.session.add(new_product)
            db.session.commit()
            
            flash('Product added', 'success')
            return redirect(url_for('admin_views.admin_products'))
        return render_template('admin-add-product.html', user=current_user, total_orders=total_orders, brands=brands)
    else:
        flash('You are not an admin!', 'error')

@admin.route('update-product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def update_product(product_id):
    if current_user.id == 1:
        num_orders = Order.query.order_by('id').all()
        total_orders = len(num_orders)
        
        product = Product.query.filter_by(id=product_id).first()

        if request.method == 'POST':
            productName = request.form.get('product-name')
            previous_price = request.form.get('previous-price')
            current_price = request.form.get('current-price')
            stock = request.form.get('product-stock')
            category = request.form.get('product-category')
            description = request.form.get('product-des')
            flash_sale = request.form.get('flash-sale')
            print(flash_sale)
            if flash_sale == 'on':
                flash_sale = True
            else:
                flash_sale = False
            
            imageFile = request.files.get('image-file')
            
            filename = secure_filename(imageFile.filename)
            filepath = f'./media/{filename}'
            
            imageFile.save(filepath)
            
            try:
                Product.query.filter_by(id=product_id).update(dict(
                                                                name=productName,
                                                                previous_price=previous_price,
                                                                current_price=current_price,
                                                                stock=stock,
                                                                flash_sale=flash_sale,
                                                                category=category,
                                                                image=filepath,
                                                                description=description
                                                                ))
                db.session.commit()
                flash('Product updated', 'success')
                return redirect(url_for('admin.add_product'))
            except Exception as e:
                flash('Could not update product', 'error')
                return redirect(url_for('admin.add_product'))
            
        
        return render_template('admin-update-product.html', user=current_user, product=product, total_orders=total_orders)
    else:
        return flash("You are not an admin!", 'error')

@admin.route('delete-product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def delete_product(product_id):
    if current_user.id == 1:
        try:
            product_to_delete = Product.query.get(product_id)
            db.session.delete(product_to_delete)
            db.session.commit()
            flash('Product deleted', 'success')
            return redirect(url_for('admin.add_product'))
        except Exception as e:
            flash('Item could not be deleted', 'error')
        return redirect(url_for('admin.add_product'))
    else:
        flash('You are not an admin!', 'error')
        
@admin.route('/update-order-status/<int:order_id>', methods=['GET', 'POST'])
@login_required
def update_order(order_id):
    if current_user.id == 1:
        num_orders = Order.query.order_by('id').all()
        total_orders = len(num_orders)
        
        if request.method == 'POST':
            new_order_status = request.form.get('new-order-status')
            
            try:
                Order.query.filter_by(id=order_id).update(dict(status=new_order_status))
                db.session.commit()
                flash('Order status updated', 'success')
                return redirect(url_for('admin_views.orders'))
            except Exception as e:
                flash('Could not update order status', 'error')
                return redirect(url_for('admin_views.orders'))
        
        return render_template('admin-update-order.html', user=current_user, total_orders=total_orders)
        
    else:
        flash('You are not an admin', 'error')

@admin.route('/admin-settings', methods=['GET', 'POST'])
@login_required
def settings():
    if current_user.id == 1:
        num_orders = Order.query.order_by('id').all()
        total_orders = len(num_orders)
        
        settings = Settings.query.filter_by(id=1).first()
        
        if request.method == 'POST':
            store_name = request.form.get('store-name')
            store_email = request.form.get('store-email')
            currency = request.form.get('currency')

            try:
                Settings.query.filter_by(id=1).update(dict(
                    store_name=store_name,
                    store_email=store_email,
                    currency=currency
                ))
                db.session.commit()
                flash('Store settings updated', 'success')
                
                return redirect(request.referrer)
            except Exception as e:
                flash('Failed to update store settings', 'error')
            
        
        return render_template('admin-settings.html', user=current_user, total_orders=total_orders, settings=settings)
    else:
        return flash('You are not an admin!', 'error')

@admin.route('/add-brand', methods=['GET', 'POST'])
@login_required
def add_brand():
    if current_user.id == 1:
        num_orders = Order.query.order_by(Order.id).all()
        total_orders = len(num_orders)
        if request.method == 'POST':
            
            brand_name = request.form.get('brand-name')
            
            new_brand = Brands()
            
            new_brand.name = brand_name
            
            db.session.add(new_brand)
            db.session.commit()
            
            flash('Brand added', 'success')
            return redirect(url_for('admin_views.admin_brands'))
        
        return render_template('admin-add-brand.html', user=current_user, total_orders=total_orders)
    else:
        flash('You are not an admin!', 'error')

@admin.route('/delete-brand/<int:brand_id>')
@login_required
def delete_brand(brand_id):
    if current_user.id == 1:
        brand_to_delete = Brands.query.get(brand_id)
        
        try:
            db.session.delete(brand_to_delete)
            db.session.commit()
            flash('Brand deleted', 'success')
            return redirect(url_for('admin_views.admin_brands'))
        except Exception as e:
            flash('Could not delete brand from brands', 'error')
            return redirect(url_for('admin_views.admin_brands'))
    else:
        flash('You are not an admin', 'error')