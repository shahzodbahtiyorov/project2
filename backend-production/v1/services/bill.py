import json
import ujson
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from v1.models import DocHistories
from v1.utils.render_to_pdf import render_pdf_view


@csrf_exempt
def generate_pdf(request):
    print("Request method:", request.method)
    print("Request headers:", request.headers)
    print("Request body:", request.body)
    body = ujson.loads(request.body)
    monitoring = DocHistories.objects.filter(tr_id=body['tr_id']).first()

    if not monitoring:
        return HttpResponse(json.dumps({"message": "Data not found"}), content_type="application/json", status=404)

    data = {
        'ext_id': monitoring.ext_id,
        'sender_company': monitoring.sender_company,
        'sender_company_account': monitoring.sender_company_account,
        'sender_company_mfo': monitoring.sender_company_mfo,
        'sender_company_inn': monitoring.sender_company_inn,
        'receiver_name': monitoring.receiver_name,
        'receiver_company_account': monitoring.receiver_company_account,
        'receiver_mfo': monitoring.receiver_mfo,
        'receiver_inn': monitoring.receiver_inn,
        'transaction_date': monitoring.transaction_date,
        'contract_number': monitoring.contract_number,
        'details': monitoring.details,
        'status': monitoring.status,
        'credit_amount': monitoring.credit_amount,
        'debit_amount': monitoring.debit_amount,
        'is_credit': 1 if monitoring.receiver_company_account == body['account'] else 2,
    }
    print(data)
    pdf = render_pdf_view('bill.html', data)
    if pdf is None:
        return HttpResponse(json.dumps({"message": "PDF generation failed"}), content_type="application/json",
                            status=500)

    return HttpResponse(pdf, content_type='application/pdf')
