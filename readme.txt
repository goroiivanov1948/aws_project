//connecting to ec2 instance via ssh//
ssh -i "fmi_ubuntu_key.pem" ubuntu@ec2-44-202-3-14.compute-1.amazonaws.com

sudo apt-get update

sudo apt-get install mysql-client

//connecting to mysql//
mysql -h employee-database.c6t3wgjsr0uv.us-east-1.rds.amazonaws.com -u goroiivanov -p

show databases;
create database employee;
use employee;

create table employee(
empid varchar(20),
fname varchar(20),
lname varchar(20),
pri_skill varchar(20),
location varchar(20));

show tables;
exit

logout


# For python and related frameworks

sudo apt-get install python3
sudo apt-get install python3-flask
sudo apt-get install python3-pymysql
sudo apt-get install python3-boto3

# for running application
sudo python3 Empapp.py