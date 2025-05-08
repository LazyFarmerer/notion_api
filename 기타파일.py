import requests
import base64, json

key = "secret_cKarHMRfHr3rGPxNunOMkOub4kgGWIbCrN3JrGOcEky"
page_id = "c5741c68697f4d998fce8eec3f80cb84"
block_id = "02084fd03fb64336aa065dda6d99350b"

def get_base64_image():
    url = f"https://api.notion.com/v1/blocks/{block_id}"

    header = {
        # "Accept": "application/json",
        "Notion-Version": "2022-06-28",
        # "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"
    }

    response = requests.get(url, headers=header)
    data = response.json()
    print(response.text)
    return {
        "last_edited_time": data["last_edited_time"],
        "image_url": data["paragraph"]["rich_text"][0]["plain_text"]
    }


def set_base64_image():
    url = f"https://api.notion.com/v1/blocks/{block_id}"

    header = {
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

    with open('book.jpg', 'rb') as img:
        base64_string = base64.b64encode(img.read())

    data = {
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": str(base64_string)
                    }
                }
            ]
        }
    }

    response = requests.patch(url, headers=header, data=json.dumps(data))
    print(response.text)
    return response.json()

set_base64_image()