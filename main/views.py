from django.shortcuts import render

import requests


def home(request):
    return render(request, 'main/index.html')


def generate_qr(request):
    url_text = request.POST.get('url', None)
    api_text = {"text": url_text}
    api_endpoint = "http://127.0.0.1:8000/api/create/"
    req = requests.post(url=api_endpoint,data=api_text)
    res = req.json()
    status = req.status_code
    context_dict = dict()
    if status == 429:
        context_dict['message'] = res.get('detail')
    else:
        context_dict['image_data'] = res.get('image_base64')
    return render(request, 'main/index.html', context_dict)
