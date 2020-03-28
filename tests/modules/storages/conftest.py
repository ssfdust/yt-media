#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io

import pytest
from werkzeug.datastructures import FileStorage

from smorest_sfs.modules.storages.models import Storages
from smorest_sfs.services.storages.handlers import StorageFactory


@pytest.fixture
def store():
    return FileStorage(io.BytesIO(b"abc"), "test.txt", "file", "text/txt")


@pytest.fixture
def storage(store):
    return Storages(name="test.txt", storetype="foo", store=store)


@pytest.fixture
def next_store():
    return FileStorage(io.BytesIO(b"efg"), "test.txt", "file", "text/txt")

@pytest.fixture
def add_storage(store):
    factory = StorageFactory(Storages(name="test.txt", storetype="foo", store=store))
    return factory.save()
