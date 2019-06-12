from flask import Flask
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


@app.route('/')
@app.route('/hello')
def HelloWorld():
    restaurants = session.query(Restaurant)
    output = ''
    for restaurant in restaurants:
        output += '<br>'
        output += restaurant.name
        items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
        for i in items:
            output += i.name
            output += i.price
            output += '<br>'
    return output
    

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port='5000')
