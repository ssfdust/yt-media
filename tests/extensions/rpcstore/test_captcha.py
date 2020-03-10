"""测试验证码"""
import pytest
from smorest_sfs.extensions.rpcstore.captcha import CaptchaStore


class TestCapture:
    @pytest.mark.parametrize(
        "key", [("test1"), ("test2"), ("test3"), ("test4"), ("test6"),]
    )
    def test_save_restore_capture(self, key: str):
        store = CaptchaStore(key)
        store.generate_captcha()
        value = store.value[:]
        store = CaptchaStore(key)
        store.get_captcha()

        assert store.value == value

    def test_empty(self):
        store = CaptchaStore("unkown")
        assert store.code_lst == []
