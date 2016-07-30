# pyHamLog

This is an open source python 2.7 project started by [Scott Harden, AJ4VD](http://www.SWHarden.com), in 
support of logging for the ARRL School Club Roundup contest.

Currently, the code is maintined by Andrew Milluzzi, KK4LWR. Andrew is
president of the [Gator Amateur Radio Club] (http://gatorradio.org/) at the
University of Florida. Please email any bugs to andy@gatorradio.org.

While originally designed for the ARRL School Club Roundup, additional support
has been added to make the software more flexible. You can edit the length of
the contest and the times in the "genstats.py" page for the contest you are
working.

## installation
* Install python 2.7
* Clone repo to your computer
* Edit "genstats.py" to current contest start date
* Edit "databse.py" to create the correct log file including contest, class, 
   and callsign.
* Update IP address and port in "webserver.py" to configure software for your
   network. (port 80 is default for websites)
* Update HTML files for contest and callsign.
* Run "webserver.py"
* Go to [your IP]/adminsrock.html
* Click on "Logging Interface" to start logging.
* Get on the air!

### To generate stats
* Go to [your IP]/adminsrock.html
* Click on "Update Figures"

### To modify log
* Go to [your IP]/adminsrock.html
* Click on "Modify Log"
