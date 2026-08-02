import requests


def get_html_document(url):
    request = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:153.0) Gecko/20100101 Firefox/153.0"})

    if request.status_code == 200:
        return request.text

    return ("Information provider has problems. Details:\n" +
            "status code: " + str(request.status_code) + "\n" +
            "response page: " + request.text)
