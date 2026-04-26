import requests

def test_realtime():
    print("Testing realtime ASL endpoint...")
    try:
        response = requests.post(
            "http://localhost:8000/api/realtime-asl",
            json={"user_input": "I want to learn advanced calculus"}
        )
        print("Status code:", response.status_code)
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print("Error:", response.text)
    except Exception as e:
        print("Request failed:", e)

if __name__ == "__main__":
    test_realtime()
