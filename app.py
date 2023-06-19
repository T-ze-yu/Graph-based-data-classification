from fastapi import FastAPI, Request, Body
from typing import Optional
from pydantic import BaseModel
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from celery.result import AsyncResult
import json
# from loguru import logger
import time
import uvicorn
from Bert_cla import Pre
from graph import jsto_graph
from typing import Dict, Any

app = FastAPI()
pre = Pre()
pre1 = jsto_graph()
class Item(BaseModel):
    task_model: int
    task_id: str
    datas: Dict[str,Any]
    task_call: Optional[int] = 1

# 使用字典存储任务状态
task_status = {}

# 这里写一个def



@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"参数不对{request.method} {request.url}")
    return JSONResponse({"code": "400", "message": exc.errors()})


@app.post('/knowledge/v1/api/aiport')
def process_file(
    Item:Item=Body(..., embed=True)
):
    task_id = Item.task_id
    if Item.task_call == 2:
        if Item.task_id in task_status:
            status = task_status[Item.task_id]
            return {"task_id": Item.task_id, "status":status, "datas":{}}
        else:
            return {"task_id": Item.task_id, "status":"-1", "datas":{}}
    # print(Item)
    task_status[task_id] = 1  # 任务创建成功
    try:
        # datas = json.loads(Item.datas)
        datas = Item.datas
        task_id = Item.task_id
        task_status[task_id] = 3
    except json.JSONDecodeError:
        del task_status[task_id]
        return {"data":{},"error":1001,"message":"字符串格式错误"}
    if Item.task_model == 1:
        try:
            task_status[task_id] = 3 # 此处状态为 3 表示任务正在处理
            res = pre(datas["content"])
            # res = "第一次任务完成"
        except:
            task_status[task_id] = 4  # 数据处理失败
            del task_status[task_id]
            return {"task_model":Item.task_model,"task_id":task_id,"datas":{},"error_code":1005}



    elif Item.task_model == 2:
        try:
            task_status[task_id] = 3 # 此处状态为 3 表示任务正在处理
            res = pre1(datas["content"][0],'aa')
            print(res)
            if res == 0 :
                res = {"content":"successful building!"}
        except:
            task_status[task_id] = 4
            del task_status[task_id]
            return {"task_model":Item.task_model,"task_id":task_id,"datas":{},"error_code":1005}

    elif Item.task_model == 3:
        try:
            task_status[task_id] = 3 # 此处状态为 3 表示任务正在处理
            res = pre1(datas["content"][0])
            if res == 0 :
                res = {"content":"successful building!"}
        except:
            task_status[task_id] = 4
            del task_status[task_id]
            return {"task_model":Item.task_model,"task_id":task_id,"datas":{},"error_code":1005}

    else:
        del task_status[task_id]
        return {"Item":Item.task_model,"task_id":Item.task_id,"datas":{},"error_code":1005}


    task_status[task_id] = 5 # 此处状态为任务处理完成

    del task_status[task_id]
    

    return {"task_model":Item.task_model,"task_id":Item.task_id,"datas":res}

if __name__ == "__main__":
    uvicorn.run(app, host="172.24.4.101", port=9999)

# def request1():
#     res = requests.post("http://0.0.0.0:9999/process", json={"Item":{"task_model":1,"task_id":"1011","datas":"{content:[['余小彤','蒋小玲']]}","task_call":2}})
#     print(res.json())  # {'foo': 1, 'age': 12, 'name': 'xiao123'}
# import time


# if __name__ == "__main__":
#   request1()
# 将# 取消注释，更换接口地址，即可执行


