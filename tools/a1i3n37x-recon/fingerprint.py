import requests

def fingerprint_site(url):
    try:
        response = requests.get(url, timeout=10)
        headers = response.headers
        server = headers.get("Server", "Unknown")
        powered_by = headers.get("X-Powered-By", "Unknown")
        tech = {
            "Server": server,
            "X-Powered-By": powered_by,
            "Content-Type": headers.get("Content-Type", "Unknown"),
            "Content-Encoding": headers.get("Content-Encoding", "Unknown"),
            "Content-Length": headers.get("Content-Length", "Unknown")
        }

        title = ""
        if "<title>" in response.text.lower():
            start = response.text.lower().find("<title>") + 7
            end = response.text.lower().find("</title>")
            title = response.text[start:end].strip()

        return {
            "url": url,
            "status_code": response.status_code,
            "headers": tech,
            "title": title
        }
    except Exception as e:
        return {"error": str(e), "url": url}
