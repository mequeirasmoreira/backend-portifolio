import logging
import emails
from emails.template import JinjaTemplate
from .config import settings

logger = logging.getLogger(__name__)

def send_email(
    name: str,
    email: str,
    message: str,
) -> bool:
    try:
        # Configurar o email
        email_message = emails.Message(
            subject=f"Nova mensagem do portfolio de {name}",
            html=JinjaTemplate("""
                <p><strong>Nome:</strong> {{ name }}</p>
                <p><strong>Email:</strong> {{ email }}</p>
                <p><strong>Mensagem:</strong></p>
                <p>{{ message }}</p>
            """),
            mail_from=(settings.SMTP_FROM_EMAIL)
        )

        # Enviar o email
        response = email_message.send(
            to=settings.SMTP_TO_EMAIL,
            render={
                "name": name,
                "email": email,
                "message": message,
            },
            smtp={
                "host": settings.SMTP_HOST,
                "port": settings.SMTP_PORT,
                "user": settings.SMTP_USERNAME,
                "password": settings.SMTP_PASSWORD,
                "tls": True,
            },
        )

        logger.info(f"Email enviado para {settings.SMTP_TO_EMAIL}")
        return response.status_code == 250

    except Exception as e:
        logger.error(f"Erro ao enviar email: {str(e)}")
        return False
