from app import app
from flask import render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from models import Customers, db
from itsdangerous import SignatureExpired, URLSafeTimedSerializer
from config import ser_key

mail = Mail(app)

serializer = URLSafeTimedSerializer(ser_key)


@app.route('/')
def index():
    return render_template('shop/index.html')


@app.route('/bra-list')
def bra_list():
    return render_template('shop/bra_list.html')


@app.route('/sets-list')
def sets_list():
    return render_template('shop/set_list.html')


@app.route('/panties-list')
def panties_list():
    return render_template('shop/panties_list.html')


@app.route('/send_email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        email = request.form['email']
        customer_check = Customers.query.filter_by(email=email).first()
        if customer_check:
            flash('Korisnik vec postoji')
            return redirect(url_for('index'))

        customer = Customers(email=email)
        db.session.add(customer)
        db.session.commit()

        token = serializer.dumps(email, salt=ser_key)
        msg = Message('Potvrda email adrese', recipients=[email])
        link = url_for('confirm_email', token=token, _external=True)
        msg.body = f'Molimo Vas da kliknete na link da bi potvrdili Vasu email adresu, {link}\nLink je validan 24 sata.'
        mail.send(msg)
        flash('Molimo Vas provjerite vas email inbox')

        return redirect(url_for('index'))


@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = serializer.loads(token, salt=ser_key, max_age=100)

    except SignatureExpired:
        flash('Vas link je istekao, molimo Vas da pokusate ponovo sa registracijom')
        return redirect(url_for('index'))

    customer = Customers.query.filter_by(email=email).first()
    customer.confirmed = True
    db.session.commit()

    msg = Message('Ostvarili ste pravo na popust', recipients=[email])
    msg.body = 'Postovani,\nMolimo vas da se javite na kasu prilikom Vase sledece kupovnine u nasem butiku.' \
               'Sve sto vam je potrebno  da bi ostavrili popust je Vasa email adresa.'
    mail.send(msg)

    flash('Uspjesno ste potvrdili Vas email, stici ce Vam email sa upustvima za popust')
    return redirect(url_for('index'))