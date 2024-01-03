from pathlib import Path
from typing import Any

import emails
from celery import shared_task
from celery.utils.log import get_task_logger
from emails.template import JinjaTemplate

from app.core.config import settings

logger = get_task_logger("tasks")


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: dict[str, Any] | None = None,
) -> None:
    environment = environment or {}
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logger.info("Send %s mail to %s - result: %s", subject_template, email_to, response)


@shared_task
def send_test_email(email_to: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test"
    path = Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html"
    with path.open() as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": settings.PROJECT_NAME, "email": email_to},
    )


@shared_task
def send_new_account_email(email_to: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account"

    path = Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html"
    with path.open() as f:
        template_str = f.read()
    link = f"{settings.SERVER_HOST}register?token={token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "email": email_to,
            "valid_hours": settings.EMAIL_VALIDATION_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


@shared_task
def send_reset_password_email(email_to: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery"
    path = Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html"
    with path.open() as f:
        template_str = f.read()
    link = f"{settings.SERVER_HOST}reset-password?token={token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "email": email_to,
            "valid_hours": settings.EMAIL_VALIDATION_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )
