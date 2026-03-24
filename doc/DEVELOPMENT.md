# 开发说明

## 文档导航

- **[doc/README.md](./README.md)**：文档索引（MODULES / SKILLS / 测试 / 东财字段等）。
- **[MODULES.md](./MODULES.md)**：**全模块** 包级与主要文件说明，改代码前建议先查对应小节。

## 环境

- Python **3.12**（见 `pyproject.toml` 的 `requires-python`）。
- 依赖：`playwright`、`plotly`、`pandas` 等；安装方式见根目录 `README.md`。

## 代码风格

- 使用 **Ruff** 做 lint 与 format（见 `.pre-commit-config.yaml`）。
- 提交前可执行：`ruff check SayuStock test` / `ruff format SayuStock test`。

## 测试

详见 [TESTING.md](./TESTING.md)。

## 自选排序扩展

若需增加「按涨跌幅排序」等自动规则：

1. 在拉取行情后得到每只标的的排序键；
2. 生成新的代码 ID 列表 `new_order`；
3. 调用 `SsBind.reorder_uid_list(user_id, bot_id, new_order)` 写回。

自动排序前建议向用户二次确认，避免与手动顺序预期冲突。
