from flask import Flask, render_template, request
from class_database import Mongo
import variables
from class_users import Users

app = Flask(__name__)
db_obj = Mongo(variables.uri, variables.db, variables.collection)
users_obj = Users("subscribers.db")

@app.route("/", methods = ['GET', 'POST'])
def home():
    try:
        if request.method == 'POST':
            user = request.form['username']
            password = request.form['password']
            
            if users_obj.search(user, password):
                return render_template("news_page_disease.html")
            
            else:
                error_message = 'Invalid username or password. Please try again.'
                return render_template("main.html", error = error_message)

        return render_template("main.html")
    
    except:
        return render_template("main.html")

@app.route('/back', methods = ["POST"])
def back():
    return render_template('main.html')

@app.route("/sign_up", methods = ['GET', 'POST'])
def sign_up():
    try:
        if request.method == 'POST':
            name = request.form['userName']
            password = request.form['psw']
            users_obj.inserting(name, password)
            return render_template("main.html")

        return render_template("sign_up.html")
    
    except:
        error_message = 'User with entered name already exist, try again.'
        return render_template("sign_up.html", error = error_message)

@app.route("/news_disease", methods = ['GET', 'POST'])
def news_disease():
    try:
        if request.method == 'POST':
            disease = request.form['disease']
            data = db_obj.read("diseases" , disease)
            return render_template("news_page_disease.html", result = data.to_html(render_links = True, escape = False), articles = len(data))
        
        return render_template("news_page_disease.html")
    except:
        # print("Enter a valid disease!")
        return render_template("news_page_disease.html")

@app.route("/news_icd10", methods = ['GET', 'POST'])
def news_icd10():
    try:
        if request.method == 'POST':
            code = request.form['diagnostic code'].upper()
            data = db_obj.read('ICD10', code)
            return render_template("news_page_icd10.html", result = data.to_html(render_links = True, escape = False), articles = len(data))

        return render_template("news_page_icd10.html")
    except:
        # print("Enter a valid code!")
        return render_template("news_page_icd10.html")

@app.route("/news_ndc", methods = ['GET', 'POST'])
def news_ndc():
    try:
        if request.method == 'POST':
            code = request.form['prescriptionCode']
            data = db_obj.read("NDC", code)
            return render_template("news_page_ndc.html", result = data.to_html(render_links = True, escape = False), articles = len(data))
        
        return render_template("news_page_ndc.html")
    except:
        # print("Enter a valid code!")
        return render_template("news_page_ndc.html")

if __name__ == '__main__':
    app.debug = True
    app.run()
