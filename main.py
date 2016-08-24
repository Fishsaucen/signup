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
import cgi
import re

form_signup="""
<html>
    <head>
        <title>User Registration</title>
        <style>
            .error {
                color: red;
            }
            #signup_div {
                position: absolute;
                left: 30%%;
                display: block;
                margin: center;
                background-color: #4ed;
            }
            #table_header {
                padding-top: 2%%;
                padding-bottom: 0%%;
                text-align: center;
                background-color: #cae;
            }
            input {
                position: relative;
                top: 8px;
                left: 15px;
            }
        </style>
    </head>
<body>
    <div id="signup_div">
        <form method="post">
            <table>
                <tr>
                   <td colspan="3" id="table_header"><h1>Signup</h1>
                   </td >
                </tr>
                <tr>
                    <td>
                        <label>Username</label> 
                    </td>
                    <td>
                        <input type="text" name="user_name" value="%(user_name)s">
                    </td>
                    <td>
                        <span class="error">%(user_name_error)s</span>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label>Password</label> 
                    </td>
                    <td>
                        <input type="password" name="password">
                    </td>
                    <td>
                        <span class="error">%(password_error)s</span>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label>Verify Password</label> 
                    </td>
                    <td>
                        <input type="password" name="verify">
                    </td>
                    <td>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label>Email (optional)</label> 
                    </td>
                    <td>
                        <input type="text" name="email" value="%(email)s">
                    </td>
                    <td>
                        <span class="error">%(email_error)s</span>
                    </td>
                </tr>
            </table>
            <input type="submit">
        </form>
    </div>
</body>
</html>
"""
# Regular Expression global variables
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"[\S]+@[\S]+.[\S]+$")

def verify_user_name(username):
    return USER_RE.match(username)

def verify_password(password):
    return PASS_RE.match(password)

def verify_email(email):
    return EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):
    """ Display input fields for the user to sign up with a username, password, and
        optional email address. We must verify that all of these fields are correct
        and indicate which fields need to be changed. If the user successfully 
        completes all fields, redirect them to the welcome page.
    """
    def write_form(self, user_name="", email="", user_name_error="", password_error="", 
            email_error=""):

        self.response.write(form_signup % {"user_name": user_name, "email": email, 
            "user_name_error": user_name_error, "password_error": password_error, 
            "email_error": email_error})

    def get(self):
        self.write_form()

    def post(self):
        valid_input=True
        user_name = self.request.get(cgi.escape('user_name'))
        password= self.request.get(cgi.escape('password'))
        verify= self.request.get(cgi.escape('verify'))
        email= self.request.get(cgi.escape('email'))
        user_name_error=""
        password_error=""
        email_error=""
        password_len= len(password)

        if not verify_user_name(user_name):
            valid_input=False
            user_name_error="Invalid user name."

        if not verify_password(password):
            valid_input=False
            password_error="Invalid password."
            password=""

        if password != verify:
            valid_input=False
            password_error="Passwords do not match."
            password=""
        if password_len < 3 or password_len > 20:
            valid_input=False
            password_error="Password length must be between 3-20 characters"
            password=""
        if email:
            if not verify_email(email):
                valid_input=False
                email_error="Invalid email address."


        if valid_input:
            self.redirect('/welcome?user_name={}'.format(user_name))
        else:
            self.write_form(user_name, email, user_name_error, password_error, email_error)


class WelcomeHandler(webapp2.RequestHandler):

    def get(self):
        user_name= self.request.get('user_name')
        self.response.write("<h1>hiya {}</h1>".format(user_name))

        #TODO: you NEED to escape all user input

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
