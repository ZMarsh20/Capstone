import pyqrcode

s = "555555/male/white/21/cs/2022"

url = pyqrcode.create(s)

url.svg("zach.svg", scale=8)
url.png('zach.png', scale=6)
