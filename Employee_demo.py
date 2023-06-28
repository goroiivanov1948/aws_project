from flask import Flask, render_template, request, redirect, url_for
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

output = {}
table = 'employee'


@app.route("/", methods=['GET', 'POST'])
def home():
    return redirect(url_for('get_emp'))


@app.route("/getemp", methods=['GET', 'POST'])
def get_emp():
    # Logic to retrieve employee information from the database
    # Populate variables with employee data
    id = request.form['emp_id']
    fname = request.form['fname']
    lname = request.form['lname']
    interest = request.form['pri_skill']
    location = request.form['location']
    image_url = request.files['image_url']

    return render_template('GetEmp.html', id=id, fname=fname, lname=lname, interest=interest, location=location, image_url=image_url)


@app.route("/getempoutput", methods=['GET', 'POST'])
def get_emp_output():
    # Logic to retrieve employee information from the database
    # Populate variables with employee data
    id = request.form['emp_id']
    fname = request.form['fname']
    lname = request.form['lname']
    interest = request.form['pri_skill']
    location = request.form['location']
    image_url = request.files['image_url']

    return render_template('GetEmpOutput.html', id=id, fname=fname, lname=lname, interest=interest, location=location, image_url=image_url)


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
        emp_name = "" + first_name + " " + last_name

        # Upload image file to S3
        emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image_file)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                emp_image_file_name_in_s3)

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("All modifications done...")
    return render_template('AddEmpOutput.html', name=emp_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)