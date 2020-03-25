"""测试验证码"""
import pytest
from smorest_sfs.extensions.storage.captcha import CaptchaStore


class TestCapture:
    @pytest.mark.parametrize("key", [("test1"), ("test2"), ("test1")])
    def test_save_restore_capture(self, key: str):
        store = CaptchaStore(key)
        value = store.generate_captcha()
        store = CaptchaStore(key)
        assert store.verify(value) is True

    def test_empty(self):
        store = CaptchaStore("unkown")
        with pytest.raises(AttributeError):
            store.verify("unkown")
