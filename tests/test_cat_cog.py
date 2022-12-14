from cat_cog import BaseImage


def test_prepare_text() -> None:
    test_img = BaseImage("123")
    assert test_img._prepare_text("1-2_3") == "1 2\n3"