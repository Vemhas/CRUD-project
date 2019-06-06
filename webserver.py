from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
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
                    output += "<a href="">Edit</a> <br>"
                    output += "<a href="">Delete</a> <br> <br> <br>"
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

        except IOError:
            self.send_error(404 - "File Not Found %s" % self.path)
    
    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.send_header('Location', '/restaurants')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                newRestaurant = fields.get('restaurantname')
            addRestaurant = Restaurant(name = "%s" % newRestaurant[0])
            print("etter addRestaurant objektet")
            print(addRestaurant)
            session.add(addRestaurant)
            session.commit()


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
