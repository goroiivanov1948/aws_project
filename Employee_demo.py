from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb
)

def generate_image_url(emp_id):
    emp_image_filename = f"emp-id-{emp_id}_image_file.png"  # Adjust the filename format according to your image naming convention
    image_url = f"https://{bucket}.s3.{region}.amazonaws.com/{emp_image_filename}"
    return image_url


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('AddEmp.html')

@app.route("/about", methods=['POST'])
def about():
    return render_template('www.intellipaat.com')

@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    pri_skill = request.form['pri_skill']
    location = request.form['location']
    emp_image_file = request.files['emp_image_file']

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    if emp_image_file.filename == "":
        return "Please select a file"

    try:
        cursor.execute(insert_sql, (emp_id, first_name, last_name, pri_skill, location))
        db_conn.commit()
        emp_name = f"{first_name} {last_name}"

        # Upload image file to S3
        emp_image_file_name_in_s3 = f"emp-id-{emp_id}_image_file.png"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(bucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image_file)
        except Exception as e:
            return str(e)

        # Generate the image URL
        image_url = generate_image_url(emp_id)

        print("All modifications done...")
        return render_template('AddEmpOutput.html', name=emp_name, image_url=image_url)
    finally:
        cursor.close()

@app.route("/getemp", methods=['GET', 'POST'])
def get_emp():
    if request.method == 'POST':
        emp_id = request.form.get('emp_id')  # Retrieve the employee ID from the form
        # Query the database to retrieve employee information based on the emp_id
        select_sql = "SELECT * FROM employee WHERE emp_id = %s"  # Adjust column name if necessary
        cursor = db_conn.cursor()
        cursor.execute(select_sql, (emp_id,))
        employee = cursor.fetchone()

        if employee:
            emp_id = employee[0]
            first_name = employee[1]
            last_name = employee[2]
            pri_skill = employee[3]
            location = employee[4]
            image_url = generate_image_url(emp_id)  # Assuming you have a function to generate the image URL
            return render_template('GetEmp.html', emp_id=emp_id, first_name=first_name, last_name=last_name, pri_skill=pri_skill, location=location, image_url=image_url)
        else:
            return "Employee not found"

    # Handle GET request (display the form)
    return render_template('GetEmp.html')


@app.route("/getempoutput", methods=['GET', 'POST'])
def get_emp_output():
    emp_id = request.form.get('emp_id')  # Retrieve the employee ID from the form
    # Query the database to retrieve employee information based on the emp_id
    select_sql = "SELECT * FROM employee WHERE emp_id = %s"
    cursor = db_conn.cursor()
    cursor.execute(select_sql, (emp_id,))
    employee = cursor.fetchone()

    if employee:
        emp_id = employee[0]
        first_name = employee[1]
        last_name = employee[2]
        pri_skill = employee[3]
        location = employee[4]
        image_url = generate_image_url(emp_id)  # Assuming you have a function to generate the image URL
        return render_template('GetEmpOutput.html', emp_id=emp_id, first_name=first_name, last_name=last_name, pri_skill=pri_skill, location=location, image_url=image_url)
    else:
        return "Employee not found"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
