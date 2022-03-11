import pyqrcode

s = "555555/01/01/21/08/08/22/"

url = pyqrcode.create(s)

url.png('zach.png', scale=6)