import requests
import os
import shutil
# import time

os.makedirs("packages", exist_ok=True)
api_url = "http://34.165.200.87:8081/service/rest/v1/components?repository=pipey_proxy"
# print(api_url)
response = requests.get(api_url)
# print(response)
x = response.json()
#package_to_upload = ""
headers = {
    'accept': 'application/json',
}

params = {
    'repository': 'pipyrepo',
}


continueFlag = True
while continueFlag:
    for item in x["items"]:
        for asset in item["assets"]:
            URL = asset["downloadUrl"]
            packageName = URL.split("/")[-1]
            print("downloading " + packageName + "\n")
            response = requests.get(URL)
            if response.status_code == 200:
                print("download succeeded")
            else:
                print("failed downloading")
            open("packages/" + packageName, "wb").write(response.content)
            #package_to_upload = packageName
            files = {'pypi.asset': open("packages/" + packageName, 'rb'), }
            response = requests.post('http://34.165.200.87:8081/service/rest/v1/components', params=params, headers=headers, files=files, auth=('admin', 'admin'))
            if response.status_code == 204:
                print("upload succeeded")
            else:
                print("failed uploading")
    if x["continuationToken"] is not None:
        api_url = "http://34.165.200.87:8081/service/rest/v1/components?continuationToken=" + x["continuationToken"] + "&repository=pipey_proxy"
        response = requests.get(api_url)
        x = response.json()
    else:
        continueFlag = False
# print("sleeping for 60 seconds")
# time.sleep(120)
# print("wakey wakey")
shutil.rmtree('packages', ignore_errors=True)
