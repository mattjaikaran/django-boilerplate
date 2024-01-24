from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
import logging

from api.settings import _env_get_required

logger = logging.getLogger(__name__)

# How to use this function:
# add all args to provide clarity on what is needed
# subject, template, send_from, send_to, context={}, bcc_emails=[]
# subject and template are stored in the templates folder
# create a new folder to keep all email templates organized

# Ex:
# send_html_email(
#     subject=login_subject,
#     template="auth/login_email.html",
#     send_from=_env_get_required("SUPPORT_EMAIL"),
#     send_to=[context["email"]],
#     context=context,
# )


def send_html_email(subject, template, send_from, send_to, context={}, bcc_emails=[]):
    """Generic sender to build and send an HTML email with a plain-text fallback.
    Args:
        subject (str): Subject of the email.
        template (str): Path to the HTML template to use for this email. Use the Django
            template loader path.
        send_from (str): The email address of the sender.
        send_to (str or list of str): Email address(es) of recipients.
        context (dict, optional): Dictionary of context variables needed to render
            the HTML template. Defaults to an empty :obj:`dict`.
        bcc_emails (list of str, optional): List of email addresses to BCC
            on the email. Defaults to an empty :obj:`list`.
    Returns: None
    """
    assert isinstance(
        send_to, (list, tuple, str)
    ), "send_to must be an instance of list, tuple, or str"

    if isinstance(send_to, str):
        send_to = [send_to]

    # Email subject *must not* contain newlines
    subject = "".join(subject.splitlines())

    # Render HTML and use premailer transform to force inline CSS
    html_body = render_to_string(template, context)

    plaintext_body = (
        "This is an HTML email. If you can read this, then "
        "your email client does not support HTML emails. "
        "Please contact us at {0} to report the problem.".format(settings.SERVER_EMAIL)
    )

    email = EmailMultiAlternatives(
        subject,
        plaintext_body,
        send_from,
        send_to,
        bcc_emails,
    )

    email.attach_alternative(html_body, "text/html")
    email.send(fail_silently=False)


# password reset email
def send_password_reset_email(context):
    print(f"context in send_password_reset_email => {context}")
    subject_context = {
        "environment": settings.ENVIRONMENT.upper(),
        "user_email": context["email"],
        "password_link": context["password_link"],
    }
    password_reset_subject = render_to_string(
        "auth/password_reset_subject.txt", subject_context
    )
    send_html_email(
        subject=password_reset_subject,
        template="auth/password_reset_email.html",
        send_from=_env_get_required("SUPPORT_EMAIL"),
        send_to=[context["email"]],
        context=context,
    )


# create email to support team (from support team) when a new conversation is created
# def send_conversation_create_email(context):
#     print(f"context in send_conversation_create_email => {context}")
#     subject_context = {
#         "environment": settings.ENVIRONMENT.upper(),
#         "recipient": context["recipient"],
#         "sender": context["sender"],
#     }
#     conversation_create_subject = render_to_string(
#         "conversation/conversation_create_subject.txt", subject_context
#     )
#     send_html_email(
#         subject=conversation_create_subject,
#         template="conversation/conversation_create_email.html",
#         send_from=_env_get_required("SUPPORT_EMAIL"),
#         send_to=_env_get_required("SUPPORT_EMAIL"),
#         context=context,
#     )


# create email to support team (from support team) when a new property is created
# def send_property_create_email(context):
#     print(f"context in send_property_create_email => {context}")
#     subject_context = {
#         "environment": settings.ENVIRONMENT.upper(),
#         # "user_email": context["user_email"],
#         "property_name": context["property_name"],
#     }
#     property_create_subject = render_to_string(
#         "property/property_create_subject.txt", subject_context
#     )
#     send_html_email(
#         subject=property_create_subject,
#         template="property/property_create_email.html",
#         send_from=_env_get_required("SUPPORT_EMAIL"),
#         send_to=_env_get_required("SUPPORT_EMAIL"),
#         context=context,
#     )


# create email to support team (from support team) when a user contacts support
def send_support_email(context):
    print(f"context in send_support_email => {context}")
    subject_context = {
        "environment": settings.ENVIRONMENT.upper(),
        "user_email": context["user_email"],
        "message": context["message"],
    }
    support_subject = render_to_string("support/support_subject.txt", subject_context)
    send_html_email(
        subject=support_subject,
        template="support/support_email.html",
        send_from=_env_get_required("SUPPORT_EMAIL"),
        send_to=_env_get_required("SUPPORT_EMAIL"),
        context=context,
    )


# wip
def send_user_login_email(context):
    print(f"context in send_user_login_email => {context}")
    subject_context = {
        "environment": settings.ENVIRONMENT.upper(),
        "user_email": context["email"],
    }
    login_subject = render_to_string("auth/login_subject.txt", subject_context)
    send_html_email(
        subject=login_subject,
        template="auth/login_email.html",
        send_from=_env_get_required("SUPPORT_EMAIL"),
        send_to=[context["email"]],
        context=context,
    )
