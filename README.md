pyHamLog
========

This is an open source python 2.7 project started by Scott Harden, AJ4VD, in 
support of logging for the ARRL School Club Roundup contest.

Currently, the code is maintined by Andrew Milluzzi, KK4LWR. Andrew is
president of the [Gator Amateur Radio Club] (gatorradio.org) at the
University of Florida. Please email any bugs to andy@gatorradio.org.

While originally designed for the ARRL School Club Roundup, additional support
has been added to make the software more flexible. You can edit the length of
the contest and the times in the "genstats.py" page for the contest you are
working.

Instructions:
1. Install python 2.7
2. Clone repo to your computer
3. Edit "genstats.py" to current contest start date
4. Edit "databse.py" to create the correct log file including contest, class, 
   and callsign.
5. Update IP address and port in "webserver.py" to configure software for your
   network. (port 80 is default for websites)
6. Update HTML files for contest and callsign.
7. Run "webserver.py"
8. Go to [your IP]/adminsrock.html
9. Click on "Logging Interface" to start logging.
10. Get on the air!

To generate stats:
1. Go to [your IP]/adminsrock.html
2. Click on "Update Figures"

To modify log:
1. Go to [your IP]/adminsrock.html
2. Click on "Modify Log"
