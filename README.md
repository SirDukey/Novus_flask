# Novus_flask

## Flask application used for deliver scrapers.

The application can deliver the scraped content to the user via ftp using the myftpserver.py application. Set the username/pass for ftp access in myftpserver.py Copy the *.service files to /etc/systemd/system/ to run the applications as a service.

Monitor the applications using journalctl -u Novus_flask or journalctl -u myftpserver

## Dependancies:

1. Python3 
2. Selenium python module 
3. Google chrome   *Google chrome relies on a desktop env like gnome even in headless mode 
4. selenium chromedriver installed in /usr/bin/ 
5. Pillow python module 
6. pyftpdlib python module
7. Flask python module

