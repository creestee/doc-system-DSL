import re

def get_sections(content):
    pattern_section = re.compile(r'''
    ^\s*\t*(.+\(*\))
    ''', flags=(re.VERBOSE | re.MULTILINE))
    result = re.findall(pattern_section, content)
    return result


def get_key(section):
    return section.split("(")[0]


def get_values(section):
    values = section[section.find("(")+1 :section.find(")")]
    return values.split(",")


def remove_quotes(text):
    text = text.replace("'", "")
    text = text.replace('"', "")
    return text


def parse_single(section):
    key = get_key(section)
    value = get_values(section)[0]
    return f"'{key}': '{value}',"


def parse_document(section):
    key = get_key(section)
    values = get_values(section)
    type = remove_quotes(values[0])
    format = remove_quotes(values[1])
    return f"'{key}': {str(dict(type=type, format=format))},"


def get_images(content):
    image_pattern = re.compile(r'''
    (image\(.*\))
    ''', flags=(re.VERBOSE | re.MULTILINE))
    result = re.findall(image_pattern, content)
    return result


def parse_image(image_str):
    values = get_values(image_str)
    name = remove_quotes(values[0])
    src = remove_quotes(values[1])
    return dict(name=name, src=src)


def get_tables(content):
    table_pattern = re.compile(r'''
    (table\(\w+\):
    \n\s*
    \{\n
    (?:[^}]+\n)*
    \s*
    \}
    )
    ''', flags=(re.VERBOSE | re.MULTILINE))

    result = re.findall(table_pattern, content)
    return result


def parse_table(table_str):
    ts = table_str.split("\n")
    name = get_values(ts[0])[0]
    rows = []
    for k in range(2, len(ts)-1):
        values = get_values(ts[k])
        rows.append(values)
    tdict = {"name": name}
    tdict["rows"] = rows
    return tdict


def get_lists(content):
    list_pattern = re.compile(r'''
    (list\(.+\):
    \n\s*\{\n
    (?:[^}]+\n)*
    \s*\}
    )
    ''', flags=(re.VERBOSE | re.MULTILINE))
    result = re.findall(list_pattern, content)
    return result


def parse_list(list_str):
    ls = list_str.split("\n")
    name = get_values(ls[0])[0]
    items = []
    for k in range(2, len(ls)-1):
        values = get_values(ls[k])[0]
        items.append(values)
    tdict = {"name": name}
    tdict['items'] = items
    return tdict


def get_text_blocks(content):
    text_block_pattern = re.compile(r'''
    (
    (?:^[^():{}]+\n)
    )
    ''', flags=(re.VERBOSE | re.MULTILINE))
    result = re.findall(text_block_pattern, content)
    return result

def parse_text_block(text_block_str):
    return text_block_str


def get_subchapters(content):
    subchapter_pattern = re.compile(r'''
    (
    subchapter\(.+\):
    (?:\n|\s)*
    {
    (?:\s|\n)*
    (?:.*\n*)*?
    \s*}\n
    )
    ''', flags=(re.VERBOSE | re.MULTILINE))
    result = re.findall(subchapter_pattern, content)
    return result


def parse_subchapter(subchapter):
    fs = subchapter.split("\n")[0]
    title = get_values(fs)[0]
    content = subchapter.split("):")[1]
    return dict(title=title, content=content)
    

def get_chapters(content):
    chapter_pattern = re.compile(r'''
    (
    chapter\(.+\):
    (?:\n|\s)*
    {
    (?:\s|\n)*
    (?:.*\n*)*?
    \s*}\n
    )
    ''', flags=(re.VERBOSE | re.MULTILINE))
    result = re.findall(chapter_pattern, content)
    return result


def parse_chapter(chapter):
    fs = chapter.split("\n")[0]
    title = get_values(fs)[0]
    content = chapter.split("):")[1]
    return dict(title=title, content=content)