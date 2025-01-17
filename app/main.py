import logging
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from .models import EmailMessage
from .email import send_email
from .config import settings

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Portfolio Email Service")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://portfolio-mequeiras-projects.vercel.app",
        "http://localhost:3000"  # Para desenvolvimento local
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar autenticação por API Key
api_key_header = APIKeyHeader(name="X-API-Key")

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == settings.API_KEY:
        return api_key
    raise HTTPException(
        status_code=401,
        detail="API Key inválida"
    )

@app.post("/send-email")
async def send_contact_email(
    email_data: EmailMessage,
    api_key: str = Depends(get_api_key)
):
    """
    Envia um email de contato do portfolio.
    """
    try:
        success = send_email(
            name=email_data.name,
            email=email_data.email,
            message=email_data.message
        )

        if success:
            logger.info(f"Email enviado com sucesso de {email_data.email}")
            return {"message": "Email enviado com sucesso"}
        else:
            raise HTTPException(
                status_code=500,
                detail="Erro ao enviar email"
            )

    except Exception as e:
        logger.error(f"Erro ao processar email: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar email: {str(e)}"
        )
