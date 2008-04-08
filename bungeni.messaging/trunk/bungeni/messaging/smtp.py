import smtplib

import zope.sendmail.interfaces

class SMTPMailer(object):
    """A direct mailer for use with zope.sendmail."""

    interface.implements(zope.sendmail.interfaces.ISMTPMailer)

    def send(self, fromaddr, toaddrs, message):
        hostname = 'localhost'
        port = 25
        username = password = None

        connection = smtp.SMTP(hostname, port)

        # authenticate if needed
        if username is not None and password is not None:
            connection.login(username, password)

        connection.sendmail(fromaddr, toaddrs, message)
        connection.quit()
