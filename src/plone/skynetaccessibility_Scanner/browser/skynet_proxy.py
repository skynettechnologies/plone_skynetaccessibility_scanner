"""
skynet_proxy.py — Server-side proxy view for SkynetAccessibility Scanner.

Registered as @@skynet-proxy on the Plone site root.

The browser-side JS cannot call the Skynet API directly because of CORS
restrictions. This view accepts the request from the browser, forwards it
server-side to the Skynet API, and streams the response back to the browser.

Query-string / POST parameters accepted
---------------------------------------
url         The full Skynet API URL to proxy. Required.
method      HTTP method to use (GET or POST). Default: GET.

All other form parameters are forwarded to the upstream URL when method is POST.
"""
import json

import requests
from Products.Five import BrowserView


class SkynetProxyView(BrowserView):
    """Forwards browser requests to the Skynet API server-side to bypass CORS."""

    # Only proxy calls that start with one of these prefixes.
    ALLOWED_PREFIXES = (
        "https://api.skynetaccessibility.com/",
        "https://skynetaccessibility.com/",
    )

    TIMEOUT = 30

    def __call__(self):
        response = self.request.response
        response.setHeader("Content-Type", "application/json")

        target_url = self.request.form.get("url", "").strip()
        if not target_url:
            response.setStatus(400)
            return json.dumps({"error": "Missing required parameter: url"})

        if not any(target_url.startswith(prefix) for prefix in self.ALLOWED_PREFIXES):
            response.setStatus(403)
            return json.dumps({"error": "Proxy target not allowed: {}".format(target_url)})

        method = self.request.form.get("method", "GET").upper()
        if method not in ("GET", "POST"):
            response.setStatus(400)
            return json.dumps({"error": "Unsupported method: {}".format(method)})

        forward_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        try:
            if method == "POST":
                payload = {
                    k: v
                    for k, v in self.request.form.items()
                    if k not in ("url", "method")
                }
                upstream = requests.post(
                    target_url,
                    json=payload,
                    headers=forward_headers,
                    timeout=self.TIMEOUT,
                )
            else:
                upstream = requests.get(
                    target_url,
                    headers=forward_headers,
                    timeout=self.TIMEOUT,
                )
        except requests.exceptions.Timeout:
            response.setStatus(504)
            return json.dumps({"error": "Upstream request timed out"})
        except requests.exceptions.ConnectionError as exc:
            response.setStatus(502)
            return json.dumps({"error": "Could not reach upstream: {}".format(str(exc))})
        except Exception as exc:
            response.setStatus(500)
            return json.dumps({"error": "Proxy error: {}".format(str(exc))})

        response.setStatus(upstream.status_code)

        try:
            upstream.json()
            return upstream.text
        except ValueError:
            return json.dumps({"raw": upstream.text})

