from flask import Flask, request, redirect, url_for, render_template, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# API to return all restaurants as a JSON object
@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant)
    return jsonify(restaurant=[r.serialize for r in restaurants])


# API to return all the menu items from a restaurant as a JSON object
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


# API to return a menu item from a restaurant as a JSON object
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    items = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=[items.serialize])


# List all the restaurants in the DB with edit and delete links.
# It also has a link to display the menu for the restaurant
@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    restaurants = session.query(Restaurant)
    return render_template('restaurants.html', restaurants=restaurants)


# Create a new restaurant
@app.route('/restaurant/new', methods = ['POST', 'GET'])
def newRestaurant():
    if request.method == 'POST':
        restaurant = Restaurant(name=request.form['newRestName'])
        session.add(restaurant)
        session.commit()
        flash("New restaurant created!!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')


# Edit the restaurant
@app.route('/restaurant/<int:restaurant_id>/edit', methods = ['POST', 'GET'])
def editRestaurant(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if myRestaurantQuery != []:
            if request.form['RestName']:
                myRestaurantQuery.name=request.form['RestName']
                session.add(myRestaurantQuery)
                session.commit()
                flash("Restaurant has been edited!!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant_id=restaurant_id, item=myRestaurantQuery)


# Delete the restaurant
@app.route('/restaurant/<int:restaurant_id>/delete', methods = ['POST', 'GET'])
def deleteRestaurant(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if myRestaurantQuery != []:
            session.delete(myRestaurantQuery)
            session.commit()
            flash("Restaurant has been deleted!!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant_id=restaurant_id, item=myRestaurantQuery)


# Display the menu for the restaurant
@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)


# Create a new menu item for a restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/new', methods = ['POST', 'GET'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        menu_item = MenuItem(name=request.form['newMenuItemName'], \
                    price=request.form['newMenuItemPrice'], \
                    description=request.form['newMenuItemDesc'], \
                    course=request.form['newMenuItemCourse'], \
                    restaurant_id=restaurant_id)
        session.add(menu_item)
        session.commit()
        flash("New menu item created!!")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id=restaurant_id)


# Edit a menu item for a restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods = ['POST', 'GET'])
def editMenuItem(restaurant_id, menu_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    myMenuItemQuery = session.query(MenuItem).filter_by(id=menu_id, restaurant_id=restaurant_id).one()
    if request.method == 'POST':
        if myMenuItemQuery != []:
            if request.form['MenuItemName']:
                myMenuItemQuery.name=request.form['MenuItemName']
                myMenuItemQuery.price=request.form['MenuItemPrice']
                myMenuItemQuery.description=request.form['MenuItemDesc']
                myMenuItemQuery.course=request.form['MenuItemCourse']
                session.add(myMenuItemQuery)
                session.commit()
                flash("Menu item has been edited!!")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=myMenuItemQuery)

# Delete a menu item from a restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['POST', 'GET'])
def deleteMenuItem(restaurant_id, menu_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    myMenuItemQuery = session.query(MenuItem).filter_by(id=menu_id, restaurant_id=restaurant_id).one()
    if request.method == 'POST':
        if myMenuItemQuery != []:
            session.delete(myMenuItemQuery)
            session.commit()
            flash("Menu item has been deleted!!")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=myMenuItemQuery)


# main function
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)