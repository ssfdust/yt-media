#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import pytest


class FixturesInjectBase:

    fixture_names = ()

    @pytest.fixture(autouse=True)
    def auto_injector_fixture(self, request):
        names = self.fixture_names
        for name in names:
            setattr(self, name, request.getfixturevalue(name))
