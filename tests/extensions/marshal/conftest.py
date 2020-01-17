#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest


@pytest.fixture(scope="package")
def app():
    from flask import Flask

    return Flask("TestMa")
