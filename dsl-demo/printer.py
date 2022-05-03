import re
import jinja2
import logging
import os
import platform
from parsed import data

if platform.system() == 'Windows':
    path_to_gtk_bin = r"C:\Program Files\GTK3-Runtime Win64\bin"
    os.add_dll_directory(path_to_gtk_bin)

from weasyprint import HTML, CSS

def render_jinja_html(file_name, **context):
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader('./')
    ).get_template(file_name).render(context)


# Jinja render html
html_string = render_jinja_html('template-jinja.html', data=data)

# Remove/comment/refactor on production
with open('output.html', 'w') as f:
    f.write(html_string)

# Remove/comment/refactor on production
logger = logging.getLogger('weasyprint')
logger.addHandler(logging.FileHandler('weasyprint.log'))

# WEASY PRINT RESULT
html = HTML(string=html_string, base_url='./')
html.write_pdf(target='./output.pdf', stylesheets=[CSS('style.css')])