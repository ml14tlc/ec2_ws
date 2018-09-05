from flask import Flask
from flask_restful import Api, Resource
import re, string, random

# Initialise Flask
app = Flask(__name__)
api = Api(app)


class PasswordGen(Resource):

    # Return a password, 5 to 20 characters long, picking only letters and numbers
    def get(self, pwdlen):
        # Define the set where to pick the random password
        randomset = string.letters + string.digits

        if re.search('^[0-9]+$', pwdlen) and int(pwdlen) >= 5 and int(pwdlen) <= 20:
            return {"password": ''.join((random.choice(randomset)) for x in range(int(pwdlen))), "length": pwdlen}, 200
        else:
            return {"error": "Please provide an integer between 5 and 20"}, 400

    # Return a 400 on all other methods
    def post(self, pwdlen):
        return {"error": "Method not implemented"}, 400

    def put(self, pwdlen):
        return {"error": "Method not implemented"}, 400

    def delete(self, pwdlen):
        return {"error": "Method not implemented"}, 400

    def patch(self, pwdlen):
        return {"error": "Method not implemented"}, 400

    def options(self, pwdlen):
        return {"error": "Method not implemented"}, 400
      
# Define the application, expect a string (Check that's made out of numbers and convert it to an integer))
api.add_resource(PasswordGen, "/password/<string:pwdlen>")

# This is required to run inside Apache
if __name__ == "__main__":
    app.run(debug=False)
