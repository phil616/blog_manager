from email.mime.base import MIMEBase

from core.logger import log
import aiosmtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from config import settings
from dataclasses import dataclass


@dataclass
class Attachment:
    filename: str
    content: bytes


async def send_email(
        host: str,
        port: int,
        username: str,
        password: str,
        subject: str,
        send_to_addr: str,
        contest_msg: str,
        text: str = 'plain',
        attachments: list[Attachment] = None
):
    server = aiosmtplib.SMTP(hostname=host, port=port, start_tls=True)
    await server.connect()

    await server.login(username, password)

    msg = MIMEMultipart()
    msg['From'] = Header(settings.EMAILS_FROM_EMAIL)  # 设置来自于邮件的发送者信息
    msg['To'] = Header(send_to_addr)  # 设置来自于邮件的接收人信息
    msg['Subject'] = Header(subject, 'utf-8')  # 设置邮件主题

    msg.attach(MIMEText(contest_msg, text, 'utf-8'))

    if attachments:
        for attachment in attachments:
            filename = attachment.filename
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.content)
            part.add_header('Content-Disposition', 'attachment', filename=filename)
            encoders.encode_base64(part)
            msg.attach(part)
    log.info(f"Sending email to {send_to_addr} with subject {subject}")
    await server.sendmail(settings.EMAILS_FROM_EMAIL, send_to_addr, msg.as_string())
    await server.quit()
