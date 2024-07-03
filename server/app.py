#!/usr/bin/env python3
from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET/POST/PATCH/DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries_list = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(bakeries_list, 200)

@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()

    if request.method == 'GET':
        return make_response(bakery.to_dict(), 200)
    
    elif request.method == 'PATCH':
        for attr in request.form:
            setattr(bakery, attr, request.form.get(attr))
        
        db.session.add(bakery)
        db.session.commit()

        return make_response(bakery.to_dict(), 200)

@app.route('/baked_goods', methods=['GET', 'POST'])
def baked_goods():
    if request.method == 'GET':
        baked_goods_list = [bg.to_dict() for bg in BakedGood.query.all()]
        return make_response(baked_goods_list, 200)

    elif request.method == 'POST':
        new_baked_good = BakedGood(
            name=request.form.get("name"),
            price=request.form.get("price"),
            bakery_id=request.form.get("bakery_id")
        )

        db.session.add(new_baked_good)
        db.session.commit()

        return make_response(new_baked_good.to_dict(), 201)

@app.route('/baked_goods/<int:id>', methods=['GET', 'DELETE'])
def baked_goods_by_id(id):
    baked_good = BakedGood.query.filter_by(id=id).first()

    if request.method == 'GET':
        return make_response(baked_good.to_dict(), 200)

    elif request.method == 'DELETE':
        db.session.delete(baked_good)
        db.session.commit()
        return make_response({'message': 'Record Deleted Successfully'}, 200)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    sorted_baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    serialized_baked_goods = [bg.to_dict() for bg in sorted_baked_goods]
    return make_response(serialized_baked_goods, 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    return make_response(most_expensive.to_dict(), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
