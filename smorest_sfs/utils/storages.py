#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Union, TypeVar
from pathlib import Path
from werkzeug.datastructures import FileStorage
import mimetypes
from .paths import ProjectPath, make_uploaded_path, get_relative_pathstr, UploadPath
import os

Response = TypeVar("Response")


def load_storage_from_path(filename: str, path: Union[Path, str]) -> FileStorage:
    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    file_pointer = open(ProjectPath.get_subpath_from_project(path), "rb")
    return FileStorage(file_pointer, filename, "file", content_type)


def save_storage_to_path(store: FileStorage, subdir: str) -> str:
    path = make_uploaded_path(subdir)
    store.stream.seek(0)
    store.save(path)
    store.stream.seek(0)
    return get_relative_pathstr(path)


def delete_from_rel_path(path: Union[Path, str]):
    filepath = ProjectPath.get_subpath_from_project(path)
    if filepath.exists() and not UploadPath.if_in_whitelst(filepath):
        os.remove(filepath)


from flask import send_file


def make_response_from_store(store: FileStorage) -> Response:
    return send_file(
        store.stream,
        attachment_filename=store.filename,
        mimetype=store.content_type,
        as_attachment=False,
    )


def make_response_from_path(filename: str, path: Union[Path, str]) -> Response:
    store = load_storage_from_path(filename, path)
    return make_response_from_store(store)
