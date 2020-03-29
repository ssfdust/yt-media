#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Any, Dict, NoReturn

from flask import render_template_string
from flask_mail import Message

from smorest_sfs.extensions import mail
from smorest_sfs.modules.email_templates.models import EmailTemplate


class MailSender:
    def __init__(self, template_name: str = "", to: str = "", **kwargs: Any):
        self.template_name = template_name
        self.content = kwargs.get("content")
        self.subject = kwargs.get("subject", "Mail From Me")
        self.msg = Message(self.subject, recipients=[to])
        self.template_str = EmailTemplate.get_template(template_name)

    def send(self) -> NoReturn:
        self.msg.html = self.template_str
        mail.send(self.msg)


class PasswdMailSender(MailSender):
    def __init__(self, content, to: str = ""):
        super().__init__(
            template_name="reset-password",
            to=to,
            content=content,
            subject="Forget Passwd",
        )
