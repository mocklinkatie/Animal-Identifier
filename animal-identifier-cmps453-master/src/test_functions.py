import pytest

from backend import accepted_filetypes
from backend import validEmailForm, clenseEmail
from backend import classifyImage
from backend import ALLOWED_EXTENSIONS, class_names

#ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
DISALLOWED_EXTENSIONS = {'pdf', 'bat', 'sh', 'exe', 'odt', 'doc'}

def test_filetype_allowed():
    for ext in ALLOWED_EXTENSIONS:
        assert(accepted_filetypes('x.'+ext) == True)

def test_filetype_disallowed():
    for ext in DISALLOWED_EXTENSIONS:
        assert(accepted_filetypes('x.'+ext) == False)
        
GOOD_EMAIL_ADDRS = {'abc@gmail.com', 'def.ghi@yahoo.com', 'xyz@myserver.de'}
BAD_EMAIL_ADDRS = {'abc def@xyz.com', 'abc@xyz .com', 'abc@@gmail.com'}
UNCLEAN_EMAIL_ADDRS = {'   abc@gmail.com    ', '   def@gmail.com', 'xyz@yahoo.com   '}

def test_validEmail_goodform():
    for email in GOOD_EMAIL_ADDRS:
        assert(validEmailForm(email) == True)

def test_validEmail_badform():
    for email in BAD_EMAIL_ADDRS:
        assert(validEmailForm(email) == False)


def test_clenseEmail():
    for email in UNCLEAN_EMAIL_ADDRS:
        assert(clenseEmail(email) == email.strip())

GOOD_ANIMALS = {'elephant.jpg'}
BAD_ANIMALS = {'peacock.jpg', 'squid.jpg', 'whale.jpg'}

def test_classifyImage_Good():
    for pic in GOOD_ANIMALS:
        print(classifyImage('./uploads/'+pic))
        assert(class_names[classifyImage('./uploads/'+pic)[0]] == pic.split('.')[0])

def test_classifyImage_Bad():
    for pic in BAD_ANIMALS:
        print(classifyImage('./uploads/'+pic))
        assert(class_names[classifyImage('./uploads/'+pic)[0]] != pic.split('.')[0])


        
