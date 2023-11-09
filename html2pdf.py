import os
from datetime import datetime, timedelta

import pdfkit
from jinja2 import Environment, FileSystemLoader

def html2pdf(template_name, contexts):
    root = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(root, 'templates')
    env = Environment(loader=FileSystemLoader(templates_dir))
    
    try:
        template = env.get_template(f'{template_name}.html')
    except:
        return {'error': 'template not found'}, None
    
    rendered_template = template.render(contexts)

    options = {
        'page-size':'A4',
        'encoding': 'UTF-8',
    }

    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

    css_path = os.path.join(root, 'templates', f'{template_name}.css')
    if os.path.exists(css_path):
        pdf = pdfkit.from_string(rendered_template, False, options=options, configuration=config, css=css_path)
    else :
        pdf = pdfkit.from_string(rendered_template, False, options=options, configuration=config)
    
    return None, pdf
