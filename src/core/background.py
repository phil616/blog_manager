from config import settings
from core.dependencies import g_global_kv
from lib.aioemail import send_email, Attachment
from core.logger import log


async def export_file_to_email(filename: str, message:str,content: str, send_to: str, bg_id: str):
    try:
        g_global_kv.set_value("bg_task_" + bg_id, "running")
        await send_email(
            settings.SMTP_HOST,
            int(settings.SMTP_PORT),
            settings.SMTP_USER,
            settings.SMTP_PASSWORD,
            subject=f"Export file {filename}",
            send_to_addr=send_to,
            contest_msg=message,
            text='plain',
            attachments=[Attachment(filename=filename, content=content.encode('utf-8'))]
        )
        g_global_kv.set_value("bg_task_" + bg_id, "done")
    except Exception as e:
        g_global_kv.set_value("bg_task_" + bg_id, "error")
        log.error(f"Error while sending email: {e}", exc_info=True)


async def bg_send_email():
    ...


async def bg_migrate_database():
    ...


async def bg_wait():
    ...


async def bg_factory(task_id: str, func: callable, /, **kwargs):
    g_global_kv.set_value("bg_task_" + task_id, "running")
    await func(**kwargs)
