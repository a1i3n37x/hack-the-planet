
import requests
from bs4 import BeautifulSoup

def find_forms(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        forms = soup.find_all("form")
        found_forms = []

        for form in forms:
            form_info = {
                "action": form.get("action", "N/A"),
                "method": form.get("method", "GET").upper(),
                "inputs": []
            }
            for input_tag in form.find_all("input"):
                form_info["inputs"].append({
                    "name": input_tag.get("name", ""),
                    "type": input_tag.get("type", "text")
                })
            found_forms.append(form_info)

        return found_forms

    except Exception as e:
        return {"error": str(e)}
