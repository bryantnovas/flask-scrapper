# 
# IMPORTS
# 
# you might have to import additional things you need

from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from crontab import CronTab
cron = CronTab(root=True)
job = cron.new(command='python import_script.py')
job.day.every(1)
cron.write()

#
# SETUP/CONFIG
#
# change the classname to reflect the name of your table
# change the columns to reflect the columns you need
# each row of your data will be an instance of this class

app = Flask(__name__)

app.config["ENV"] = 'development'
app.config["SECRET_KEY"]=b'_5#y2L"F4Q8z\n\xec]/'

# change the following .db file name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crypto_db.db'
# this line is to prevent SQLAlchemy from throwing a warning
# if you don't get one with out it, feel free to remove
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#
# DB SETUP
# 

# this set's up our db connection to our flask application
db = SQLAlchemy(app)

# this is our model (aka table)
class DBTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    symbol = db.Column(db.String(255), nullable=False)
    price = db.Column(db.String(255), nullable=False)
    market_share = db.Column(db.String(255), nullable=False)
    change_24hr = db.Column(db.String(255), nullable=False)
    
#
# VIEWS 
#


# set up your index view to show your "home" page
# it should include:
# links to any pages you have
# information about your data
# information about how to access your data
# you can choose to output data on this page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# include other views that return html here:
@app.route('/other')
def other():
    return render_template('other.html')

# set up the following views to allow users to make
# GET requests to get your data in json
# POST requests to store/update some data
# DELETE requests to delete some data

# change this to return your data
@app.route('/api', methods=['GET'])
def get_data():
    table = DBTable.query.all()
    d = {row.name:[row.symbol, row.price, row.market_share, row.change_24hr] for row in table}
    return jsonify(d)

# change this to allow users to add/update data
@app.route('/api', methods=['POST'])
def add_data():
    row = dict(request.args.items())
    message = ''
    try:
        db_row = DBTable(name=row['name'], symbol=row['symbol'], price=row['price'], market_share=row['market_share'], change_24hr=row['change_24hr'])
        db.session.add(db_row)
        db.session.commit()
        print('sucessfully added row')
        message = 'Success'
    except Exception as e:
        print(e)
        message = 'Error!'
    return jsonify({'message':message})
        
# change this to allow the deletion of data
@app.route('/api', methods=['DELETE'])
def delete_data():
    row = dict(request.args.items())
    message = ''
    try:
        db_row = DBTable.query.filter_by(name=row['name']).first()
        db.session.delete(db_row)
        db.session.commit()
        print('sucessfully deleted row')
        message = 'Success'
    except Exception as e:
        print(e)
        message = 'Error!'
    return jsonify({'message': message})

#
# CODE TO BE EXECUTED WHEN RAN AS SCRIPT
#

if __name__ == '__main__':
    app.run(debug=True)