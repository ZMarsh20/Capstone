import pyqrcode

s = "555555/1/1/21/8/8/22/#"

url = pyqrcode.create(s)

url.png('zach.png', scale=6)