import os
import sys
import logging
import platform
import jinja2

import dslparser


if platform.system() == 'Windows':
    path_to_gtk_bin = r"C:\Program Files\GTK3-Runtime Win64\bin"
    os.add_dll_directory(path_to_gtk_bin)

from weasyprint import HTML, CSS

def render_jinja_html(file_name, **context):
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader('./')
    ).get_template(file_name).render(context)

if __name__ == "__main__":
    args = sys.argv
    input_file = args[1]
    output_file = args[2]
    dslparser.parse_file(input_file)
    from parsed import data
    # Jinja render html
    html_string = render_jinja_html('template-jinja.html', data=data)

    # Remove/comment/refactor on production
    # with open('output.html', 'w') as f:
    #     f.write(html_string)

    # Remove/comment/refactor on production
    logger = logging.getLogger('weasyprint')
    logger.addHandler(logging.FileHandler('weasyprint.log'))

    # WEASY PRINT RESULT
    html = HTML(string=html_string, base_url='./')
    html.write_pdf(target=output_file, stylesheets=[CSS('style.css')])