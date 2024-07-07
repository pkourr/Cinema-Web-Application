# Import necessary modules
from flask import Flask, render_template, request, url_for, session, redirect, flash
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import string
import bcrypt
import sys
import os
import tempfile
from datetime import timedelta

# Initialize Flask application
app = Flask(__name__)

# Set the lifetime of permanent session to 1 day
app.permanent_session_lifetime = timedelta(days = 1)

# Connect to the MongoDB Atlas cluster
cluster = MongoClient("mongodb+srv://Student:Student2023@cluster0.dgdt5rp.mongodb.net/?retryWrites=true&w=majority")

# Access the "cinema" database in the cluster
db = cluster["cinema"]

# Access the "users" and "projection" collections in the "cinema" database
users = db['users']
projection = db['projection']

# Define the home page route
@app.route("/")
def home():
  # Clear session data
  #session.clear()

  # If the user tries to log in
  if 'username' and 'password' in session:
    # Check if the entered credentials are correct
    registered_users = users.find_one({'username': session['username'], 'password': session['password']})
    try:
      # If the credentials are correct, set the session as logged in
      print(registered_users['adress'])
      if 'logged_in' not in session:
        flash('You have successfully logged in as ' + session['username'] + '!')
      session['logged_in'] = True
      print(session['username'])
      print(session['password'])
    except TypeError as e:
      # If the credentials are wrong, display an error message and redirect to the login page
      flash('Your credentials are not correct.')
      return redirect(url_for('login'))

  # If the user is not logged in, display the home page
  return render_template("index.html")

# Define the movies page route
@app.route("/movies",  methods = ['POST', 'GET'])
def movies():
  # If the user submits the form to select a movie
  if request.method == "POST":
    # Get the selected movie from the form and store it in the session data
    movie = request.form['title']
    session['movie'] = movie
    return redirect(url_for('halls'))

  # If the request method is GET, display the movies page
  return render_template("movies.html")

# Define the halls page route
@app.route("/movies/hall",  methods = ['POST', 'GET'])
def halls():
  # If the user is not logged in, redirect to the movies page
  if 'username' not in session:
    flash('You need to log in first.')
    return redirect(url_for('movies'))

  # If the user submits the form to select a movie type and hour
  if request.method == "POST":
    # Get the selected movie type and hour from the form and store them in the session data
    selected_price = request.form['selected_price']
    session['selected_price'] = selected_price

    selected_hour = request.form['selected_hour']
    session['selected_hour'] = selected_hour

    # Redirect to the seats page
    return redirect(url_for('seats'))

  # If the request method is GET, display the halls page
  return render_template("hall_hour.html")

@app.route("/movies/hall/seats", methods = ['POST', 'GET'])
def seats():
  
  # Initialize some variables for seat selection
  final = []
  final2 = []
  alphabet = ['A', 'B', 'C', 'D', 'E']
  numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
  
  # Create a list of all possible seat combinations
  for i in alphabet:
    final = []
    for j in numbers:
      final.append(i + j)
    final2.append(final)
  print(final2)

  lista = []
  # Find all the selected seats for the specific movie-hall-hour
  docs = projection.find({'movie': session['movie'], 'hall': session['selected_price']})
  for doc in docs:
    lista.append(doc['seat'])
  
  if request.method == "POST":
    print('ok')
    try:
      # If you chose a seat:
      selected_seat = request.form['selected_seat']
      session['selected_seat'] = selected_seat
    except KeyError as e:
      # If you pressed submit and did not choose a seat, the page will refresh
      flash('Seat selection is mandatory!')
      return redirect(url_for('seats'))

    return redirect(url_for('final'))

  # Render the seat selection page
  return render_template("seats.html", dis_seats = lista, final2 = final2)


@app.route("/movies/hall/seats/end")
def final():
  # Print the stored session variables to check everything is working properly
  print(session['username'])
  print(session['password'])
  print(session['selected_price'])
  print(session['selected_hour'])
  print(session['selected_seat'])
  print(session['movie'])
  # Insert the new reservation to the database
  projection.insert_one({'username': session['username'], 'hall': session['selected_price'], 'time': session['selected_hour'], 'seat': session['selected_seat'], 'movie': session['movie']})
  docs = projection.find({'username': session['username'], 'hall': session['selected_price'], 'time': session['selected_hour'], 'seat': session['selected_seat'], 'movie': session['movie']})
  for doc in docs:
    var = doc['_id']
  # Render the final page
  return render_template("final.html", var = var)


@app.route("/login", methods = ['POST', 'GET'])
def login():
  # Enter username and password and try to login (collect data from login form)
  if request.method == "POST":
    user = request.form['username']
    session['username'] = user
    session['password'] = request.form['pass']
    return redirect(url_for('home'))
  
  # Handle registration process
  elif 'reg_user' in session:
    registered_users = users.find_one({'username': session['reg_user']})
    try:
      # When we try to register and username is already taken
      print(registered_users['country'])
      flash('Username already in use', 'warning')
      return redirect(url_for('register'))
    except TypeError as e:
      # Registration successful
      print(session['reg_user'])
      users.insert_one({'username': session['reg_user'], 'password': session['reg_password'], 'city': session['selected_city'], 'name': session['name'], 'email': session['email'], 'adress': session['adress'], 'country': session['selected_country']})
      session.pop('reg_user', None)
      return render_template('login.html')
  print('neither')
  return render_template('login.html')
  
  
@app.route("/register", methods = ['POST', 'GET'])
def register():
  if request.method == "POST":
    # take all data from register form
    # retrieve data from the HTML form using request.form and store it in variables
    reg_user = request.form['username']
    reg_password = request.form['pass']
    selected_country = request.form['selected_country']
    selected_city = request.form['selected_city']
    name = request.form['name']
    email = request.form['email']
    adress = request.form['adress']
    # store user data in session object
    session['reg_user'] = reg_user
    session['reg_password'] = reg_password
    session['selected_country'] = selected_country
    session['selected_city'] = selected_city
    session['name'] = name
    session['email'] = email
    session['adress'] = adress
    flash('Registration successfull!', 'success')
    # redirect to login page after registration
    return redirect(url_for('login'))
  # render the registration page if it's a GET request
  return render_template("register.html")

# logout if we press logout
@app.route("/logout", methods = ['POST', 'GET'])
def logout():  
  # clear session variables to log out user
  session.pop('logged_in', None)
  session.pop('username', None)
  session.pop('password', None)
  # display message indicating successful logout using flash function
  flash('You have successfully logged out!', 'success')
  # render the index page after logging out
  return render_template("index.html")

# error page
@app.route("/error", methods = ['POST', 'GET'])
def error():  
  # render error page
  return render_template("error.html")

@app.route("/admin", methods = ['POST', 'GET'])
def admin():  
  # error 404 if we try to enter admin page without admin credentials
  if 'username' not in session:
    # if username is not found in session object, redirect to the error page
    return redirect(url_for('error'))
  # check if the user has admin privileges
  else:
    if session['username'] != 'admin':
      # if user doesn't have admin privileges, redirect to the error page
      return redirect(url_for('error'))
  lista = []
  lista2 = []
  # find all data necessary for admin page table
  # use find() function to get all documents from the users collection and store them in docs
  docs = users.find({})
  for doc in docs:
    lista = []
    # retrieve data from each document and store it in a list
    lista.append(doc['username'])
    lista.append(doc['email'])
    lista.append(doc['name'])
    lista2.append(lista)
  print(lista)
  # render customer_admin.html template with the list of user data
  return render_template("customer_admin.html", lista2 = lista2)


@app.route("/admin/view/:<username>/:<id>", methods = ['POST', 'GET'])
def editor(username, id):
  # Initialize empty lists for various parameters
  lista = []
  seats_list = []
  alphabet = list(string.ascii_uppercase)
  numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
  final = []
  # Create a list of all possible seat combinations
  for i in alphabet:
    for j in numbers:
      final.append(i + j)
  print(final)
  # Find the reservation we want to edit with the respective ID
  docs = projection.find({'_id': ObjectId(id)})
  for doc in docs:
    lista.append(doc)
    print(doc)
  # Find all reservations and add their seats to seats_list
  docs = projection.find()
  for doc in docs:
    seats_list.append(doc['seat'])
    print(doc)
  print(seats_list)
  # Check if the request is a POST request (i.e. form submission)
  if request.method == "POST":
    # Update the reservation with the new data and pass them to the database
    new_hall = request.form['new_price']
    new_hour = request.form['new_hour']
    new_seat = request.form['new_seat']
    session['new_hall'] = new_hall
    session['new_hour'] = new_hour
    session['new_seat'] = new_seat
    projection.update_one({'_id': ObjectId(id)}, { "$set": { "hall": session['new_hall'] } })
    projection.update_one({'_id': ObjectId(id)}, { "$set": { "hour": session['new_hour'] } })
    projection.update_one({'_id': ObjectId(id)}, { "$set": { "seat": session['new_seat'] } })
    flash('Reservation updated successfully!', 'success')
    # Redirect to the viewer page for the user
    return redirect(url_for('viewer', username = username))
  # Render the customer_edit.html template with the appropriate data
  return render_template("customer_edit.html", lista = lista, final = final, seats_list = seats_list)


@app.route("/admin/view/:<username>", methods = ['POST', 'GET'])
def viewer(username):
  lista = []
  # Find all the reservations for a certain user
  docs = projection.find({'username': username})
  for doc in docs:
    lista.append(doc)
  print(lista)
  # If there are no reservations for this user, show a message and redirect to admin page
  if len(lista) == 0:
    flash('No reservations found for this user.')
    return redirect(url_for('admin'))
  # Render the customer_view.html template with the appropriate data
  return render_template("customer_view.html", lista = lista)

@app.route("/delete:<username>", methods = ['POST', 'GET'])
def delete(username):
  # Delete user and their reservations
  users.delete_one({'username': username})
  projection.delete_many({'username': username})
  flash('User deleted successfully!', 'success')
  # Redirect to the admin page
  return redirect(url_for('admin'))


# This block of code runs the Flask application if this script is run directly, 
# by setting the app's secret key and starting it in debug mode. 
# It is good practice to keep the secret key hidden, like in an environment variable.
# The debug mode helps to identify errors, but shouldn't be used in production.
if __name__ == "__main__":
  app.secret_key = 'mysecret'
  app.run(debug = True)

