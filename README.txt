To run the server execute
1.cd [SmartOrder or the project directory name] ( outer directory containing manage.py)
2.check for the serial port used and change it in readWeight.py(open readWeight.py in an editor)
3.python3 readWeight.py &
4.python3 manage.py runserver 0.0.0.0:8000

5.Can also use 'minicom -D '/dev/<ttyport used>' -b <baud rate ex: 9600> to check if serial data is being recieved.


------------------:Fixing Known bugs:-------------------
For Unix/Linux if server time is wrong then to change it:
NOTE: This is if the timer on the order acknowledgement page shows 'get your order' as soon as completed.
1.Goto SmartOrder/settings.py
2.Change TIME_ZONE = 'Asia/Kolkata'
3.Change USE_TZ = True
4.Restart the server

it worked for me...hope it works for you to.

this version has timer on order acknowledgement page