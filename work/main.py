import requests
from pprint import pprint

session = requests.Session()

BASE_URL = "http://192.168.2.16:8083/api/"
userId = None
def login(username, password):
    post_data = {
        "username": username,
        "password": password
    }
    res_data = session.post(url=BASE_URL+"tb-user/login", json=post_data).json()
    session.headers.update({"Authorization": res_data["data"]["token"]})
    global userId
    userId = res_data["data"]["userId"]

def work_hour_list(pageSize, pageNum, projectId):
    global userId
    post_data = {
        "pageSize": pageSize, 
        "pageNum": pageNum, 
        "projectId": projectId, 
        "userId": userId
    }
    res_data = session.post(url=BASE_URL+"workHour/list", json=post_data).json()
    for data in res_data["data"]["resultList"]:
        pprint(data)

def work_hour_add(entryTime, workContent, workHour):
    global userId
    # 2023-08-14
    post_data = {
        "entryTime": entryTime+" 00:00:00",
        "milePostId": 13,
        "name": "工程活动",
        "projectId": 88,
        "userId": userId,
        "workContent": workContent,
        "workHour": workHour
    }
    res_data = session.post(url=BASE_URL+"workHour/add", json=post_data).json()

if __name__ == "__main__":
    login("konglei","kl1999714")
    work_hour_list(1, 1,"88")
    # work_hour_add("2023-08-21", "SIT测试", 8.5)
    pass