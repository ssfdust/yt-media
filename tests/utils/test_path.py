#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path

from freezegun import freeze_time
import pytest
import os

from smorest_sfs.utils.paths import (
    ProjectPath,
    UploadPath,
    make_uploaded_path,
    get_relative_pathstr,
    WHITE_LIST,
)


class TestProjectPath:
    @pytest.mark.parametrize("_dir", ["tests", "smorest_sfs"])
    def test_project_path(self, _dir):
        project_path = ProjectPath.get_project_path()
        dir_path = Path(project_path, _dir)
        assert dir_path.exists()


@freeze_time("1994-09-11 08:20:00")
class TestUploadPath:
    @pytest.mark.parametrize(
        "storetype, withdate, args",
        [("a", True, ["1994", "09", "11"]), ("b", False, [])],
    )
    def test_uploads_subdir(self, storetype, withdate, args):
        project_path = ProjectPath.get_project_path()
        dir_path = Path(project_path, "uploads", storetype, *args)
        assert UploadPath.get_uploads_subdir(storetype, withdate) == dir_path


import pytest


@freeze_time("1994-09-11 08:20:00")
@pytest.mark.usefixtures("patch_uuid")
@pytest.mark.usefixtures("clean_dirs")
@pytest.mark.parametrize("key", ["foo", "bar", "new"])
def test_make_uploaded_path(key):
    path = make_uploaded_path(key)
    pathstr = get_relative_pathstr(path)
    abs_path = ProjectPath.get_subpath_from_project(pathstr)

    assert pathstr == f"uploads/{key}/1994/09/11/123456789" and path == abs_path


def test_white_lst():
    for path in WHITE_LIST:
        assert os.path.exists(ProjectPath.get_subpath_from_project(path))
