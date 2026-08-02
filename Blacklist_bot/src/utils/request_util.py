from curl_cffi import requests


def get_html_document(url):
    request = requests.get(url, impersonate="chrome")

    if request.status_code == 200:
        return request.text

    return ("Information provider has problems. Details:\n" +
            "status code: " + str(request.status_code) + "\n" +
            "response page: " + request.text)
