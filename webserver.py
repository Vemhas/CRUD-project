#!/usr/bin/env python2
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import bleach
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()



class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<a href='/restaurants/new'><h3>Make a New Restaurant Here \n</h3></a>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "<br>"
                    output += """<a href="restaurants/%s/edit">Edit</a> <br>""" % restaurant.id
                    output += """<a href="restaurants/%s/edit">Delete</a> <br> <br> <br>""" % restaurant.id
                output += "</body></html>" 
                self.wfile.write(output)
                return
            
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body><h2>Make a New Restaurant</h2>"
                output += "<form method='POST' enctype='multipart/form-data'> <input name='restaurantname' type='text' placeholder='New Restaurant Name' ><input type='submit' value='Create'> </form>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                restaurantIdPath = self.path.split("/")[2]
                restaurant = session.query(Restaurant).filter_by(id = restaurantIdPath).one()
                if restaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = ""
                    output += "<html><body>"
                    output += "<h2>%s</h2>" % restaurant.name
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit'>" % restaurantIdPath 
                    output += "<input name='renameRestaurant' type='text' value='%s'>" % restaurant.name
                    output += "<input type='submit' value='Rename'> "
                    output += "</form>" 
                    output += "</body></html>"
                    self.wfile.write(output)
                    return

        except IOError:
            self.send_error(404 - "File Not Found %s" % self.path)
    
    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
            
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    newRestaurant = fields.get('restaurantname')
                    addRestaurant = Restaurant(name = "%s" % newRestaurant[0])
                    session.add(addRestaurant)
                    session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    newRestaurantName = fields.get('renameRestaurant')
                    print(newRestaurantName)
                    print("newRestaurantName")
                    restaurantIdPath = self.path.split("/")[2]
                    print(restaurantIdPath)
                    print("restaurantIdPath")
                    restaurantQuery = session.query(Restaurant).filter_by(id = restaurantIdPath).one()
                    print(restaurantQuery.name)
                    print("restaurantQuery")
                    if restaurantQuery != []:
                        restaurantQuery.name = newRestaurantName[0]
                        session.add(restaurantQuery)
                        session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

        except:
            pass

            
            
        



def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print ("Web Server running on port nr %s" % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print ("^C entered, stopping web server...")
        server.socket.close()
        

if __name__ == '__main__':
    main()
