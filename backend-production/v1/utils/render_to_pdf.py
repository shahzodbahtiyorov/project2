"""
render_to_pdf.py

This module provides functionality for rendering HTML templates to PDF documents.
It includes a function for converting a template and context dictionary into a PDF response.

Functions:
- `render_to_pdf(template_src, context_dict={})`: Renders an HTML template with a given context dictionary into a PDF
    and returns it as an HTTP response.

Dependencies:
- `io.BytesIO`: Provides in-memory byte stream operations.
- `django.http.HttpResponse`: Used to return HTTP responses.
- `django.template.loader.get_template`: Loads Django templates.
- `xhtml2pdf.pisa`: Converts HTML to PDF.

"""
import os
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from xhtml2pdf import pisa
from django.conf import settings
from xhtml2pdf.files import pisaFileObject


def link_callback(uri, rel):
    print(f"URI received: {uri}")

    # Ensure URI starts with a slash
    if not uri.startswith('/'):
        uri = '/' + uri

    sUrl = settings.STATIC_URL
    sRoot = settings.STATICFILES_DIRS[0]
    mUrl = settings.MEDIA_URL
    mRoot = settings.MEDIA_ROOT

    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        path = uri

    pisaFileObject.getNamedFile = lambda self: path
    print(path)

    if not os.path.isfile(path):
        raise Exception('media URI must start with %s or %s' % (sUrl, mUrl))

    return path



@csrf_exempt
def render_pdf_view(template_src='bill.html', context_dict={}):
    print(f"Template: {template_src}, Context: {context_dict}")
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    template = get_template(template_src)
    html = template.render(context_dict)

    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response

