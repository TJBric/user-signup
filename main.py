
import webapp2
import re

form="""
     <head>
            <style>
                .error {
                    color: red;
                }
            </style>
        </head>
        <body>
        <h1>User Signup</h1>
            <form method="post">
                <table>
                    <tr>
                        <td><label for="username">Username:</label></td>
                        <td>
                            <input name="username" type="text" value="" required>
                            <span class="error"></span>
                        </td>
                    </tr>
                    <tr>
                        <td><label for="password">Password:</label></td>
                        <td>
                            <input name="password" type="password" required>
                            <span class="error"></span>
                        </td>
                    </tr>
                    <tr>
                        <td><label for="verify">Verify Password</label></td>
                        <td>
                            <input name="verify" type="password" required>
                            <span class="error"></span>
                        </td>
                    </tr>
                    <tr>
                        <td><label for="email">Email (optional)</label></td>
                        <td>
                            <input name="email" type="email" value="">
                            <span class="error"></span>
                        </td>
                    </tr>
                </table>
                <input type="submit">
            </form>
        </body>
"""

class MainHandler(webapp2.RequestHandler):
    def write_form(self, username="", password="", verify="", email=""):
        self.response.out.write(form % {"username": username,
                                        "password": password,
                                        "verify": verify,
                                        "email": email
                                        })

    def get(self):
        self.write_form()

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        error = False

        params = dict(username = username,
                      email = email)

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            error = True

        if error:
            self.response.out.write(form, **params)
        else:
            self.redirect('/welcome?username=' + username)


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')

def valid_username(username):
    return username and USER_RE.match(username)

def valid_password(password):
    return password and PASS_RE.match(password)

def valid_email(email):
    return not email or EMAIL_RE.match(email)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        self.response.out.write("Welcome, " + username + "!")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)

], debug=True)
