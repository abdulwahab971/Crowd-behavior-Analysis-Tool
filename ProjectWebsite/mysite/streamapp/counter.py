import os,datetime
t = os.path.getmtime(r"C:\Users\Muhammad Ahsan\PycharmProjects\ProjectWebsite\mysite\streamapp\static\streamapp\results196.mp4")

x = str(datetime.datetime.fromtimestamp(t).time())
print(x)


