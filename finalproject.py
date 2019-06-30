from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant)
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == "POST":
        restaurantName = request.form['name']
        addRestaurant = Restaurant(name = restaurantName)
        session.add(addRestaurant)
        session.commit()
        flash("New restaurant created.")
        return redirect(url_for('showRestaurants'))
    return render_template('newRestaurant.html')


@app.route('/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurants(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == "POST":
        restaurant.name = request.form['name']
        session.commit()
        flash("Restaurant information edited.")
        return redirect(url_for('showRestaurants'))
    return render_template('editRestaurant.html', restaurant = restaurant)
    

@app.route('/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurants(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == "POST":
        session.delete(restaurant)
        session.commit()
        flash("Restaurant deleted.")
        return redirect(url_for('showRestaurants'))
    return render_template('deleteRestaurant.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return render_template('menu.html', restaurant = restaurant, items = items)

@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'], description=request.form['description'], 
            price=request.form['price'], course=request.form['course'],
            restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New menu item created.")
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    return render_template('newMenuItem.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['price']:
            item.price =request.form['price']
        if request.form['course']:
            item.course=request.form['course']
        session.add(item)
        session.commit()
        flash("New menu item edited.")
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    return render_template('editMenuItem.html', restaurant = restaurant, item = item)

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    deleteItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        flash("Menu item deleted.")
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    return render_template('deleteMenuItem.html', restaurant = restaurant, item = item)


#making API Endpoints (GET REQUEST):
@app.route('/restaurants/JSON/')
def restaurantsJSON():
    restaurants = session.query(Restaurant)
    print(restaurants)
    return jsonify(r = [r.serialize for r in restaurants])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON/')
def restaurantmenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return jsonify(Menuitems = [i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()

    return jsonify(MenuItem = [item.serialize])

if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)