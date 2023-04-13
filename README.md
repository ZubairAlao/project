# CAMPUS HELPDESK
#### Video Demo:  <https://youtu.be/JfdqHv_XJek>
#### Description: Campus Helpdesk is a web application that allows students to submit complaints or requests related to campus facilities or services, and allows campus administrators to manage and respond to those complaints.

## Requirements
- cs50
- Flask
- Flask-Session
- requests

## How to Use
- Navigate to your project and run **flask run** to run on CS50 CodeSpace
- if you want to run it on your local system i recomemend you
    - Create and activate a Python virtual environment
    - Install with pip install -r requirements.txt
    - you can also run it with **flask run** on your local system

## To use the application, follow these steps:
#### Users
- Visit the login page and enter your username and password (or signup a new account if you don't have one yet).
- Make Complains by clicking on **Make Complain** link on navbar fill out the form and submit
- Once you have made the complain, you will see a list of any complaints or requests you have submitted in a tabular form that contain subject, description, status of reply(replied or not) and action to open chat or delete message.
- To submit a new complaint or request, click the **Make Complain** button and fill out the form to submit.
- There is also a **Open Chat** link on the navbar and **open reply** on the complaints table where you can have a better view of complaints, time submitted, subject and description of the complain with option to delete if admin have not answer it and status to show if admin have replied or not.

#### Admin
- Campus administrators will be able to see all complaints or requests submitted by users, and can respond to them by typing reply and clicking on the **reply complaints**.
- The complaints are ordered by first messages to arrive and top most priority given to not answered question to be at the topmost of the list
- Admin can delete reply when mistake is made.

## Features of Campus Helpdesk includes the following features:

- User authentication and authorization
- Ability for students to submit complaints or requests
- Ability for administrators to view and respond to complaints or requests
- Responsive design for use on mobile devices

## implementation of the Campus Helpdesk
The Campus Helpdesk made used of 3 tables in the database, users for storing usernames and password, complaints for storing complaints and replies for answering compliants.

The Campus Helpdesk application has a few routes such as:
     default page, /open, /login, /logout, /complaints, /index, /admin, and /reply.

#### The sign up route:
The sign up allows user to sign up, it collect their usersname and password, the username must not exist in the database and the password and confirm password must match. if correct it insert the data into the users table in the database.

#### The /login route:
Allows users to log in with their username and password. It checks if the username exists in the database and verifies the password. If the user is an admin, they are redirected to /admin else, they are redirected to /index route.

#### The /logout route:
Logs out the user and redirects them to the login page.

#### The index
The index page has list of complaints from current users by selecting users, complaints and replies where user_id is current login user. it also as delete form request to delete complaints

#### The /complaints route:
Allows users to make complaints by entering a subject and description. If the input is valid, the complaint is inserted into the database.

#### The /admin route:
This is the admin page where all user complaints go to, selecting from the three tables and ordering them on order of not replied or replied and time submitted without delete request.

#### The /open route:
Shows a better view of the tabled structure in index page, option to delete complaints and allows them to make new request to admin.

#### The /reply route:
Allows users to reply to complaints by entering a message and the complaint ID. The message and user ID are inserted into the replies table in the database with a foreign key relationship to the complaints table.

##### The about:
About school and Helpdesk information


