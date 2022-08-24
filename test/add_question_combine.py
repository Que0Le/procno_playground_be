import pyttsx3 as ptts
import json, csv

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings 


# engine = ptts.init() # object creation
# engine.save_to_file("Hello World", f"{settings.DATA_PATH}/temp/test.mp3")
# engine.runAndWait()


client = TestClient(
    app, 
    # base_url="https://localhost:8888"
)


# def test_get_question(capsys):
#     response = client.get(f"{settings.API_V1_STR}/questions/meta")
#     assert response.status_code == 200
    # with capsys.disabled():
    #     print(response.json())
    #     print("this output will not be captured and go straight to sys.stdout")

def get_all_user(capsys):
    response = client.get(f"{settings.API_V1_STR}/users")
    assert response.status_code == 200
    return response.json()


def test_create_readtext(capsys):
    first_user = get_all_user(capsys)[0]
    with capsys.disabled():
        print(first_user)
    with open("tools/fake_data/read_text_english.csv", "r") as csvfile:
        data = csv.reader(csvfile, delimiter=',', quotechar='"')
        count = 0
        for row in data:
            count = count + 1
            if count == 1:
                continue
            with capsys.disabled():
                print(row)
            payload = {"owner_uniq_id": first_user["uniq_id"], "read_text": row[1]}
            response = client.post(
                url=f"{settings.API_V1_STR}/read-texts/", 
                data=json.dumps(payload)
            )
            assert response.status_code == 200
            with capsys.disabled():
                print(payload)
                print(response.json())