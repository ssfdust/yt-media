#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Any, Mapping

from flask import render_template_string
from flask_mail import Message

from smorest_sfs.extensions import mail
from smorest_sfs.modules.email_templates.models import EmailTemplate


class MailSender:
    def __init__(self, template_name: str = "", to: str = "", **kwargs: Any):
        self.template_name = template_name
        self.content: Mapping[str, Any] = kwargs.get("content", {})
        self.subject: str = kwargs.get("subject", "Mail From Me")
        self.msg: Message = Message(self.subject, recipients=[to])
        self.template_str: str = EmailTemplate.get_template(template_name)

    def send(self) -> None:
        self.msg.html = render_template_string(self.template_str, **self.content)
        mail.send(self.msg)


class PasswdMailSender(MailSender):
    def __init__(self, content: Any, to: str = ""):
        super().__init__(
            template_name="reset-password",
            to=to,
            content=content,
            subject="Forget Passwd",
        )
