#!/usr/bin/env python
# -*- coding: utf-8 -*-
from smorest_sfs.modules.email_templates.models import EmailTemplate


def test_get_template(flask_app):
    name = str(EmailTemplate.create(name="test", template="111"))
    assert name == "test" and EmailTemplate.get_template(name) == "111"
