#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from werkzeug.datastructures import FileStorage
from smorest_sfs.modules.storages.models import Storages
import io


@pytest.fixture
def store():
    return FileStorage(io.BytesIO(b"abc"), "test.txt", "file", "text/txt")


@pytest.fixture
def storage(store):
    return Storages(name="test.txt", storetype="foo", store=store)


@pytest.fixture
def next_store():
    return FileStorage(io.BytesIO(b"efg"), "test.txt", "file", "text/txt")
