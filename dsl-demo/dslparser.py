import sys
from pprint import pprint, pformat
from parser_lib import *


def read_file(filename, encoding="utf-8"):
    with open(filename, "r", encoding=encoding) as f:
        content = f.read()
    return content


def write_to_file(filename, content, encoding="utf-8"):
    with open(filename, "w", encoding=encoding) as f:
        f.write(content)

 
def parse_file(input_file=".\input.txt", parsed_file="parsed.py"):
    content = read_file(input_file)

    content = content.replace("{^", "{")
    content = content.replace("^}", "}")
    content = remove_quotes(content)

    sections = get_sections(content)

    pr_content = content

    for section in sections:
        key = get_key(section)
        if key in ("title", "subject", "author", "table_of_contents"):
            pr_content = pr_content.replace(section, parse_single(section))

        elif key == "document":
            pr_content = pr_content.replace(section, parse_document(section))

    images = get_images(pr_content)
    for i, image_str in enumerate(images):
        image_dict = parse_image(image_str)
        image_replace = f"'image_{i}': {str(image_dict)}," 
        pr_content = pr_content.replace(image_str, image_replace)

    tables = get_tables(pr_content)
    for i, table_str in enumerate(tables):
        table_dict = parse_table(table_str)
        table_replace = f"'table_{i}': {str(table_dict)}," 
        pr_content = pr_content.replace(table_str, table_replace)

    lists = get_lists(pr_content)
    for i, list_str in enumerate(lists):
        list_dict = parse_list(list_str)
        list_replace = f"'list_{i}': {str(list_dict)}," 
        pr_content = pr_content.replace(list_str, list_replace)

    text_blocks = get_text_blocks(pr_content)
    for i, text_block_str in enumerate(text_blocks):
        text_block_parsed = parse_text_block(text_block_str)
        text_block_str = text_block_str.replace("\"", "")
        text_block_replace = f"'text_{i}': '''{text_block_str}''',"
        pr_content = pr_content.replace(text_block_str, text_block_replace)

    subchapters = get_subchapters(pr_content)
    for i, subchapter_str in enumerate(subchapters):
        subchapter_dict = parse_subchapter(subchapter_str)
        subchapter_replace = f"'subchapter_{i}': {subchapter_dict},"
        subchapter_replace = subchapter_replace.replace("\\n", "")
        subchapter_replace = subchapter_replace.replace("\'", "'")
        subchapter_replace = subchapter_replace.replace("\"", "")
        pr_content = pr_content.replace(subchapter_str, subchapter_replace)


    chapter = get_chapters(pr_content)
    for i, chapter_str in enumerate(chapter):
        chapter_dict = parse_chapter(chapter_str)
        chapter_replace = f"'chapter_{i}': {chapter_dict},".replace(r"\\\\", r"\\")
        chapter_replace = chapter_replace.replace("\"", "")
        chapter_replace = chapter_replace.replace("\\n", "")
        pr_content = pr_content.replace(chapter_str, chapter_replace)

    write_to_file(parsed_file, f"data = {pr_content}")


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 3:
        input_file = args[1]
        parsed_file = args[2]
        parse_file(input_file, parsed_file)
    else:
        parse_file()