from flask import Flask, render_template, request, redirect, url_for, Response
import os
from os.path import join, dirname, realpath
import pandas as pd
import mysql.connector

from scripts.emission_calc import emission_calculator
from scripts.airport_dist_calc import calculate_distance

app = Flask(__name__)

# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

# Database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="seatTle*!31",
  database="flight_data"
)

mycursor = mydb.cursor()

#mycursor.execute("SHOW DATABASES")

# View All Database
#print('Printing DBs...')
#for x in mycursor:
#  print(x)
#print('')

# Root URL
@app.route('/')
def index():
     # Set The upload HTML template '\templates\index.html'
    return render_template('index.html')

# Results URL
@app.route('/results')
def results():
     # Set The upload HTML template '\templates\index.html'
    return render_template('results.html')

# template URL
@app.route("/getTemplate")
def getTemplate():
      print(os.getcwd())
      with open("templates/artifacts/flights_template.csv") as fp:
            csv = fp.read()
      return Response(
                  csv,
                  mimetype="artifacts",
                  headers={"Content-disposition":
                        "attachment; filename=flight_template.csv"})


# Get the uploaded files
@app.route("/", methods=['POST'])
def uploadFiles():
      # get the uploaded file
      uploaded_file = request.files['flights_file']
      if uploaded_file.filename != '':
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
          # set the file path
           uploaded_file.save(file_path)
           parseCSV(file_path)
          # save the file
      return redirect(url_for('results'))

def parseCSV(filePath):
      # Use Pandas to parse the CSV file
      df = pd.read_csv(filePath)

      # Loop through the Rows
      miles_list = []
      emiss_list = []
      for i,row in df.iterrows():
             sql = "INSERT INTO flights (origin_airport, destination_airport, class, round_trip, usd_amount, distance_miles, emissions) VALUES (%s, %s, %s, %s, %s, %s, %s)"
             dist = calculate_distance(row['origin_airport'], row['destination_airport'])
             miles_list.append(dist)
             emiss = emission_calculator(miles=dist)
             emiss_list.append(emiss)
             value = (row['origin_airport'],row['destination_airport'],row['class'],row['round_trip'],row['usd_amount'], dist, emiss)
             mycursor.execute(sql, value)
             mydb.commit()
             print(i,row['origin_airport'],row['destination_airport'],row['class'],row['round_trip'],row['usd_amount'], dist, emiss)
      
      df['distance_miles'] = miles_list
      df['emissions'] = emiss_list

      # total metrics
      total_dist = sum(df['distance_miles'])
      total_emissions = sum(df['emissions'])
      em_per_mile = total_emissions / total_dist
      print('')
      print('----')
      print(f'Travelling a total distance of {total_dist} miles, there were {total_emissions} tonnes of carbon emitted per person averaging out to {em_per_mile} tonnes per person per mile')
      print('----')
      print('')
      return df, total_dist, total_emissions

if (__name__ == "__main__"):
     app.run(port = 5000)