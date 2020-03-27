#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path

from freezegun import freeze_time
import pytest

from smorest_sfs.utils.paths import ProjectPath, UploadPath


class TestProjectPath:
    @pytest.mark.parametrize("_dir", ["tests", "smorest_sfs"])
    def test_project_path(self, _dir):
        project_path = ProjectPath.get_project_path()
        dir_path = Path(project_path, _dir)
        assert dir_path.exists()


@freeze_time("1994-09-11 08:20:00")
class TestUploadPath:
    @pytest.mark.parametrize("storetype", ["a", "b"])
    def test_uploads_subdir(self, storetype):
        project_path = ProjectPath.get_project_path()
        dir_path = Path(project_path, "uploads", storetype, "1994", "09", "11")
        assert UploadPath.get_uploads_subdir(storetype) == dir_path
