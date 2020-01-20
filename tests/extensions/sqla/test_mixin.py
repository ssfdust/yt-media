#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试mixin模块"""

from copy import copy

import pytest
from smorest_sfs.extensions.sqla import CharsTooLong, DuplicateEntry
from smorest_sfs.extensions.sqla.helpers import set_default_for_instance
from tests.utils import FixturesInjectBase


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


class TestUpdateBySchema(FixturesInjectBase):
    fixture_names = ("TestParentTable", "TestParentSchema")

    def do_init_update_by_schema(self, **kwargs):
        temp_instance = self.TestParentTable(**kwargs)
        temp_instance = set_default_for_instance(temp_instance)
        self.item.update_by_ma(self.schema, temp_instance)
        return temp_instance

    def create_item_and_schema(self, schema_kwargs, **item_kwargs):
        setattr(self, "item", self.TestParentTable(**item_kwargs))
        setattr(self, "schema", self.TestParentSchema(only=schema_kwargs))

    def teardown_method(self, _):
        setattr(self, "item", None)
        setattr(self, "schema", None)

    @pytest.mark.usefixtures("TestTableTeardown")
    def test_normal_schema_should_update_successfully(self):
        self.create_item_and_schema(None,
                                    name="the_name_should_be_changed")
        self.do_init_update_by_schema(name="the_changed_name")
        assert self.item.name == "the_changed_name"

    @pytest.mark.usefixtures("TestTableTeardown")
    def test_no_keys_in_schema_should_update_nothing(self):
        self.create_item_and_schema((), name="the_name_should_not_be_changed")
        self.do_init_update_by_schema(name="the_name_should_never_changed")
        assert self.item.name == "the_name_should_not_be_changed"

    @pytest.mark.usefixtures("TestTableTeardown")
    @pytest.mark.parametrize("key", ["id", "deleted", "modified", "created"])
    def test_blacked_keys_in_schema_should_update_nothing(self, key):
        self.create_item_and_schema((key, ), name="the_blacked_key_should_not_be_changed")
        temp_instance = self.do_init_update_by_schema(name="the_key_should_never_changed")
        updated_val = getattr(temp_instance, key)
        assert self.item.name != updated_val

    @pytest.mark.usefixtures("TestTableTeardown")
    def test_temp_instance_should_not_be_saved(self):
        self.create_item_and_schema(None, name="temp_instance_should_not_be_saved")
        temp_instance = self.do_init_update_by_schema(name="the_id_is_none")
        assert temp_instance.id is None

    @pytest.mark.usefixtures("TestTableTeardown")
    def test_temp_instance_should_not_in_session(self, db):
        item = self.TestParentTable.create(name=f"keep_the_name")
        schema = self.TestParentSchema()
        temp_instance = self.TestParentTable(name="change_the_name")
        temp_instance = set_default_for_instance(temp_instance)
        item.update_by_ma(schema, temp_instance)
        assert temp_instance not in db.session

    @pytest.mark.usefixtures("TestTableTeardown")
    def test_temp_instance_should_be_flushed(self, db):
        item = self.TestParentTable.create(name=f"keep_the_name")
        schema = self.TestParentSchema()
        temp_instance = self.TestParentTable(name="change_the_name")
        temp_instance = set_default_for_instance(temp_instance)
        item.update_by_ma(schema, temp_instance)
        db.session.flush()
        assert temp_instance.id is None

    @pytest.mark.usefixtures("TestTableTeardown")
    def test_temp_instance_should_be_commited(self, db):
        item = self.TestParentTable.create(name=f"keep_the_name")
        schema = self.TestParentSchema()
        temp_instance = self.TestParentTable(name="change_the_name")
        temp_instance = set_default_for_instance(temp_instance)
        item.update_by_ma(schema, temp_instance)
        db.session.commit()
        assert temp_instance.id is None

    #  def test_update_by_ma_in_complex(self):
    #      child1 = self.TestChild()
    #      child2 = TestChild()
    #      parent = TestParent.create(name="1", children=[child1, child2])
    #      modtime = copy.copy(parent.modified)
    #      child3 = TestChild(name="3")
    #      tmp_parent = TestParent(name="add1", children=[child1, child3])
    #      parent.update_by_ma(ParentSchema, tmp_parent, commit=False)
    #      assert tmp_parent.id is None
    #      assert parent.children == [child1, child3]
    #      assert parent.name == "add1"
    #      new_parnet = TestParent().create()
    #      assert new_parnet.id == parent.id + 1
    #      tmp_parent = TestParent(name="add2", children=[child2, child3])
    #      parent.update_by_ma(ParentSchema(), tmp_parent)
    #      parent = (
    #          db.session.query(TestParent)
    #          .filter(TestParent.id == parent.id)
    #          .one()
    #      )
    #      #  assert parent.children == [child2, child3
    #      #                            ] or parent.children == [child3, child2]
    #      parent.children.sort(key=lambda x: x.id)
    #      for sample, child in zip([child2, child3], parent.children):
    #          assert sample.id == child.id
    #          assert sample.name == child.name
    #          assert sample.pid == child.pid
    #      assert parent.name == "add2"
    #      new_parnet = TestParent().create()
    #      assert new_parnet.id == parent.id + 2
    #      assert parent.modified > modtime
