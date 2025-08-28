import requests

endpoint = "http://127.0.0.1:8000/api/v1/"
res = requests.get(endpoint , json={'product_id' : 123})

print(res.status_code)   # 200 means OK
# print(res.json())        # Convert response to JSON
