'''
Created on Sep 3, 2015

@author: andre
'''

import smtplib as smtp
import mimetypes #@UnusedImport
import email #@UnusedImport
import logging
import sys
import socket
import errno
from reportlab.pdfgen import canvas
from email.mime.application import MIMEApplication
from bzrlib.osutils import basename


class EmailClient(object):
  ''' TODO - Description'''



  def __init__(self, smtp_url = 'smtp.gmail.com', smtp_port = 25, username = '', password = ''):
      ''' TODO - Description '''
      self.f_log = logging.getLogger('App') # this can be called in any place
      # This are the required fields to create a EmailClient 
      self.smtpServerPort = smtp_port # SMTP Server Port can be  25, 465, or 587
      self.smtpServerUrl = smtp_url   # SMTP Server Address, we assume to use the google smtp server 
      self.username = username        # SMTP account username
      self.password = password        # SMTP user password
      self.isSmtpOk = False
  # --------------------------------------------------------------------------      


  def sendEmail(self, from_addr = '', to_addr = '', mail_subject = '', mail_body = '', attachment = None):
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
      if attachment:
        with open (attachment, 'r') as file_path:
          mail.attach(MIMEApplication(file_path.read(), \
                                      Content_Disposition='attachment; filename="{0}"'.format(basename(attachment)),\
                                      Name=basename(attachment)))
          
      self.smtpServer.sendmail(from_addr,[to_addr], mail.as_string())
    except smtp.SMTPSenderRefused as e:
      self.f_log.error("Please provide a valid e-mail address [{1}] - {0}".format(str(e), e.recipients[0]))
    except smtp.SMTPConnectError as e:
      self.f_log.error("Unable to connect to smtp server [{0}]".format(str(e)))
    except smtp.SMTPAuthenticationError as e:
      self.f_log.error("Please provide the correct username/password combination [{0}]".format(str(e)))    
    except smtp.SMTPDataError as e:
      self.f_log.error("Unable to send the e-mail body message [{0}]".format(str(e)))    
    except smtp.SMTPResponseException as e:
      self.f_log.error("ERROR {0}: {1}".format(e.smtp_code, e.smtp_error))      
    except socket.timeout as e:
      self.f_log.error("Connection timeout [{0}]".format(str(e)))
    except socket.gaierror as e:
      self.f_log.error("Please check your internet connection [{0}]".format(str(e)))
    except IOError as (errno, strerror):
      if errno == errno.ENOENT:
        self.f_log.error("The file attachment does not exists")
      self.f_log.error("ERROR {0} - {1}".format(errno, strerror))
    except:
      self.f_log.error("Unexpected error:", sys.exc_info()[0])
      raise
    finally:
      if self.isSmtpOk:
        self.smtpServer.quit()     
  # --------------------------------------------------------------------------   


  def hello(self, c):
    c.drawString(100,100,"Hello World")
   
  # --------------------------------------------------------------------------

# FOR DEBUG AND TESTING
if __name__ == '__main__':
  
    mail_client = EmailClient()
    mail_client.username = "ds.asd@sad.eu"
    mail_client.password = "blablablalba"
    mail_client.sendEmail( mail_subject ="test",
                           from_addr="asd.ds@sda.eu", 
                           to_addr="asd.dsa@asd.eu" ,
                           mail_body = "hey",
                           attachment_path ="att.pdf")
    
    c = canvas.Canvas("hello.pdf")
    mail_client.hello(c)
    c.showPage()
    c.save()
  # --------------------------------------------------------------------------
    
# EOF