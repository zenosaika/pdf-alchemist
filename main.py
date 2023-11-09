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

@app.get('/internlog')
def get_internlog(id: str = '', date: str = ''):

    if id == '':
        return {'error': 'id is not specified'}
    if date == '':
        return {'error': 'date is not specified'}
    
    template_name = 'internlog'
    contexts = {
        'id': id, 
        'date': date
    }

    err, pdf = html2pdf(template_name, contexts)

    if err:
        return err
    
    headers = {"Content-Disposition": f"inline; filename={id}.pdf"}
    response = Response(pdf, media_type="application/pdf", headers=headers)

    return response

###########################################################
