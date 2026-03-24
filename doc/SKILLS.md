# SayuStock 项目技能（Skills）

本文档概括本仓库的能力边界与协作要点，便于 AI 助手与贡献者快速对齐上下文。

**更细的逐文件说明**（覆盖全部模块）见 **[MODULES.md](./MODULES.md)**；**启动、开发、测试**见 **[QUICKSTART.md](./QUICKSTART.md)**；文档总索引见 **[README.md](./README.md)**。

## 项目定位

- **SayuStock**：基于 [gsuid_core](https://github.com/Genshin-bots/gsuid_core) 的股票 Bot 插件，面向 QQ/微信/Telegram 等多端。
- **核心能力**：行情图（Plotly/Playwright）、自选管理、云图、新闻等；数据多来自东方财富等公开接口（见 [eastmoneyApi.md](./eastmoneyApi.md)）。

## 目录与职责（总览）

| 路径 | 说明 |
|------|------|
| `SayuStock/stock_user/` | 用户自选：添加、删除、**排序**（上移/下移/全量重排） |
| `SayuStock/stock_info/` | 大盘概览、我的自选、全天候、基金持仓等出图与指令 |
| `SayuStock/stock_cloudmap/` | 大盘/行业/概念云图、个股与 K 线、对比个股 |
| `SayuStock/stock_news/` | 雪球 7×24 订阅与推送 |
| `SayuStock/stock_status/` | 插件状态（订阅数、自选账户数） |
| `SayuStock/stock_sina/` | 市盈率/市净率对比图 |
| `SayuStock/stock_ai/` | 模型/AI 趋势预测图 |
| `SayuStock/stock_config/` | `STOCK_CONFIG` 插件配置 |
| `SayuStock/utils/` | 通用工具、行情请求、数据库 `SsBind`、`watchlist_order` |
| `SayuStock/tools/` | 离线数据脚本（如 `gen_A.py`） |

## 自选数据模型

- 用户在库中的自选以 **下划线拼接** 的行情 ID 字符串存于 `SsBind.uid`。
- 展示顺序与拼接顺序一致；`convert_list` 会处理带下划线的代码分段。
- 排序相关逻辑：**先**用 `validate_full_reorder` / `swap_adjacent` 校验，**再** `update_data` 写回。

## Bot 指令（排序）

- `排序自选` / `自选排序` + 空格分隔的**全部**自选代码（顺序即目标顺序）。
- `自选上移` / `自选下移` + 单个代码，相邻交换。

## 修改代码时的注意点

- 解析用户输入的行情 ID 应与「添加自选」一致：普通标的用 `get_code_id` 返回的 `QuoteID`，VIX 类为 `VIX.xxx`（见 `stock_user._token_to_stored_code`）。
- 避免破坏 `convert_list` 对存储格式的假设；数据库层统一用 `convert_list` 后再比较或重排。
