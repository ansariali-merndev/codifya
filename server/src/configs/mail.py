from fastapi_mail import MessageSchema, FastMail
from fastapi_mail import ConnectionConfig
from env import GMAIL_PASS, GMAIL_USER
from datetime import datetime

conf = ConnectionConfig(
    MAIL_USERNAME=GMAIL_USER,
    MAIL_PASSWORD=GMAIL_PASS,
    MAIL_FROM=GMAIL_USER,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_mail(email, otp):
    body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Verify your email</title>
    </head>
    <body style="margin:0; padding:0; background-color:#f6f9fc; font-family:Arial, sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0" style="padding:20px 0;">
            <tr>
                <td align="center">
                    <table width="480" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:12px; padding:30px;">
                        
                        <tr>
                            <td align="center" style="padding-bottom:20px;">
                                <h2 style="margin:0; color:#111;">Codifya</h2>
                                <p style="margin:0; color:#888; font-size:14px;">Secure Account Verification</p>
                            </td>
                        </tr>

                        <tr>
                            <td style="color:#333; font-size:15px; line-height:1.6;">
                                Hello,
                                <br/><br/>
                                Thank you for signing up with Codifya.
                                To complete your registration, please verify your email address using the One-Time Password (OTP) below.
                            </td>
                        </tr>

                        <tr>
                            <td align="center" style="padding:25px 0;">
                                <div style="display:inline-block; padding:15px 30px; font-size:26px; letter-spacing:6px; font-weight:bold; color:#2563eb; background:#f1f5ff; border-radius:8px;">
                                    {otp}
                                </div>
                            </td>
                        </tr>

                        <tr>
                            <td style="color:#555; font-size:14px; line-height:1.6;">
                                This OTP is valid for a limited time and should not be shared with anyone.
                                <br/><br/>
                                If you did not initiate this request, you can safely ignore this email.
                            </td>
                        </tr>

                        <tr>
                            <td style="padding-top:25px; border-top:1px solid #eee; font-size:12px; color:#999;">
                                Need help? Contact our support team.
                                <br/>
                                © {datetime.now().year} Codifya. All rights reserved.
                            </td>
                        </tr>

                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    message = MessageSchema(
        subject="Verify your email address",
        recipients=[email],
        body=body,
        subtype="html",
    )

    fm = FastMail(conf)
    await fm.send_message(message)
