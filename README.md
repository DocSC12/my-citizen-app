# my-citizen-app

> 城市公共服务小程序：政务服务大厅 + 出行查询，uni-app + FastAPI 全栈实现。
> 仿「临汾公众服务」小程序的独立复刻，个人学习项目。

## 功能特性

- **服务大厅**：轮播运营位、8 大服务宫格（社保 / 公积金 / 医疗挂号 / 生活缴费等）、政务公告
- **服务列表 / 详情**：分类过滤、办理材料、办理流程、一键拨打咨询热线
- **出行服务**：公交班次 / 站点 / 票价查询
- **登录鉴权（项目核心）**
  - 双 token 无感刷新：accessToken 过期后由 refreshToken 静默换新，请求队列挂起 + 重放，用户全程无感知
  - 登录安全：pydantic 参数校验（422 精确到字段）+ 密码连错 5 次锁定 10 分钟（HTTP 423 Locked）
  - 前端防连点锁，前后端双重校验
- **持久化登录态**：Pinia + Storage 双写，冷启动自动恢复

## 技术栈

| 层 | 技术 |
| --- | --- |
| 前端 | uni-app + Vue 3 + TypeScript + Pinia + UnoCSS（基于 unibest 模板） |
| 后端 | Python FastAPI + pydantic |
| 工程化 | ESLint + Husky + commitlint + vitest |

## 项目结构

```
├── src/
│   ├── pages/          # 页面：首页 / 登录 / 服务列表 / 服务详情 / 出行 / 我的
│   ├── http/http.ts    # 请求封装：401 无感刷新（单飞刷新 + 队列重放 + 防死循环保险丝）
│   ├── store/token.ts  # Pinia 双 token 管理（内存 + Storage 双写）
│   └── tabbar/          # 自定义 tabbar（角色可控）
└── server/
    └── main.py          # FastAPI 后端：校验 / 锁定 / 业务接口
```

## 快速启动

### 后端（FastAPI）

```bash
cd server
pip install fastapi uvicorn
uvicorn main:app --port 8000 --reload
```

接口文档自动生成：<http://127.0.0.1:8000/docs>

### 前端（uni-app 小程序）

```bash
pnpm install
pnpm dev:mp-weixin
```

用微信开发者工具导入 `dist/dev/mp-weixin`，并在详情中勾选「不校验合法域名」。

**测试账号**：`admin` / `123456`（accessToken 有效期故意设为 60 秒，便于观察无感刷新）

## 学习里程碑

| 提交 | 内容 |
| --- | --- |
| `feat: init` | unibest 模板初始化，跑通微信小程序 |
| `feat: page stack` | 页面路由实验：四种跳转 API / 页面栈 / onLoad 与 onShow |
| `feat: silent refresh` | 双 token 无感刷新全链路（前端队列 + FastAPI 后端） |
| `feat: full app` | 完整业务成品：校验层 + 锁定 + 服务 / 公告 / 公交接口 |

## 出处声明

- 项目骨架基于 [unibest](https://github.com/feige996/unibest) 模板（gitee 镜像同步）
- 双 token 无感刷新方案参考芋道源码 ruoyi-vue-pro 的单飞刷新 + 队列重放思路，简化为教学实现
- 业务形态参考「临汾公众服务」小程序