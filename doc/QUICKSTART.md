# 启动、开发与测试快速指南

SayuStock 是 **[gsuid_core](https://github.com/Genshin-bots/gsuid_core)（早柚核心）** 的插件，**不能单独 `python main.py` 启动**；需要先部署并启动核心，再由核心加载本插件。

更细的模块说明见 [MODULES.md](./MODULES.md)，测试细节见 [TESTING.md](./TESTING.md)。

---

## 一、如何启动（正式使用）

### 1. 前置条件

- 已按官方文档安装并配置 **gsuid_core**（与 GenshinUID / 其他基于核心的 Bot 部署方式一致）。
- 参考：[安装文档](http://docs.gsuid.gbots.work/#/)（根目录 [README.md](../README.md) 亦有安装提醒）。

### 2. 安装本插件与依赖

1. 在核心环境中安装插件，例如向 Bot 发送：`core安装插件SayuStock`，或将本仓库放到核心要求的插件目录并以可编辑方式安装。
2. 安装 Python 依赖（任选其一，与根目录 README 一致）：
   - `pdm run python -m pip install playwright plotly pandas`
   - 或 `poetry run pip install playwright plotly pandas`
   - 或 `uv run python -m pip install playwright plotly pandas`
3. 安装 Playwright 浏览器（**必须**，否则出图可能卡住）：
   - `playwright install`
4. 重启核心使插件生效，例如发送：`gs重启`（以你当前核心的指令为准）。

### 3. 启动核心服务

- 日常运行：按你部署 **gsuid_core** 的方式启动（如 systemd、Docker、或直接运行核心入口进程）。
- 插件随核心加载，无需再单独启动 SayuStock 进程。

### 4. 联调用的 HTTP 端口（可选）

- 仓库内 `test/single_stock_test.py` 默认向 `http://127.0.0.1:8765/api/send_msg` 发消息，用于本地联调。
- 若你的核心监听地址或端口不同，需改脚本中的 URL 或配置核心一致。

---

## 二、本地开发环境

### 1. 环境与克隆

- Python **3.12**（见 `pyproject.toml` 的 `requires-python`）。
- 克隆本仓库后建议创建虚拟环境：

```bash
cd /path/to/SayuStock
python3.12 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 2. 安装依赖

```bash
# 运行插件所需（与 README 一致）
pip install playwright plotly pandas
playwright install

# 可选：以可编辑方式安装包，便于 import
pip install -e .

# 开发依赖（pytest、后续若加入类型检查等）
pip install -e ".[dev]"
```

### 3. 在核心中加载本地代码

- 将本仓库目录放到核心配置的 **插件目录**，或 `pip install -e .` 到该 core 使用的同一虚拟环境，保证 **`import SayuStock` 能成功**（`SayuStock/__init__.py` 会导入 `gsuid_core`）。
- 修改代码后需 **重启核心** 或按核心的热重载方式生效。

### 4. 代码质量

- 使用 **Ruff**（见 `.pre-commit-config.yaml`）：

```bash
ruff check SayuStock test
ruff format SayuStock test
```

更多说明见 [DEVELOPMENT.md](./DEVELOPMENT.md)。

---

## 三、测试（与 [TESTING.md](./TESTING.md) 对应）

| 方式 | 用途 | 是否需要核心 |
|------|------|----------------|
| `pytest`（单元测试） | 校验纯逻辑（如 `watchlist_order`） | **否** |
| `single_stock_test.py` | 联调：发指令、保存返回图片 | **是**（需 core 在 8765 等可访问地址） |

推荐流程：**先 `pytest`**，再在核心环境做指令级验收。

---

## 文档索引

| 文档 | 内容 |
|------|------|
| [README.md](./README.md) | `doc/` 总索引 |
| [DEVELOPMENT.md](./DEVELOPMENT.md) | 开发约定、自选扩展、风格 |
| [TESTING.md](./TESTING.md) | 测试命令、联调步骤、注意事项 |
