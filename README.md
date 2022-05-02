# Capstone

This project is to work with clients to produce the Attendance tracking system they have formulated using the skills we have aquired over the years at university.

Python branch is the code that I worked on to have users make events and view the participants of that event.
  This website has the following features:
    A route to make QR codes.
    The ability to sign up users using email authentication and passwords salted and hashed with sha256.
    Add events that are restricted to the present and future dates, can only be a week long, can only have five active at one time, unique codes and names.
    Can update those events if they have not began yet.
    Can remove events -> will delete from database if it hasn't started yet otherwise only remove access to event. 
    Can click on event to go to query page then view all the people that match the filters set.

Android branch is the code to scan QR codes to submit proper QR codes to the database through the web app.
  This app has the following features:
    Arbitrary scanning based on code entered on the home screen.
    Can be either face or rear camera decided by home screen.
    Plays an incorrect noise when the website returns 'failure' or not connected to internet.
