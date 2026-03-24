# 测试说明

全文档索引见 [README.md](./README.md)。**启动核心、安装插件、开发环境搭建**见 [QUICKSTART.md](./QUICKSTART.md)。模块与测试目录对应关系见 [MODULES.md](./MODULES.md) 末尾「测试与脚本」一节。

---

## 一、单元测试（不依赖核心）

### 适用场景

- 校验纯函数、与数据库/网络无关的逻辑。
- 在 **未安装 gsuid_core** 的 CI 或最小环境中也可运行（当前 `watchlist_order` 测试用 `importlib` 加载模块，避免执行 `SayuStock/__init__.py`）。

### 环境准备

```bash
cd /path/to/SayuStock
python3.12 -m venv .venv && source .venv/bin/activate   # 可选
pip install -e ".[dev]"    # 或: pip install pytest
```

### 运行命令

```bash
# 运行全部测试
pytest

# 只跑自选顺序相关测试
pytest test/test_watchlist_order.py -v

# 查看收集到的用例（不执行）
pytest --collect-only
```

### 当前覆盖

- `SayuStock.utils.watchlist_order`：`validate_full_reorder`、`swap_adjacent`（自选排序与上下移的数学约束）。

配置见 `pyproject.toml` 中 `[tool.pytest.ini_options]`（`testpaths`、`pythonpath`、`addopts`）。

---

## 二、集成 / 联调测试（依赖核心）

### 脚本说明

`test/single_stock_test.py` 通过 **HTTP POST** 向本地 **gsuid_core** 暴露的接口发消息：

- 默认地址：`http://127.0.0.1:8765/api/send_msg`
- 消息体为 `MessageReceive`（`msgspec` 序列化），与核心约定一致。

### 前置条件

1. **已启动 gsuid_core**，且 HTTP API 与脚本中的 URL 一致（若端口不同，请修改脚本内 `http://127.0.0.1:8765`）。
2. 核心已加载 **SayuStock** 插件，且依赖已安装（含 `playwright install`）。
3. 脚本所在环境需安装：`httpx`、`msgspec`（与核心侧版本兼容即可），以及能访问 `gsuid_core.logger` 等（通常与核心同一环境运行最省事）。

### 运行示例

```bash
cd /path/to/SayuStock
# 在已安装 gsuid_core 与插件的环境中
python test/single_stock_test.py
```

脚本会依次发送多条指令（如 `个股 601919`），并将返回的 **base64 图片** 保存为当前目录下的 `*.jpg` 文件。

### 失败排查

| 现象 | 可能原因 |
|------|----------|
| 连接被拒绝 | 核心未启动或端口不是 8765 |
| 超时 | 首次出图需 Playwright，或网络拉取行情慢 |
| 无图片返回 | 插件未加载、指令无图、或响应结构与脚本预期不一致 |

---

## 三、推荐流程

1. **开发中**：改代码后先 `ruff check` / `ruff format`，再 `pytest`。
2. **联调**：启动核心 + 插件，运行 `single_stock_test.py` 或在 Bot 里发「我的自选」「大盘云图」等指令人工验收。
3. **发布前**：确保单元测试通过，并在目标环境至少验证一条出图指令。
