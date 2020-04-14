"""测试验证码"""
import pytest
from werkzeug.exceptions import NotFound

from smorest_sfs.extensions.storage.captcha import CaptchaStore


class TestCapture:
    @pytest.mark.parametrize("key", [("test1"), ("test2"), ("test1")])
    def test_save_restore_capture(self, key: str) -> None:
        store = CaptchaStore(key)
        value = store.generate_captcha()
        store = CaptchaStore(key)
        assert store.verify(value) is True

    def test_empty(self) -> None:
        store = CaptchaStore("unkown")
        with pytest.raises(NotFound):
            store.verify("unkown")
