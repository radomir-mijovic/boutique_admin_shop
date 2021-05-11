from app import app
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required
from models import db, Items, Customers
from sqlalchemy import func


@app.route('/admin')
@login_required
def admin():
    name = 'SVI ARTIKLI'
    bra_info = 'Ukupno bruseva u radnji'
    pant_info = 'Ukupno gacica u radnji'
    set_info = 'Ukupno kompleta u radnji'
    items = Items.query.all()

    count_bra = db.session.query(func.sum(Items.quantity)
                                 ).filter(Items.category.contains('brus')).all()
    list_bra = [a[0] for a in count_bra]
    bra_num = list_bra[0]

    count_set = db.session.query(func.sum(Items.quantity)
                                 ).filter(Items.category.contains('kompl')).all()
    list_set = [a[0] for a in count_set]
    set_num = list_set[0]

    count_pant = db.session.query(func.sum(Items.quantity)
                                  ).filter(Items.category.contains('gaci')).all()
    list_pant = [a[0] for a in count_pant]
    pant_num = list_pant[0]

    return render_template('admin/admin.html',
                           items=items, name=name,
                           bra_num=bra_num, set_num=set_num,
                           pant_num=pant_num, bra_info=bra_info,
                           pant_info=pant_info, set_info=set_info)


@app.route('/admin/customers')
@login_required
def customers():
    customer = Customers.query.all()
    return render_template('admin/admin_customers.html', customer=customer)


@app.route('/admin/delete_customer/<int:pk>', methods=['POST'])
@login_required
def delete_customer(pk):
    if request.method == 'POST':
        customer = Customers.query.get(pk)
        db.session.delete(customer)
        db.session.commit()
        return redirect(url_for('customers'))


@app.route('/admin/check_discount/<int:pk>', methods=['POST'])
@login_required
def check_discount(pk):
    if request.method == 'POST':
        customer = Customers.query.get(pk)
        customer.discount = True
        db.session.commit()
        return redirect(url_for('customers'))


@app.route('/admin/uncheck_discount/<int:pk>', methods=['POST'])
@login_required
def uncheck_discount(pk):
    if request.method == 'POST':
        customer = Customers.query.get(pk)
        customer.discount = False
        db.session.commit()
        return redirect(url_for('customers'))


@app.route('/admin/bra-list')
@login_required
def admin_bra_list():

    name = 'BRUSEVI'
    items = Items.query.filter(Items.category.contains('brus'))
    return render_template('admin/admin.html',
                           name=name, items=items)


@app.route('/admin/set-list')
@login_required
def admin_set_list():

    name = 'KOMPLETI'
    items = Items.query.filter(Items.category.contains('komple'))
    return render_template('admin/admin.html',
                           name=name, items=items)


@app.route('/admin/panties-list')
@login_required
def admin_panties_list():

    name = 'GACICE'
    items = Items.query.filter(Items.category.contains('gaci'))
    return render_template('admin/admin.html',
                           name=name, items=items)


@app.route('/admin/t-shirt-list')
@login_required
def admin_shirt_list():

    name = 'MAJICE'
    items = Items.query.filter(Items.category.contains('majic'))
    return render_template('admin/admin.html',
                           name=name, items=items)


@app.route('/admin/socks-list')
@login_required
def admin_socks_list():

    name = 'CARAPE'
    items = Items.query.filter(Items.category.contains('carap'))
    return render_template('admin/admin.html',
                           name=name, items=items)


@app.route('/add_item', methods=['GET', 'POST'])
@login_required
def add_item():
    if request.method == 'POST':
        category = request.form['category']
        name = request.form['name']
        item_num = request.form['item_num']
        size = request.form['size']
        quantity = request.form['quantity']

        item = Items(category=category, name=name, item_num=item_num,
                     size=size, quantity=quantity)

        db.session.add(item)
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('admin/admin.html')


@app.route('/delete/<int:pk>')
@login_required
def delete(pk):
    item = Items.query.get(pk)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('admin'))


@app.route('/update/<int:pk>', methods=['POST', 'GET'])
@login_required
def update(pk):
    item = Items.query.get(pk)
    if request.method == 'POST':
        item.category = request.form['category']
        item.name = request.form['name']
        item.item_num = request.form['item_num']
        item.size = request.form['size']
        item.quantity = request.form['quantity']
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('admin/admin.html', item=item)


@app.route('/search_num', methods=['POST'])
@login_required
def search_num():
    if request.method == 'POST':
        num = request.form['search']
        if num is None:
            flash('Artikal nije pronađen')
            return redirect(url_for('admin'))

        items = Items.query.filter(Items.item_num.startswith(num)).all()
        return render_template('admin/admin.html', items=items)


@app.route('/search_name', methods=['POST'])
@login_required
def search_name():
    if request.method == 'POST':
        search_name = request.form.get('search_name')

        items = Items.query.filter(Items.name.contains(search_name)).all()

        count_bra = db.session.query(func.sum(Items.quantity)
                                     ).filter(Items.name.contains(search_name),
                                              Items.category.contains('brus')
                                              ).all()
        bra_tuple = [a[0] for a in count_bra]
        bra_num = bra_tuple[0]

        count_pant = db.session.query(func.sum(Items.quantity)
                                      ).filter(Items.name.contains(search_name),
                                               Items.category.contains('gaci')
                                               ).all()
        pant_tuple = [a[0] for a in count_pant]
        pant_num = pant_tuple[0]

        count_set = db.session.query(func.sum(Items.quantity)
                                     ).filter(Items.name.contains(search_name),
                                              Items.category.contains('kompl')
                                              ).all()
        set_tuple = [a[0] for a in count_set]
        set_num = set_tuple[0]

        bra_info = 'Bruseva u radnji'
        pant_info = 'Gacica u radnji'
        set_info = 'Kompleta u radnji'
        return render_template('admin/admin.html', items=items,
                               bra_num=bra_num, bra_info=bra_info,
                               pant_num=pant_num, pant_info=pant_info,
                               set_info=set_info, set_num=set_num)
