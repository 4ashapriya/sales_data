import pytest
from app.sales import utils


@pytest.mark.parametrize("x, expected", [
    ({"date": "2019-08-01"}, 200)])
def test(x, expected):
    assert utils.generate_report(x)['status_code'] == expected
