from junitxml2json import convert
import pytest
import xml.etree.ElementTree as ET


def test_copy_attrib_to_dict():
    test_xml = ET.fromstring(
        '<testcase name="Test Copy" assertions="12" time="12.8" />'
    )
    test_dict = convert.copy_attrib_to_dict(test_xml)
    assert test_dict['name'] == "Test Copy"
    assert test_dict['assertions'] == 12
    assert test_dict['time'] == 12.8


@pytest.mark.parametrize("input, output, out_type",
                         [
                             ["ABC", "ABC", str],
                             ["123", 123, int],
                             ["12.3", 12.3, float],
                             ["", "", str],
                             ["12A", "12A", str],
                         ])
def test_to_num_if_num(input, output, out_type):
    out = convert.to_num_if_num(input)
    assert out == output
    assert isinstance(out, out_type)
