from schemas.email import EmailInfo
import re
from aiosmtplib import SMTP
from settings import settings


class EmailService():
    """
    Сервис для работы с результатами
    """

    async def mass_send_email(self, email_info: EmailInfo):
        """Осуществить рассылку"""
        
        message = email_info.text
        
        sender_email = settings.email.address
        
        async with SMTP(hostname='smtp.gmail.com', port=587) as smtp:
            print(settings.email.address)
            print(settings.email.password)
            await smtp.login(sender_email, settings.email.password)
            for receiver in email_info.to:
                if self.is_valid_email(receiver):
                    await smtp.sendmail(sender_email, receiver, message)


    def is_valid_email(self, email: str):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_regex, email):
            return True
        else:
            return False