"""测试sqla"""

import pytest
from werkzeug.exceptions import NotFound
from tests._utils.injection import FixturesInjectBase


class ItemsFixtureBase(FixturesInjectBase):
    @pytest.fixture
    def crud_items(self):
        return [
            self.TestCRUDTable.create(name=name)
            for name in ["aaabbb", "bbbbcccc", "bbcccc", "bbc"]
        ]


class TestBaseQuery(ItemsFixtureBase):
    fixture_names = ("TestCRUDTable",)

    @pytest.mark.usefixtures("TestTableTeardown")
    def test_soft_delete(self, crud_items):
        pre_cnt = self.TestCRUDTable.query.count()
        deleted_one = crud_items[0]
        deleted_one.delete()

        direct_get_by_id = self.TestCRUDTable.query.filter_by(id=deleted_one.id).first()
        with_deleted_get_by_id = self.TestCRUDTable.query.with_deleted().get(
            deleted_one.id
        )
        cur_cnt = self.TestCRUDTable.query.count()

        assert (
            direct_get_by_id is None
            and with_deleted_get_by_id is deleted_one
            and cur_cnt == pre_cnt - 1
        )

    @pytest.mark.usefixtures("TestTableTeardown", "crud_items")
    def test_filter_like_by(self):
        cnt = self.TestCRUDTable.query.filter_like_by(name="bc").count()
        assert cnt == 3

    def test_surrogatepk_keys(self):
        for key in ["id", "deleted", "modified", "created"]:
            assert hasattr(self.TestCRUDTable, key)

    @pytest.mark.usefixtures("TestTableTeardown")
    def test_surrogatepk_defaults(self):
        item = self.TestCRUDTable.create(name="test_defaults")
        assert (
            item.id is not None
            and item.deleted is False
            and item.created.strftime("%Y-%m-%d %H:%M:%S")
            and item.modified.strftime("%Y-%m-%d %H:%M:%S")
        )


class TestBaseRUDByID(ItemsFixtureBase):
    fixture_names = ("TestCRUDTable", "TestParentSchema", "TestParentTable")

    @pytest.mark.usefixtures("TestTableTeardown")
    def test_base_read_by_id(self, crud_items):
        item = crud_items[0]
        assert self.TestCRUDTable.get_by_id(item.id) == item

    @pytest.mark.usefixtures("TestTableTeardown")
    def test_base_delete_by_id(self, crud_items):
        item = crud_items[0]
        self.TestCRUDTable.delete_by_id(item.id)
        with pytest.raises(NotFound):
            self.TestCRUDTable.get_by_id(item.id)

    @pytest.mark.usefixtures("TestTableTeardown")
    def test_base_delete_by_idlst(self, crud_items):
        items = crud_items[0:-1]
        idlst = [item.id for item in items]
        self.TestCRUDTable.delete_by_ids(idlst)
        for item_id in idlst:
            with pytest.raises(NotFound):
                self.TestCRUDTable.get_by_id(item_id)

    def test_base_update_by_id(self, db):
        item = self.TestParentTable.create(name="base_update_by_id")
        temp_item = self.TestParentTable(name="test_update_by_id")
        self.TestParentTable.update_by_id(item.id, self.TestParentSchema, temp_item)
        assert temp_item not in db.session and item.name == "test_update_by_id"
