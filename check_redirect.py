import requests


def check_redirect(response_history):
    if response_history:
        raise requests.HTTPError('Redirect to main')