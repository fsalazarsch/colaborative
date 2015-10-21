import smtplib
import urllib.request
from datetime import datetime

def send_mail(addressee, subject, message):
  username = 'service@hit-map.com'
  password = '4JdYHLZC'
  fromaddr = 'service@hit-map.com'

  message = 'Subject: %s\n\n%s' %(subject, message)

  server = smtplib.SMTP('smtp.gmail.com:587')
  server.starttls()
  server.login(username,password)
  server.sendmail(fromaddr, addressee, message)
  server.quit()



def download_data(url):
  request = urllib.request.Request(url)
  response = urllib.request.urlopen(request)
  html = response.read().decode('utf-8')
  return html


def now():
  ret = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  return ret


def validate_email(string):
  if string.find('.') < 0:
    return False
  if string.find('@') < 0:
    return False
  return True


