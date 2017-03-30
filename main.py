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
# The below form has 4 input fields and 4 error fields (not including submit).
# Input fields for username and email have value parameters = the users input.
# Input fields for password and verify have value parameters = "" .
# Once pw and vpw are entered and form is submitted, we want these fields empty.
# The error messages are listed after each input box.
# The variables surrounded by %s will be replaced from items in the replacements
# dictionary in the write_form function.

form = """
    <form  method = "post">
    <h1 style="color:blue;font-size:52px">SIGNUP</h1>
    <br>
    <br>
        <label> User Name
            <input type = "text" name="username" value="%(username)s">%(user_error)s
        </label>
        <br>
        <br>
        <label> Password
            <input type="password" name="password" value="">%(password_error)s
        </label>
        <br>
        <br>
        <label> Verify Password
            <input type="password" name="verify" value="">%(verify_error)s
        </label>
        <br>
        <br>
        <label>Email (Optional)
                <input type="text" name="email" value="%(email)s">%(email_error)s
        </label>
        <br>
        <br>
        <input type="submit" >
    </form>
    """

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
   return username and USER_RE.match(username)

PASS_Re = re.compile(r"^.{3,20}$")
def valid_password(password):
   return password and PASS_Re.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
   return not email or EMAIL_RE.match(email)


class MainHandler(webapp2.RequestHandler):
   def write_form(self, user_error="",username="",password_error="",
   verify_error="",email_error="",email=""):
      replacements = {'user_error':user_error,
                                   'username':username,
                                   'password_error':password_error,
                                   'verify_error':verify_error,
                                   'email_error':email_error,
                                   'email':email}
      self.response.write(form % replacements)

   def get(self):
       self.write_form()

   def post(self):
       have_error = False
       username = self.request.get('username')
       password = self.request.get('password')
       verify = self.request.get('verify')
       email = self.request.get('email')
       user_error = ""
       password_error = ""
       verify_error = ""
       email_error = ""

       if not valid_username(username):
           user_error="That's not a valid username."
           have_error = True

       if not valid_password(password):
           password_error="That's not a valid password."
           have_error = True

       elif password != verify:
           verify_error ="Your passwords don't match."
           have_error = True

       if not valid_email(email):
           email_error = "That's not a valid email."
           have_error = True

       if not have_error:
           self.redirect('/Welcome?username={}'.format(username))

       self.write_form(
       username=username,
       user_error=user_error,
       password_error=password_error,
       verify_error=verify_error,
       email=email,
       email_error=email_error)

class WelcomeHandler(webapp2.RequestHandler):
   def get(self):
       username = self.request.get("username")
       self.response.write(" Welcome "+ username+ "!")


app = webapp2.WSGIApplication([
   ('/', MainHandler),
   ('/Welcome',WelcomeHandler)
], debug=True)
