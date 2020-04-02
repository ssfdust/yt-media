#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List, Tuple, Type, Union, Set

from flask import url_for
from marshmallow import Schema

import pytest
from smorest_sfs.extensions.sqla import Model

from .uniqueue import UniqueQueue


def log_to_queue(record):
    queue = UniqueQueue()
    queue.put(record.record["message"])
    return record


def inject_logger(logger):
    logger.add(log_to_queue, serialize=False)


def uninject_logger(logger):
    logger.remove()


class FixturesInjectBase:

    items: str
    listview: str
    listkeys: Set[str] = {"id", "name"}
    view: str
    item_view: str
    login_roles: List[str]
    model: Type[Model]
    schema: Type[Schema]
    delete_param_key: str
    fixture_names: Union[Tuple[str], Tuple] = ()

    @pytest.fixture(autouse=True)
    def auto_injector_fixture(self, request):
        names = self.fixture_names
        for name in names:
            setattr(self, name, request.getfixturevalue(name))


class GeneralModify(FixturesInjectBase):
    def _add_request(self, data):
        with self.flask_app_client.login(self.regular_user, self.login_roles) as client:
            with self.flask_app.test_request_context():
                url = url_for(self.view)
                resp = client.post(url, json=data)
                item = self.model.get_by_id(resp.json["data"]["id"])
                schema = self.schema()
                dumped_data = self.__get_schema_dumped(schema, item)
                self.model.query.filter_by(id=resp.json["data"]["id"]).delete()
                self.db.session.commit()
                assert (
                    resp.status_code == 200
                    and isinstance(resp.json["data"], dict)
                )
                return dumped_data

    def _get_deleting_items(self):
        items = getattr(self, self.items)
        return items[:1]

    def _get_modified_item(self):
        items = getattr(self, self.items)
        return items[-1]

    @staticmethod
    def __get_schema_dumped(schema, item):
        return schema.dump(item)

    def _get_dumped_modified_item(self):
        item = self._get_modified_item()
        schema = self.schema()
        return self.__get_schema_dumped(schema, item)

    def _delete_request(self):
        with self.flask_app_client.login(self.regular_user, self.login_roles) as client:
            with self.flask_app.test_request_context():
                url = url_for(self.view)
                items = self._get_deleting_items()
                ids = [i.id for i in items]
                resp = client.delete(url, json={"lst": ids})
                assert resp.status_code == 200 and all([i.deleted for i in items])
                return resp, items

    def __item_modify_request(self, method, **kwargs):
        with self.flask_app_client.login(self.regular_user, self.login_roles) as client:
            with self.flask_app.test_request_context():
                item = self._get_modified_item()
                url = url_for(self.item_view, **{self.delete_param_key: item.id})
                resp = client.open(url, method=method, **kwargs)
                return resp

    def _item_modify_request(self, json):
        resp = self.__item_modify_request("PUT", json=json)
        schema = self.schema()
        item = self._get_modified_item()
        dumped_data = self.__get_schema_dumped(schema, item)
        assert resp.status_code == 200
        return dumped_data

    def _item_delete_request(self):
        resp = self.__item_modify_request("DELETE")
        item = self._get_modified_item()
        assert resp.status_code == 200 and item.deleted
        return resp, item


class GeneralGet(FixturesInjectBase):
    def _get_view(self, endpoint: str, **kwargs):
        with self.flask_app_client.login(self.regular_user, self.login_roles) as client:
            with self.flask_app.test_request_context():
                url = url_for(endpoint, **kwargs)
                return client.get(url)

    def _get_options(self):
        resp = self._get_view(self.listview)
        assert (
            resp.status_code == 200
            and isinstance(resp.json["data"], list)
            and resp.json["data"][0].keys() == self.listkeys
        )

    def _get_list(self, **kwargs):
        resp = self._get_view(self.view, **kwargs)
        assert resp.status_code == 200 and isinstance(resp.json["data"], list)
        return resp.json["data"]

    def _get_item(self, **kwargs):
        resp = self._get_view(self.item_view, **kwargs)
        assert resp.status_code == 200 and isinstance(resp.json["data"], dict)
        return resp.json["data"]
