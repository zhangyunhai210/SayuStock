# SayuStock 全模块说明

本文档按代码目录梳理 **整个项目** 各模块职责，便于定位功能与二次开发。插件依赖 [gsuid_core](https://github.com/Genshin-bots/gsuid_core)（`SV` 指令、`Bot`、`Event`、数据库、调度器等）。

---

## 根目录与版本

| 路径 | 说明 |
|------|------|
| `SayuStock/version.py` | `SayuStock_version`，与发布说明中的版本号对应。 |
| `SayuStock/__init__.py` | 向 `gsuid_core` 注册插件（`Plugins`）；运行环境需已安装核心。 |
| `pyproject.toml` / `README.md` | 项目元数据、依赖与安装说明。 |

---

## `SayuStock/stock_user/` — 用户自选

| 文件 | 说明 |
|------|------|
| `__init__.py` | 指令：**添加/删除自选**；**排序自选、自选上移、自选下移**；解析股票代码与 `SsBind` 交互。 |

**依赖**：`SsBind`、`get_code_id`、`get_vix_name`。

---

## `SayuStock/stock_info/` — 大盘、自选图、基金、全天候

| 文件 | 说明 |
|------|------|
| `__init__.py` | 指令：**大盘概览/大盘概况**、**我的自选/我的持仓/我的股票**、**全天候/全天候板块**、**基金持仓/持仓分布**；定时任务每日 23:00 保存大盘数据。 |
| `draw_info.py` | 大盘概览图（Plotly/PIL 等）。 |
| `draw_info_pil.py` | 大盘相关 PIL 绘制辅助。 |
| `draw_my_info.py` | **我的自选** 长图：主指数、自选列表 `draw_bar`、涨跌汇总。 |
| `draw_future.py` | **全天候** 板块图。 |
| `draw_fund_info.py` | **基金持仓**：拉取基金持仓 API，绘制持仓条形图。 |
| `get_jp_data.py` | 日本/相关市场数据（若被其他绘制逻辑引用）。 |

---

## `SayuStock/stock_cloudmap/` — 云图、个股、对比

| 文件 | 说明 |
|------|------|
| `__init__.py` | 指令：**大盘云图**、**板块云图/行业云图**、**概念云图**、**个股**（含 K 线周期前缀）、**我的个股**、**对比个股/个股对比**；定时 0:20 清理 `DATA_PATH` 缓存。 |
| `get_cloudmap.py` | 核心：Plotly 生成云图、个股、K 线、单品种对比等；调用 `render_image_by_pw`（Playwright）、行情接口 `get_gg`/`get_vix`/板块数据等。 |
| `get_compare.py` | 多标的对比图：`to_compare_fig`、归一化曲线。 |
| `utils.py` | K 线填充 `fill_kline` 等与云图/对比共用的数据处理。 |

**`MS_MAP`**（`__init__.py`）：`5k`、`日k`、`周k` 等前缀与 K 线周期代码映射。

---

## `SayuStock/stock_news/` — 雪球新闻订阅

| 文件 | 说明 |
|------|------|
| `__init__.py` | 指令：**订阅雪球新闻/热点**、**取消订阅**；定时任务拉取雪球 7×24，向订阅会话推送；`TASK_NAME` 与 `stock_status` 共用。 |

**依赖**：`utils/request.py`（`get_news`、`clean_news`）、`gs_subscribe`。

---

## `SayuStock/stock_status/` — 插件状态展示

| 文件 | 说明 |
|------|------|
| `__init__.py` | 向核心注册状态：**启用订阅** 数量、**自选账户** 数量（`SsBind.get_all_data`），供 Web 控制台/状态页展示。 |

---

## `SayuStock/stock_sina/` — 新浪市盈/市净对比

| 文件 | 说明 |
|------|------|
| `__init__.py` | 指令前缀：**市盈率对比**、**市净率对比**。 |
| `gen_image.py` | `get_sina_pepb_compare`：生成对比图。 |

---

## `SayuStock/stock_ai/` — AI/趋势预测图

| 文件 | 说明 |
|------|------|
| `__init__.py` | 指令前缀：**模型预测**、**ai预测**/**AI预测**、**趋势预测**。 |
| `draw_ai_map.py` | `draw_ai_kline_with_forecast`：K 线与预测可视化。 |

---

## `SayuStock/stock_config/` — 插件配置

| 文件 | 说明 |
|------|------|
| `stock_config.py` | `STOCK_CONFIG`：`StringConfig`，与核心插件配置系统集成。 |
| `config_default.py` | 默认配置项（如云图刷新间隔等）。 |

**依赖**：`utils/resource_path.py` 中的 `CONFIG_PATH`。

---

## `SayuStock/utils/` — 通用工具

| 文件 | 说明 |
|------|------|
| `utils.py` | `convert_list`（自选下划线拼接解析）、`get_vix_name`、`number_to_chinese` 等。 |
| `watchlist_order.py` | 自选**全量重排校验**、**相邻交换**纯函数（供 `SsBind` 与单测）。 |
| `constant.py` | 常量：错误文案、`VIX_LIST`、`code_id_dict`、板块字典等。 |
| `resource_path.py` | `DATA_PATH`、`CONFIG_PATH` 等资源路径。 |
| `image.py` | 页脚、通用 `render_image_by_pw`（Playwright 出图）等。 |
| `request.py` | 雪球新闻：`get_token`、`get_news`、`clean_news`；Playwright 与 aiohttp。 |
| `models.py` | 雪球等数据结构模型（如 `XueQiu7x24`）。 |
| `load_data.py` | 数据加载辅助。 |
| `time_range.py` | 交易时段/分钟数等（云图 K 线使用）。 |
| `get_OKX.py` | OKX 相关 K 线/频率映射（与数字货币或扩展行情有关）。 |

### `database/`

| 文件 | 说明 |
|------|------|
| `models.py` | `SsBind`：自选 `uid`（下划线拼接）、推送开关；**增删改自选**、**重排/上移下移**；Web 控制台 `SsPushAdmin`。 |

### `stock/`

| 文件 | 说明 |
|------|------|
| `request.py` | 东方财富等行情：`get_gg`、`get_vix`、`get_mtdata`、`get_hotmap`、`get_menu` 等。 |
| `request_utils.py` | `get_code_id`（搜索/解析代码）、`get_fund_pos_list`、`get_image_from_em` 等。 |
| `utils.py` | 行情缓存、文件工具。 |
| `get_vix.py` | VIX 指数相关拉取。 |

---

## `SayuStock/tools/` — 维护脚本

| 文件 | 说明 |
|------|------|
| `gen_A.py` | 从 JSON 批量提取 `SECUCODE` 等，用于生成/维护数据文件（非 Bot 运行时路径）。 |

---

## 外部数据与接口文档

- 东方财富相关接口说明见 **[eastmoneyApi.md](./eastmoneyApi.md)**。
- 雪球、新浪等接口分散在 `utils/request.py`、`stock_sina/gen_image.py`、`utils/stock/request.py` 中，修改时需注意反爬与频率限制。

---

## 模块依赖关系（简图）

```
stock_user / stock_info / stock_cloudmap / stock_news / …
        ↓
utils (database.models, stock.request, image, …)
        ↓
stock_config (STOCK_CONFIG) / resource_path
```

绘图与云图路径：`get_cloudmap.render_image` → Plotly → `render_image_by_pw`（Playwright）。

---

## 测试与脚本

| 路径 | 说明 |
|------|------|
| `test/` | 单元测试（如 `watchlist_order`）；详见 [TESTING.md](./TESTING.md)。 |
| `test/single_stock_test.py` | 本地 HTTP 联调 core，非 CI 默认项。 |

若需为某模块补充更细的「函数级」说明，建议在该包内增加简短模块 docstring，并在本文件中增加对应小节链接。
