'''
Created on Sep 3, 2015

@author: andre
'''

import smtplib as smtp
import mimetypes
import email
import sys
import socket
import email.mime.application
from PyQt4 import QtCore
import errno
from reportlab.pdfgen import canvas


class EmailClient(QtCore.QObject):
  ''' TODO - Description'''

  fromAddr        = None
  toAddr          = None
  smtpServerUrl   = None
  smtpServerPort  = None

  def __init__(self, smtp_url = 'smtp.gmail.com', smtp_port = 25, username = '', password = ''):
      ''' TODO - Description '''
      
      # This are the required fields to create a EmailClient 
      self.smtpServerPort = smtp_port # SMTP Server Port can be  25, 465, or 587
      self.smtpServerUrl = smtp_url   # SMTP Server Address, we assume to use the google smtp server 
      self.username = username        # SMTP account username
      self.password = password        # SMTP user password
      self.isSmtpOk = False
      


  def sendEmail(self, from_addr = '', to_addr = '', mail_subject = '', mail_body = '', attachment_path = None):
    ''' TODO - Description'''
    try:
      # This will try to send a HELO/EHLO command to check if the server is available, if not raises a exception
      self.smtpServer = smtp.SMTP('{0}:{1}'.format(self.smtpServerUrl, self.smtpServerPort)) 
      # This flag is set to True only if the previous command succeed
      self.isSmtpOk = True
      
      self.smtpServer.starttls()
      self.smtpServer.login(self.username, self.password)
      
          
      mail = email.mime.Multipart.MIMEMultipart()
      mail['Subject'] = mail_subject
      mail['From'] = from_addr
      mail['To'] = to_addr
      
      body = email.mime.Text.MIMEText(mail_body)
      mail.attach(body)
      
      if attachment_path:
        with open (attachment_path, 'r') as file_path:
          file_attachment = email.mime.application.MIMEApplication(file_path.read(), _subtype='pdf')        
        file_attachment.add_header('Content-Disposition', 'attachment', filename=file_attachment)
        mail.attach(file_attachment)
      
      self.smtpServer.sendmail(from_addr,[to_addr], mail.as_string())
      
    
    except smtp.SMTPSenderRefused as e:
      print "Please provide a valid e-mail address"
      print str(e)
      print e.recipients[0]
        
    except smtp.SMTPConnectError as e:
      print "Unable to connect to smtp server"
      print str(e)
      
    except smtp.SMTPAuthenticationError as e:
      print "Please provide the correct username/password combination"
      print str(e)
    
    except smtp.SMTPDataError as e:
      print "Unable to send the e-mail body message"
      print str(e)
    
    except smtp.SMTPResponseException as e:
      print "ERROR {0}: {1}".format(e.smtp_code, e.smtp_error)
      print str(e)
      
    except socket.timeout as e:
      print "Connection timeout"
      print str(e)
    
    except socket.gaierror as e:
      print "Please check your internet connection."
      print str(e)
    
    except IOError as (errno, strerror):
      if errno == errno.ENOENT:
        print "The file attachment does not exists"
      print "ERROR {0} - {1}".format(errno, strerror)
      
    except:
      print "Unexpected error:", sys.exc_info()[0]
      raise
        
    finally:
      if self.isSmtpOk:
        self.smtpServer.quit()
     
     


  def hello(self, c):
    c.drawString(100,100,"Hello World")
   
    

# FOR DEBUG AND TESTING
if __name__ == '__main__':
  
    mail_client = EmailClient()
    mail_client.username = "andre.silva@ola.eu"
    mail_client.password = "12345678"
    mail_client.sendEmail( mail_subject ="test",
                           from_addr="andre.silva@introsys.eu", 
                           to_addr="andre.silva@introsys.eu" ,
                           mail_body = "hey")
    
    c = canvas.Canvas("hello.pdf")
    mail_client.hello(c)
    c.showPage()
    c.save()
  
    