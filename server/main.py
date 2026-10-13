import time
from fastapi import FastAPI, Header, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="my-citizen-app 教学后端")

# ================= 双 token(教学内存版) =================
ACCESS_TTL = 60  # 教学:故意 60 秒过期方便观察;生产一般 2 小时
REFRESH_TOKEN = "refresh-token-xyz-999"  # 长期有效(生产一般 7~30 天)
issued_at = 0.0

# ================= 登录安全:密码错误锁定 =================
MAX_FAIL = 5        # 连错 5 次
LOCK_SECONDS = 600  # 锁 10 分钟
fail_count = 0      # 教学版只记总数;生产按用户名分别记(Redis key: login:fail:{username})
locked_until = 0.0

# ================= 内存"数据库"(生产换 MySQL) =================
SERVICES = [
    {"id": 1001, "title": "社保查询", "icon": "🏥", "category": "social", "desc": "查询个人社保缴费记录、余额"},
    {"id": 1002, "title": "公积金", "icon": "🏛️", "category": "fund", "desc": "公积金余额与缴存明细查询"},
    {"id": 1003, "title": "医疗挂号", "icon": "🩺", "category": "medical", "desc": "全市医院预约挂号"},
    {"id": 1004, "title": "入学报名", "icon": "🎓", "category": "edu", "desc": "中小学入学网上报名"},
    {"id": 1005, "title": "交通违章", "icon": "🚗", "category": "traffic", "desc": "违章查询与罚款缴纳"},
    {"id": 1006, "title": "生活缴费", "icon": "💡", "category": "life", "desc": "水电气暖一站式缴费"},
    {"id": 1007, "title": "电子证照", "icon": "🪪", "category": "cert", "desc": "电子身份证、驾驶证、行驶证"},
    {"id": 1008, "title": "便民热线", "icon": "☎️", "category": "hotline", "desc": "12345 政务服务热线"},
]

ANNOUNCEMENTS = [
    {"id": 1, "title": "2026 年度城乡居民医保缴费开始", "date": "10-08"},
    {"id": 2, "title": "公交线路优化调整公告(10 月 15 日起)", "date": "10-10"},
    {"id": 3, "title": "政务服务大厅周末延时服务上线", "date": "10-12"},
]

# 详情数据:个别服务定制,其余走 DEFAULT_DETAIL
DETAILS = {
    1001: {"steps": ["实名认证", "选择查询险种", "生成缴费明细"], "materials": ["身份证", "社保卡"], "hotline": "12333"},
    1003: {"steps": ["选择医院科室", "选择就诊日期", "确认挂号并取号"], "materials": ["身份证", "就诊卡"], "hotline": "12320"},
}
DEFAULT_DETAIL = {
    "steps": ["实名认证", "填写申请信息", "提交审核", "等待结果通知"],
    "materials": ["身份证"],
    "hotline": "12345",
}


# ================= 请求体 schema(pydantic 校验层) =================
class LoginForm(BaseModel):
    username: str = Field(min_length=3, max_length=20, description="用户名 3-20 字符")
    password: str = Field(min_length=6, max_length=20, description="密码 6-20 字符")


def make_access_token():
    # 生产环境用 JWT(自带过期时间的签名令牌);教学版用"签发时间戳"模拟过期
    global issued_at
    issued_at = time.time()
    return "access-token-abc-123"


@app.post("/login")
def login(form: LoginForm):
    global fail_count, locked_until
    now = time.time()

    # 1. 先查锁:锁定期内直接拒绝,连密码都不校验(防暴力破解)
    if now < locked_until:
        remain = int((locked_until - now) / 60) + 1
        return JSONResponse(status_code=423, content={"code": 423, "msg": f"错误次数过多已锁定,约 {remain} 分钟后重试", "data": None})
    # 锁过期则计数归零,重新累计
    if locked_until and now >= locked_until:
        fail_count = 0
        locked_until = 0.0

    # 2. 账号密码校验(生产:查库 + bcrypt 哈希比对,绝不存明文)
    if form.username == "admin" and form.password == "123456":
        fail_count = 0  # 登录成功即清零
        return {"code": 0, "msg": "ok", "data": {"accessToken": make_access_token(), "refreshToken": REFRESH_TOKEN}}

    # 3. 失败计数 + 触发锁定
    fail_count += 1
    if fail_count >= MAX_FAIL:
        locked_until = now + LOCK_SECONDS
        return {"code": 1002, "msg": "密码错误次数过多,账号已锁定 10 分钟", "data": None}
    return {"code": 1001, "msg": f"账号或密码错误,再错 {MAX_FAIL - fail_count} 次将锁定", "data": None}


@app.post("/refresh-token")
def refresh(refresh_token: str = Header(default="")):
    # 只验 refreshToken 不验 accessToken——这就是"无感刷新"需要的后端配合
    if refresh_token == f"Bearer {REFRESH_TOKEN}":
        return {"code": 0, "msg": "ok", "data": {"accessToken": make_access_token()}}
    return JSONResponse(status_code=401, content={"code": 401, "msg": "refresh 也失效了", "data": None})


@app.get("/user-info")
def user_info(authorization: str = Header(default="")):
    valid = authorization == "Bearer access-token-abc-123" and (time.time() - issued_at) < ACCESS_TTL
    if valid:
        return {"code": 0, "msg": "ok", "data": {"nickname": "兰斯", "role": "admin"}}
    return JSONResponse(status_code=401, content={"code": 401, "msg": "accessToken 过期", "data": None})


# ================= 公开业务接口(不需要登录,浏览器/未登录可访问) =================
@app.get("/announcements")
def announcements():
    return {"code": 0, "msg": "ok", "data": ANNOUNCEMENTS}


@app.get("/services")
def services(category: str = Query(default="")):
    data = [s for s in SERVICES if not category or s["category"] == category]
    return {"code": 0, "msg": "ok", "data": data}


@app.get("/service-detail")
def service_detail(id: int = Query(...)):
    base = next((s for s in SERVICES if s["id"] == id), None)
    if base is None:
        return {"code": 1003, "msg": "服务不存在", "data": None}
    detail = DETAILS.get(id, DEFAULT_DETAIL)
    return {"code": 0, "msg": "ok", "data": {**base, **detail}}


@app.get("/bus-line")
def bus_line(line: str = Query(min_length=1)):
    return {"code": 0, "msg": "ok", "data": {
        "line": line,
        "direction": "开往 市政务服务中心",
        "nextBuses": ["08:30", "08:45", "09:00"],
        "firstBus": "06:30",
        "lastBus": "21:30",
        "stations": ["火车站", "解放路口", "平阳广场", "市政务服务中心"],
        "fare": "1 元(刷卡 0.9 元)",
    }}