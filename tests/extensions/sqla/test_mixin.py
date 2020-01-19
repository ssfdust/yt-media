#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试mixin模块"""

from copy import copy

import pytest
from marshmallow import Schema, fields
from smorest_sfs.extensions.sqla import CharsTooLong, DuplicateEntry


class TestSqlaCRUD:
    def test_created_must_have_id(self, TestCRUDTable):
        item = TestCRUDTable.create(name="created_must_have_id")
        assert item.id is not None and item.name == "created_must_have_id"

    def test_save_must_have_id(self, TestCRUDTable):
        item = TestCRUDTable(name="save_must_have_id")
        item.save()
        assert item.id is not None and item.name == "save_must_have_id"

    def test_save_should_update_modified(self, TestCRUDTable):
        item = TestCRUDTable.create(name="save_should_update_modified")
        pre_modified = copy(item.modified)
        item.save()
        assert item.modified > pre_modified

    def test_update_should_success(self, TestCRUDTable):
        item = TestCRUDTable.create(name="update_never_success")
        pre_modified = copy(item.modified)
        item.update(name="update_should_success")
        assert item.name == "update_should_success" and item.modified > pre_modified

    def test_update_should_not_update_blacked_keys(self, TestCRUDTable):
        item = TestCRUDTable.create(name=1)
        item.update(
            id=10000,
            name="update_should_not_update_blacked_keys",
            deleted=True,
            created="2008-04-12",
            modified="2008-04-12",
        )
        assert item.name == "update_should_not_update_blacked_keys" and \
            item.id != 10000 and \
            item.deleted is False and \
            item.modified.strftime("%Y-%M-%d") != "2008-04-12" and \
            item.created.strftime("%Y-%M-%d") != "2008-04-12"

    def test_soft_delete_id_should_exists(self, TestCRUDTable, db):
        item = TestCRUDTable.create(name="soft_delete_id_should_exists")
        item.delete()

        assert item.deleted is True and \
            db.session.query(TestCRUDTable).get(item.id) is not None

    def test_hard_delete_id_never_exists(self, TestCRUDTable, db):
        item = TestCRUDTable.create(name="hard_delete_id_never_exists")
        item.hard_delete()

        assert item.deleted is False and \
            db.session.query(TestCRUDTable).get(item.id) is None

    def test_errors(self, TestCRUDTable):
        very_long_text = ("sdjiasdjuwhqyuh1274yh7hsduaihsduwhqeuhquiehuhdnuq"
                          "sajdasoijdsahjduhasduhsaduhasudhausidhuashduhaish"
                          "sadasdasdasdasdasdasd")
        with pytest.raises(DuplicateEntry):
            TestCRUDTable.create(name="duplicate_entry")
            TestCRUDTable.create(name="duplicate_entry")
        with pytest.raises(CharsTooLong):
            TestCRUDTable.create(name=very_long_text)


class TestComplexUpdate(FixturesInjectBase):
    fixture_names = ("TestChildTable", "TestParentTable",
                     "TestChildSchema", "TestParentSchema")

    def test_update_by_ma(self, db):
        class TestChildSchema(Schema):
            id = fields.Int()
            pid = fields.Int()
            name = fields.Str()

        class TestParentSchema(Schema):
            name = fields.Str()
            children = fields.List(fields.Nested(ChildSchema))

        child1 = TestChild(name="1")
        child2 = TestChild(name="2")
        parent = TestParent.create(name="1", children=[child1, child2])
        modtime = copy.copy(parent.modified)
        child3 = TestChild(name="3")
        tmp_parent = TestParent(name="add1", children=[child1, child3])
        parent.update_by_ma(ParentSchema, tmp_parent, commit=False)
        assert tmp_parent.id is None
        assert parent.children == [child1, child3]
        assert parent.name == "add1"
        new_parnet = TestParent().create()
        assert new_parnet.id == parent.id + 1
        tmp_parent = TestParent(name="add2", children=[child2, child3])
        parent.update_by_ma(ParentSchema(), tmp_parent)
        parent = (
            db.session.query(TestParent)
            .filter(TestParent.id == parent.id)
            .one()
        )
        #  assert parent.children == [child2, child3
        #                            ] or parent.children == [child3, child2]
        parent.children.sort(key=lambda x: x.id)
        for sample, child in zip([child2, child3], parent.children):
            assert sample.id == child.id
            assert sample.name == child.name
            assert sample.pid == child.pid
        assert parent.name == "add2"
        new_parnet = TestParent().create()
        assert new_parnet.id == parent.id + 2
        assert parent.modified > modtime
