# Social Network Web App

Hi there! Thank you for checking out my social networking web app!
It works pretty similar to twitter, except that you can edit your posts ;).
Also there is a bug with the like feature that is being worked on!

## How to Run

This is a python project. The best way to run this would be to click on the green button that says
"code" above and choose to download as a zip file. Once you have downloaded, you can extract the file
into the folder of your choice. From here, open up your terminal and cd into the folder you
extracted the project into. Lastly, run "python manage.py runserver" in order to run the server.

## Tools used

I used Python and the Django framework for the backend and some of the templates (Django made it pretty easy to implement pagination), and all the data from each post was stored in the sqlite database that came with Django. From there, I just used plain Vanilla JS in order to do PUT, POST, and DELETE methods from the client side. The rest is just HTML and CSS.
In addition to this, I also used the selenium webdriver in order to add a bunch of posts all at once, so that the pagination feature could be tested (you can find this in the test.py file).
