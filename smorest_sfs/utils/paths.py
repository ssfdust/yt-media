#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
from pathlib import Path
from typing import Any, Union

import smorest_sfs

from .datetime import utctoday

UPLOADS = "uploads"
WHITE_LIST = [
    Path("uploads", "avators", "default", "AdminAvator.jpg"),
    Path("uploads", "avators", "default", "DefaultAvator.jpg"),
]


def datetopath(datestr: str) -> Path:
    return Path(*datestr.split("-"))


def todaytopath() -> Path:
    today = utctoday()
    return datetopath(str(today))


class ProjectPath:
    @classmethod
    def __get_sfs_path(cls) -> Any:
        return getattr(smorest_sfs, "__path__")[0]

    @classmethod
    def get_project_path(cls) -> Path:
        sfs_path = Path(cls.__get_sfs_path())
        return sfs_path.parent

    @classmethod
    def get_subpath_from_project(cls, path: Union[str, Path]) -> Path:
        project_path = cls.get_project_path()
        return Path(project_path, path)


class UploadPath(ProjectPath):
    @classmethod
    def get_uploads_path(cls) -> Path:
        project_path = cls.get_project_path()
        return cls._get_uploads_path(project_path)

    @classmethod
    def _get_uploads_path(cls, project_path: Path) -> Path:
        return project_path.joinpath(UPLOADS)

    @classmethod
    def get_uploads_subdir(cls, subname: str, withdate: bool = True) -> Path:
        uploads_path = cls.get_uploads_path()
        return cls._get_uploads_subdir(uploads_path, subname, withdate)

    @classmethod
    def _get_uploads_subdir(
        cls, uploads_path: Path, subname: str, withdate: bool = True
    ) -> Path:
        if withdate:
            todaypath = todaytopath()
            return uploads_path.joinpath(subname, todaypath)
        return uploads_path.joinpath(subname)

    @classmethod
    def if_in_whitelst(cls, path: Union[str, Path]) -> bool:
        whitelst = [cls.get_subpath_from_project(p) for p in WHITE_LIST]
        return path in whitelst


def _make_uploaded_path(path: Path) -> Path:
    if not path.exists():
        path.mkdir(parents=True)
    return path


def _make_secure_filepath(path: Path) -> Path:
    secure_name = uuid.uuid4().hex
    return path.joinpath(secure_name)


def make_uploaded_path(subname: str) -> Path:
    uploads_path = UploadPath.get_uploads_subdir(subname)
    path = _make_uploaded_path(uploads_path)
    return _make_secure_filepath(path)


def get_relative_pathstr(path: Path) -> str:
    project_path = ProjectPath.get_project_path()
    return str(path.relative_to(project_path))
