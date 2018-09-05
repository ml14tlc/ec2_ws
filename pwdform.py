#!/usr/bin/env python
# -*- coding: UTF-8 -*-# enable debugging
import re, cgi, cgitb, string, random

#cgitb.enable()    
form = cgi.FieldStorage()

# Define the set where to pick the random password
randomset = string.letters + string.digits
# Read the password length
pwdlen = cgi.escape(form.getvalue('pwdlen'))
# Read the user's preference for the password character set
pwdtype = cgi.escape(form.getvalue('alphanum'))
# If special characters are included, then change the character set
if pwdtype == 'specialchars':
  randomset = string.letters + string.digits + string.punctuation

# Check that the input is a number
if re.search('^[0-9]+$', pwdlen) and int(pwdlen) >= 5 and int(pwdlen) <= 20:
  pwd = ''.join((random.choice(randomset)) for x in range(int(pwdlen)))
  msg = "<h2>Your password is</h2>\r\n<p>" + pwd + "</p>"
else:
  msg = "<h2>Error</h2>\r\n<p>" + pwdlen + " in an invalid input: please pick a number between 5 and 20</p>"
print("Content-Type: text/html;charset=utf-8\r\n")
print("\r\n")
print("<html>")
print("<head>")
print("<title>Here's your password</title>")
print("</head>")
print("<body>")
print(msg)
print("</body>")
print("</html>")
