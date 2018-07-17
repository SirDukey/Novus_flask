#!/opt/rh/rh-python36/root/usr/bin/python3 

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


def myftpserv():
    authorizer = DummyAuthorizer()
    authorizer.add_user('library', 'library', '/Novus_flask/downloaded', perm='elradfmwMT')
    authorizer.add_anonymous('/Novus_flask/downloaded')
    handler = FTPHandler
    handler.authorizer = authorizer
    address = ('', 2121)
    server = FTPServer(address, handler)
    server.serve_forever()


if __name__ == '__main__':
    myftpserv()
