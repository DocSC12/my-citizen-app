import time
from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

ACCESS_TTL = 60  # ★ 教学:故意 60 秒过期,方便观察;生产一般 2 小时
REFRESH_TOKEN = "refresh-token-xyz-999"  # ★ 长期有效(生产一般 7~30 天)
issued_at = 0.0

class LoginForm(BaseModel):
    username: str
    password: str

def make_access_token():
    # 生产环境用 JWT(自带过期时间的签名令牌);教学版用"签发时间戳"模拟过期
    global issued_at
    issued_at = time.time()
    return "access-token-abc-123"

@app.post("/login")
def login(form: LoginForm):
    if form.username == "admin" and form.password == "123456":
        return {"code": 0, "msg": "ok",
                "data": {"accessToken": make_access_token(), "refreshToken": REFRESH_TOKEN}}
    return {"code": 1001, "msg": "账号或密码错误", "data": None}

@app.post("/refresh-token")
def refresh(refresh_token: str = Header(default="")):
    # ★ 只验 refreshToken 不验 accessToken——这就是"无感刷新"需要的后端配合
    if refresh_token == f"Bearer {REFRESH_TOKEN}":
        return {"code": 0, "msg": "ok", "data": {"accessToken": make_access_token()}}
    return JSONResponse(status_code=401, content={"code": 401, "msg": "refresh 也失效了", "data": None})

@app.get("/user-info")
def user_info(authorization: str = Header(default="")):
    valid = authorization == "Bearer access-token-abc-123" and (time.time() - issued_at) < ACCESS_TTL
    if valid:
        return {"code": 0, "msg": "ok", "data": {"nickname": "兰斯", "role": "admin"}}
    return JSONResponse(status_code=401, content={"code": 401, "msg": "accessToken 过期", "data": None})