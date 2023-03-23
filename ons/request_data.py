import json

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


URL_BASE = "https://api.beta.ons.gov.uk/v1/datasets/"


def get_data_frame(key: str):
    request_url = URL_BASE+key
    d = _connect_to_uk_api(request_url)
    url_ts = d['links']['latest_version']['href']
    csv_link = _connect_to_uk_api(url_ts)['downloads']['csv']['href']
    return _connect_to_uk_api(csv_link, request_type='csv')


def _connect_to_uk_api(url: str, request_type: str = 'json') -> dict:
    session = requests.session()
    retry_strategy = Retry(
        total=3, backoff_factor=0.1, status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    try:
        r = session.get(url=url)
    except requests.exceptions.HTTPError as err:
        raise requests.exceptions.HTTPError(
            f"HTTP error fetching data:",
            r.status_code,
            r.reason,
            URL_BASE,
        ) from err
    if r.status_code != requests.codes.ok:
        raise Exception(r.status_code, r.reason, url)
    session.close()
    if request_type == 'json':
        return json.loads(r.text)
    elif request_type == 'csv':
        return r.text
