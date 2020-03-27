#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import date
from pathlib import Path
from uuid import uuid4

import smorest_sfs

from .datetime import utctoday

UPLOADS = "uploads"

def datetopath(datestr: str) -> Path:
    return Path(*datestr.split('-'))

def todaytopath() -> Path:
    today = utctoday()
    return datetopath(str(today))


class ProjectPath:
    @classmethod
    def __get_sfs_path(cls) -> Path:
        return getattr(smorest_sfs, "__path__")[0]

    @classmethod
    def get_project_path(cls) -> Path:
        sfs_path = Path(cls.__get_sfs_path())
        return sfs_path.parent


class UploadPath(ProjectPath):
    @classmethod
    def get_uploads_path(cls) -> Path:
        project_path = cls.get_project_path()
        return cls._get_uploads_path(project_path)

    @classmethod
    def _get_uploads_path(cls, project_path: Path) -> Path:
        return project_path.joinpath(UPLOADS)

    @classmethod
    def get_uploads_subdir(cls, subname: str) -> Path:
        uploads_path = cls.get_uploads_path()
        return cls._get_uploads_subdir(uploads_path, subname)

    @classmethod
    def _get_uploads_subdir(cls, uploads_path: Path, subname: str) -> Path:
        todaypath = todaytopath()
        return uploads_path.joinpath(subname, todaypath)


def _make_uploaded_path(path: Path) -> Path:
    if not path.exists():
        path.mkdir(parents=True)
    return path


def _make_secure_filepath(path: Path) -> Path:
    secure_name = uuid4().hex
    return path.joinpath(secure_name)


def get_uploaded_path(subname: str) -> Path:
    uploads_path = UploadPath.get_uploads_subdir(subname)
    path = _make_uploaded_path(uploads_path)
    return _make_secure_filepath(path)
