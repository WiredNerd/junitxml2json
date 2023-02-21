import xml.etree.ElementTree as ET


def parse_testsuites_file(filename: str):
    root_xml = ET.parse(filename).getroot()
    assert root_xml.tag == "testsuites"
    return parse_testsuites(root_xml)


def parse_testsuites_string(xml: str):
    root_xml = ET.fromstring(xml).getroot()
    assert root_xml.tag == "testsuites"
    return parse_testsuites(root_xml)


def parse_testsuites(ts_xml: ET):
    ts_dict = copy_attrib_to_dict(ts_xml)

    ts_dict['testsuite'] = []
    for child in ts_xml:
        if child.tag == 'testsuite':
            ts_dict['testsuite'].append(parse_testsuite(child))
    return ts_dict


def parse_testsuite(ts_xml: ET):
    ts_dict = copy_attrib_to_dict(ts_xml)

    ts_dict['properties'] = {}
    ts_dict['testcase'] = []
    for child in ts_xml:
        if child.tag == 'properties':
            ts_dict['properties'] = parse_properties(child)
        elif child.tag == 'testcase':
            ts_dict['testcase'].append(parse_textcase(child))
        elif child.tag == 'system-out':
            ts_dict['system-out'] = child.text
        elif child.tag == 'system-err':
            ts_dict['system-err'] = child.text
    return ts_dict


def parse_properties(props_xml: ET):
    props_dict = {}
    for prop in props_xml:
        props_dict[prop.attrib['name']] = prop.attrib['value']
    return props_dict


def parse_textcase(tc_xml: ET):
    tc_dict = copy_attrib_to_dict(tc_xml)

    tc_dict['error'] = []
    tc_dict['failure'] = []
    tc_dict['system-out'] = []
    tc_dict['system-err'] = []
    for child in tc_xml:
        if child.tag == 'skipped':
            tc_dict['skipped'] = child.text
        elif child.tag == 'error':
            tc_dict['error'].append(copy_attrib_to_dict(child))
        elif child.tag == 'failure':
            tc_dict['failure'].append(copy_attrib_to_dict(child))
        elif child.tag == 'system-out':
            tc_dict['system-out'].append(child.text)
        elif child.tag == 'system-err':
            tc_dict['system-err'].append(child.text)
    return tc_dict


def copy_attrib_to_dict(elem: ET):
    out = {}
    for key in elem.attrib:
        out[key] = to_num_if_num(elem.attrib[key])
    return out


def to_num_if_num(val: str):
    try:
        out = val
        out = float(val)
        out = int(val)
    except ValueError:
        pass
    return out
