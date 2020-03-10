#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from flask import Flask


@pytest.fixture(scope="package")
def app() -> Flask:

    return Flask("TestMa")
