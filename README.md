# Token-genereation-using-flask-UWSGI-and-k8s-using-two-namespaces

In the above code I have generated a JWT token.
I am storing user name and user password inside the MOngoDB.
 
I have created 2 api one for user data insertion and another for user login( user authentication).
 
To run the above code clone it and you have to only create a folder named modules an inside it craete a file name globals.py 
and paste the below lines inside it .

****************************************************************************
globals.py file content
****************************************************************************

SECRET_KEY = 'sultan-key' # IMPORTANT - change this to your own secret key
ACCESS_TOKEN_EXPIRES = 60 * 60  # 1 hr

****************************************************************************

I have deployed the entire code inside the kubernetes and I have used two namespace one for mongoDB named mydbnamespace
and another named mycurdappnamespace.

