#Code by Selena Jimenez feat Google
#Project 1!
#Web Programming

import os
from flask import Flask, render_template, request, session, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
from flask import redirect,url_for


app = Flask(__name__)
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")


message=""            #To show messages to the html (alerts)
error=""                #To show error messages
isbn=""

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#======================================================================================================================
#===================================CACHE==============================================================================
#======================================================================================================================
@app.after_request    #In case we want to return, we use dizzzzzz
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

#======================================================================================================================
#===================================INICIO=============================================================================
#======================================================================================================================
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")        #Just the start point

#======================================================================================================================
#=========================VERIFICAR SI HAY LOG O NO====================================================================
#======================================================================================================================
@app.route("/start")
def start():
  if session.get('username')!=None:         #If we have a session
    return render_template("main.html", message="Welcome back, "+session.get('username')+", Search a book") #Direct to the sauce
  else:
    return render_template("login.html")    #Log in

#======================================================================================================================
#================================ADD USER/GO TO LOG====================================================================
#======================================================================================================================
@app.route("/sign", methods=["GET", "POST"])
def sign():
    if request.method == "POST":
        username = request.form.get("username")         #Declarando las variables obtenidas desde el HTML
        password = request.form.get("password")         #Declarando las variables obtenidas desde el HTML

          #Add the new values obtained from the html form
        db.execute("INSERT INTO account (username,password) VALUES ( :username , :password )",{"username":username,"password":password})
        db.commit()                 #We add the new user
        return render_template("login.html", message="User created, please login")

#======================================================================================================================
#============================VERIFY CORRECT LOGIN======================================================================
#======================================================================================================================
@app.route("/main", methods=["GET", "POST"])
def login():
    if session.get('username')!=None:
        return render_template("main.html")             #Verify if there is an active session
      
    if request.method == "POST":
        username = request.form.get("username")         #Declarando las variables obtenidas desde el HTML
        password = request.form.get("password")         #Declarando las variables obtenidas desde el HTML

        if db.execute("Select * from account where username=:username and password=:password",{"username":username,"password":password}).rowcount == 1:
            session['username']=username	
            return render_template("main.html", message="Welcome "+username+", Search a book")
        else:
            return render_template("sign.html", message="User not found, create one!")

#======================================================================================================================
#=====================================LOG OUT==========================================================================
#======================================================================================================================
@app.route("/logout", methods=["GET", "POST"])
def logout():
    session['username']=None
    return redirect(url_for('index'))       #Take you to the very beginning


#======================================================================================================================
#=======================================SEARCH BOOK====================================================================
#======================================================================================================================
@app.route("/book", methods=["GET", "POST"])
def book():
    if session.get('username')==None:
        return redirect(url_for('login'))               #If there is no session, u'll be redirected to login
    
    if request.method == "POST":
        isbn = '%'+request.form.get("isbn")+'%'
        author = '%'+request.form.get("author")+'%'
        title = '%'+request.form.get("title")+'%'
        books=db.execute("Select * from books where isbn like :isbn  and author like :author and title like :title ",{"author": author, "isbn": isbn, "title":title}).fetchall()
        #res=len(books)
        if len(books)==0:
            return render_template("main.html", error="No results found")       #Just show u a "no results found" message
        else:
            return render_template("main.html", book=books)     #Show results
        
    return render_template("main.html", message="Welcome back, "+session.get('username')+", Search a book")


#======================================================================================================================
#=======================================REVIEW STUFF, hate u===========================================================
#======================================================================================================================
@app.route("/isbn/<string:isbn>", methods=["GET", "POST"])
def isbn(isbn):
    if session.get('username')==None:                   #See login
        return redirect(url_for('login'))

    rating='Average rating: '
    count='Number of ratings: '
    
    try:                    #Get the reviews from the web page using the ISBN
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "VNPjjx8kWTBjY5tOBQ5FQQ", "isbns": isbn})
        api=res.json()      
        rating=rating+str(api['books'][0]['average_rating'])
        count=count+str(api['books'][0]['reviews_count'])
    except:
        rating='There is no review available'
        count=''

    username= session.get('username')               #get the user in order to know who review

    book=db.execute("Select * from books where isbn=:isbn",{"isbn":isbn}).fetchall()     #Select the books that was "linked"(?)
    reviews=db.execute("Select * from reviews where isbn=:isbn",{"isbn":isbn}).fetchall()   #Select the book from the reviews table
    reviewusr=db.execute("Select * from reviews where isbn=:isbn and username=:user",{"isbn":isbn,"user": username}).rowcount

    if reviewusr==0:        #If there is no review from the user to the book we create one (***)
        if request.method == "POST":
            commit=request.form.get("commit")           #Get data from the html
            grade=request.form.get("grade")
            if grade=='':
                grade=0
                
            db.execute("Insert into reviews(isbn,username,review)  values (:isbn,:user,:review)",{"isbn":isbn,"user":username,"review":commit})
            review_count=1
            average_score=0.0       
            
            for review in book:
                review_count=review_count+int(review.review_count)
                average_score=(float(review.average_score)+int(grade))/int(review_count)

            db.execute("update books set review_count=:review_count where isbn=:isbn",{"isbn":isbn,"review_count":review_count})
            db.commit()             #Save the reviews made by the user
            
            db.execute("update books set average_score=:average_score where isbn=:isbn",{"isbn":isbn,"average_score":average_score})
            db.commit()             #Save the reviews made by the user
            
            reviews=db.execute("Select * from reviews where isbn=:isbn",{"isbn":isbn}).fetchall()
            book=db.execute("Select * from books where isbn=:isbn",{"isbn":isbn}).fetchall()
            
            return render_template("review.html",isbn=isbn,res=rating,count=count,book=book,reviews=reviews,error='The user has a reviews, no is valid more reviews',p=False)

        elif len(reviews)==0:   
            return  render_template("review.html",isbn=isbn,res=rating,count=count,book=book,error='There is any review')
        else:
            return  render_template("review.html",isbn=isbn,res=rating,count=count,book=book,reviews=reviews)
    else: #If THERE IS a review, then the user will not submit one (***)
        return  render_template("review.html",isbn=isbn,res=rating,count=count,book=book,reviews=reviews,error='The user has a review for this book, no is valid more reviews',p=False)


#======================================================================================================================
#=======================================API STUFF======================================================================
#======================================================================================================================
@app.route("/api/<string:isbn>", methods=["GET", "POST"])
def jsonapi(isbn):
    if session.get('username') is None:             #lo de siempre
        return redirect(url_for('login'))
    
    book=db.execute("Select * from books where isbn=:isbn ",{"isbn":isbn}).fetchall()        
    if len(book)==0:
        return  render_template("error.html",message="404")     #If there is no book, return an error page

    elif request.method == "GET":
        return render_template("api.html", info=book)           #Send the info to an html to print it

#======================================================================================================================
#================================FINISHED AAAAAAAAA====================================================================
#======================================================================================================================
