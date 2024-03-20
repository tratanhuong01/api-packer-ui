from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from openai import OpenAI
from typing import List
import firebase_admin
from firebase_admin import credentials, db
from typing import Any, Dict
from pydantic import BaseModel
# import asyncio

client = OpenAI(
    api_key="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",
)

#
class Role(BaseModel):
    role:str
    content:str
#

app = FastAPI()
cred = credentials.Certificate("./packer-ui-firebase.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://packer-ui-default-rtdb.firebaseio.com/'
})


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Component(BaseModel):
    id: Any
    name : str
    type: str
    component : List[Any]

## packer-ui
@app.post("/components")
async def add_component(component: Component): 

    try:
        # Get a reference to the 'components' array in the database
        ref = db.reference("/components")
        array = ref.get()

        # Ensure 'array' is initialized as a list if it's None
        if array is None:
            array = []

        # Append the new component to the array
        array.append(component.model_dump())

        # Update the 'components' array in the database
        ref.set(array)

        return array
    except Exception as e:
        # Handle any exceptions that may occur during database interaction
        raise HTTPException(status_code=500, detail=str(e))
## packer-ui

## packer-ui
@app.get("/components")
async def get_component(): 

    try:
        # Get a reference to the 'components' array in the database
        ref = db.reference("/components")
        array = ref.get()
        
        return array
    except Exception as e:
        # Handle any exceptions that may occur during database interaction
        raise HTTPException(status_code=500, detail=str(e))
## packer-ui

## chat-gpt

def get_chat_completion(messages, model="gpt-3.5-turbo"):
  
   # Calling the ChatCompletion API
   newMessages = []
   for item in messages:
       newMessages.append({
           "role": item.role,
           "content": item.content
       }) 
   response = client.chat.completions.create(
       model=model,
       messages=newMessages,
       temperature=0,
       max_tokens=1000
   )

   # Returning the extracted response
   return response.choices[0].message.content

@app.post("/v1/chat-gpt")
async def chatV1(messages: List[Role]):
    return get_chat_completion(messages)

@app.post("/v2/chat-gpt")
async def chatV2():
    return "Để tính tổng của một mảng số trong JavaScript, bạn có thể sử dụng một trong các cách sau:\n\n1. Sử dụng vòng lặp for:\n```javascript\nfunction tinhTong(arr) {\n  let tong = 0;\n  for (let i = 0; i < arr.length; i++) {\n    tong += arr[i];\n  }\n  return tong;\n}\n\nlet mangSo = [1, 2, 3, 4, 5];\nconsole.log(tinhTong(mangSo)); // Kết quả: 15\n```\n\n2. Sử dụng phương thức reduce:\n```javascript\nlet mangSo = [1, 2, 3, 4, 5];\nlet tong = mangSo.reduce((accumulator, currentValue) => accumulator + currentValue, 0);\nconsole.log(tong); // Kết quả: 15\n```\n\n3. Sử dụng vòng lặp forEach:\n```javascript\nlet mangSo = [1, 2, 3, 4, 5];\nlet tong = 0;\nmangSo.forEach((so) => {\n  tong += so;\n});\nconsole.log(tong); // Kết quả: 15\n```\n\nCác cách trên đều sẽ tính tổng của các phần tử trong mảng số và trả về kết quả. Bạn có thể chọn cách nào phù hợp với nhu cầu của mình."

@app.post("/v3/chat-gpt")
async def chatV3():
    return "Open this HTML file in a browser, and as you scroll through the page, the current vertical scroll position will be displayed in the browser's console. Adjust the height property in the CSS to add more or less content and observe the scroll position changes."

@app.post("/v4/chat-gpt")
async def chatV4():
    return "Xin lỗi về sự nhầm lẫn trước đó. Dưới đây là một ví dụ về code JavaScript để tính tổng của các số trong một mảng:\n\n```javascript\n// Mảng chứa các số cần tính tổng\nconst numbers = [1, 2, 3, 4, 5];\n\n// Khởi tạo biến sum để lưu tổng\nlet sum = 0;\n\n// Duyệt qua từng phần tử trong mảng và cộng vào tổng\nfor (let i = 0; i < numbers.length; i++) {\n    sum += numbers[i];\n}\n\n// In ra tổng\nconsole.log(\"Tổng của các số trong mảng là: \" + sum);\n```\n\nTrong ví dụ trên, chúng ta khởi tạo một mảng `numbers` chứa các số cần tính tổng. Sau đó, chúng ta sử dụng một vòng lặp `for` để duyệt qua từng phần tử trong mảng và cộng vào biến `sum`. Cuối cùng, chúng ta in ra tổng của các số trong mảng."

## chat-gpt
# if __name__ == "__main__":
#     uvicorn.run(
#         app="api:app",
#         host="192.168.30.163",
#         port=8000,
#         reload=True
#     )