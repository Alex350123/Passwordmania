PasswordMania is a two factor authentication prototype based on music recognition. New users should register with email and password. They can then import music authenticating part as the 2FA. 
After building their own music library, users will be asked to select correct title from 4 options based on the first second of the song. If they failed during any of the five questions, their login attempt will be denied. 
REQUIREMENTS

To run the project smoothly on your system, make sure the following requirements are met:

➢ You have Python3 but versions no newer than 3.10 installed on your system(3.9 is recommended), as all of the codings are done in python only.

➢ You have Node.js installed on your system

➢ You must have a good internet connection.

➢ You need to have at least one of these text editors (or IDEs) installed on your system: Visual
Studio Code, Pycharm, Anaconda (Jupyter or Spyder), or Atom.

Now, these are the basic software requirements, other than these, you just need to follow the instructions provided below to make sure the project works flawlessly on your system.

INSTRUCTIONS

After you’ve met the basic requirements, unzip and open the source code folder named "PasswordMania"  onto your text editor/IDE. For quick view of the prototype, we already save data in db.sqlite3. So to run this project, simply follow these instructions:

1. In the folder, you can see a file ‘requirements.txt’, this file contains all the modules that we used in python to work on the project, you’ll have to install them as well. To install all the modules in one go, open the python terminal, in that, open the project folder, and run the following command:


   pip install -r requirements.txt


This command will install all the required modules.

In order to load preview urls, install the folowing node packages through the following commands in the ternimal:

  npm install dotenv express cors spotify-preview-finder

and you’ll be good to go.

2. Now, to run the project on your localhost, enter the following command on your terminal:

    python manage.py runserver


Now, after this command, if you open localhost:8000 on your web browser, it should open our login page. 

To create a new user, you can simply register with information needed. We have these default users to quickly go through PasswordMania:

In http://localhost:8000/: 
email: lpy@outlook.com, password: 123456
In http://localhost:8000/admin/:
email: admin@outlook.com, password: 123456

To create a Manager User, enter the following command on your terminal:

    python manage.py createsuperuser

After entering username and password, you will be able to login as a manager in manager login page. For quick going through, you can use default manager user:
Manager User:
username: admin, password: 123456

If you login with customer account, you will be directed to customer home page where you can simply just use all of our functionalities, like booking a vehicle, reporting any fault, and returning the vehicle. If you login with operator acount, you can track vehicles, move them from one location to another, and charge them as well when they’re running low on power. For managers, a dashboard will be displayed which will render multiple reports. You can enter new vehicles , new station and new users as well if you log in as a manager. All the changes that happen on the localhostwebsite, will reflect on our database as well.

If you want to use this system with just your own data, follow these instructions:

1. open the python terminal, in that, open the project folder, and run the following command:

    pip install -r requirements.txt

2. delete db.sqlite3 file

3. run the following commands in this order, to migrate the SQL database onto your system:

    python model.py makemigrations

    python model.py migrate

after running these commands, the database should be synced with your system.

4. enter the following command on your terminal:

    python manage.py runserver

Now you should be able to run this project on your localhost


POSSIBLE ERROR ENCOUNTERS AND THEIR SOLUTION

A. Not being able to locate the manage.py file:
Go to the root directory using the command line and run the command:

    python manage.py runserver

This should solve the issue, and then check on localhost:8000 again.

B. User interface not loading properly:
Make sure that your system is connected to the internet and try again.


