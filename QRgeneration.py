import pyqrcode

s = "222222/01/01/23/08/08/22/00001"
url = pyqrcode.create(s)

url.png('victor.png', scale=6)