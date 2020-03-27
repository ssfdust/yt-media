"""测试API"""
from typing import Dict
from flask.views import MethodView
import pytest
from flask_smorest import Blueprint
from smorest_sfs.extensions.api.decorators import paginate
from tests._utils.injection import FixturesInjectBase


class TestApi(FixturesInjectBase):

    fixture_names = ("app", "api", "TestPagination", "TestPageSchema")

    def setup_blp(self):
        blp = Blueprint("tests", "tests")

        TestPagination = self.TestPagination
        TestPageSchema = self.TestPageSchema

        @blp.route("/")
        class Pets(MethodView):  # pylint: disable=W0612
            @blp.response(TestPageSchema)
            @paginate()
            def get(self):
                """List pets"""
                return TestPagination.query.order_by(TestPagination.id)

        self.api.register_blueprint(blp, base_prefix="/pets", url_prefix="/")

    @pytest.mark.parametrize(
        "meta",
        [
            (
                {
                    "links": {
                        "first": "/pets/?page=1&per_page=5",
                        "last": "/pets/?page=4&per_page=5",
                        "next": "/pets/?page=3&per_page=5",
                        "prev": "/pets/?page=1&per_page=5",
                    },
                    "page": 2,
                    "pages": 4,
                    "per_page": 5,
                    "total": 20,
                }
            )
        ],
    )
    def test_api(self, meta: Dict):
        # pylint: disable=W0613
        self.setup_blp()
        data = self.get_test_json("pets/?page=2&per_page=5")

        assert data["meta"] == meta

    def get_test_json(self, url: str) -> Dict:
        test_client = self.app.test_client()
        resp = test_client.get(url)
        return resp.json
