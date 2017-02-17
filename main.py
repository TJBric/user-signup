#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import webapp2
import re
import cgi

header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
    <style type="text/css">
    span {color: red}
    label {
        display:inline-block;
        width: 125px;
        margin-bottom: 5px;
        }
    </style>
</head>
"""

form = """
<body>
    <h1>User Signup</h1>
    <form method="post">
        <label>User Name: </label>
        <input type="text" name="username" value="%(username)s">
        <span>%(error_user)s</span>
        <br>
        <label>Password: </label>
        <input type="password" name="password">
        <span>%(error_pw)s</span>
        <br>
        <label>Verify Password: </label>
        <input type="password" name="verify">
        <span>%(error_verify)s</span>
        <br>
        <label>E-Mail (optional):</label>
        <input type="text" name="email" value="%(email)s">
        <span>%(error_email)s</span>
        <br><br>
        <input type="submit">
    </form>
"""
footer="""
</body>
</html>
"""
class MainHandler(webapp2.RequestHandler):
    def write_form(self, username="", error_user="", error_pw="", error_verify="", email="", error_email=""):
          self.response.out.write(header + (form % {"username": username,
                                            "email": email,
                                            "error_pw": error_pw,
                                            "error_email": error_email,
                                            "error_user" : error_user,
                                            "error_verify" : error_verify
                                            }) + footer)
    def get(self):
        self.write_form()

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        esc_user = escaped_html(username)
        esc_pw = escaped_html(password)
        esc_verify = escaped_html(verify)
        esc_email = escaped_html(email)

        form_user = esc_user
        form_pw = "Invalid Password"
        form_verify = "Passwords don't match."
        form_email = "Invalid e-mail."

        if not valid_username(esc_user):
            self.write_form("", "Invalid Username", "", "", "", "")
        elif not valid_password(esc_pw):
            self.write_form(form_user, "", form_pw, "", esc_email, "")
        elif esc_pw != esc_verify:
            self.write_form(form_user,"", "", "Passwords don't match.", esc_email, "")
        elif not valid_email(esc_email):
            self.write_form(form_user, "", "", "", "", form_email)
        else:
            self.response.out.write("<h2>Welcome, " + username + "!</h2>")


def escaped_html(text):
    return cgi.escape(text)

user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and user_re.match(username)

pass_re = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and pass_re.match(password)

email_re  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or email_re.match(email)


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
