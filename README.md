# webAPI_research_project
A flask application that uses the YNAB.com and Twilio REST web APIs to modify and send budget data to my phone.

The topic of Web Service APi's was chosen as my research project while studying
at the University of South Carolina Upstate during Fall 2018, my last semester at the school.
I made an "A" grade on this assignment. The class was CSCI 599 with Dr. Wei Zhong as professor. 

The Pipfile contains the dependency information needed to run this project. You'll need flask, requests, and a few other things. If you clone this repository, just run "pipenv install" at the top level directory. Pipenv will see the dependencies in the Pipfile and reconcile anything that is not found in the Pipfile.lock file. 

Once the above is complete, open a command prompt. Assuming you have Python 3.6 already installed, you can run...
"python wsgi.py" at the command-line. This will run the flask development server and will launch the application. 

This flask application is not intended or written for production. The front end is not user friendly at all and really isn't meant to be, but feel free to build your own if you would like. 

Since there is no front end to help you along, please see the "routing.py" file for URLs. Or you can use this list:

127.0.0.1/
127.0.0.1/recent-transactions
127.0.0.1/edit-transaction
127.0.0.1/update-transaction
