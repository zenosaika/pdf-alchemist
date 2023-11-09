import os
import base64

from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

from html2pdf import html2pdf

###########################################################

app = FastAPI()

###########################################################

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

###########################################################

@app.get('/')
def main():
    return "what is love? baby don't hurt me!"

###########################################################

@app.get('/dir')
def get_dir(id: str = '', date: str = ''):

    if id == '':
        return {'error': 'id is not specified'}
    if date == '':
        return {'error': 'date is not specified'}
    
    # read and convert TSE logo image to base64
    root = os.path.dirname(os.path.abspath(__file__))
    tse_logo_path = os.path.join(root, 'static', 'tse_logo.png')
    with open(tse_logo_path, 'rb') as img:
        tse_logo_base64 = base64.b64encode(img.read()).decode()
    
    template_name = 'dir'

    contexts = {
        'id': id, 
        'date': date,
        'tse_logo_base64': tse_logo_base64,
        'name': 'Hatsune Miku',
        'company': 'Neki Company',
        'records': [{} for _ in range(7)],
    }

    # https://wkhtmltopdf.org/usage/wkhtmltopdf.txt
    options = {
        'page-size': 'A4',
        'orientation':'Landscape',
        'header-html': 'templates/dir_header.html',
        'header-spacing': '10',
        'margin-top': '20',
        'margin-bottom': '20',
        'encoding': 'UTF-8',
    }

    err, pdf = html2pdf(template_name, contexts, options)

    if err:
        return err
    
    headers = {"Content-Disposition": f"inline; filename={id}.pdf"}
    response = Response(pdf, media_type="application/pdf", headers=headers)

    return response

###########################################################
