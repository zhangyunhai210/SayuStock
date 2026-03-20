# 测试说明

## 单元测试（推荐）

不依赖 gsuid_core 运行中的 Bot，仅校验纯逻辑：

```bash
cd /workspace
pip install -e ".[dev]"   # 或 pip install pytest
pytest
```

当前覆盖：

- `SayuStock.utils.watchlist_order`：`validate_full_reorder`、`swap_adjacent`（自选排序与上下移的数学约束）。

配置见 `pyproject.toml` 中 `[tool.pytest.ini_options]`。`watchlist_order` 的测试通过 `importlib` 直接加载模块文件，避免 `import SayuStock` 时依赖未安装的 `gsuid_core`。

## 集成 / 联调测试

`test/single_stock_test.py` 通过 HTTP 向本地 **gsuid_core** 的 `8765` 端口发消息，用于真机联调；运行前需先启动核心服务。

## 流程建议

1. 修改自选或顺序相关代码后，先跑 `pytest`。
2. 再在装有核心的环境中用「我的自选」「排序自选」等指令做人工验收。
