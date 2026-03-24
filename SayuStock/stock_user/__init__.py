from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.logger import logger
from gsuid_core.models import Event

from ..utils.utils import get_vix_name
from ..utils.database.models import SsBind
from ..utils.stock.request_utils import get_code_id

sv_user_info = SV("股票用户信息", priority=1)

HINT1 = """[SayuStock]
你需要在命令后面加入你自选的股票！
例如: 添加自选 600000
你可以在命令后面加入多个股票，用空格隔开
例如: 添加自选 600000 光纤传媒
"""

HINT2 = """[SayuStock]
你需要在命令后面加入你要删除的股票！
例如: 删除自选 600000
你可以在命令后面加入多个股票，用空格隔开
例如: 删除自选 600000 光纤传媒
"""

HINT_SORT = """[SayuStock] 自选排序帮助
· 排序自选 <代码1> <代码2> ... — 按从左到右的顺序重排全部自选（须包含当前全部代码）
· 自选上移 <代码> — 在列表中上移一位
· 自选下移 <代码> — 在列表中下移一位
代码支持数字代码或简称，与「添加自选」一致。
"""


async def _token_to_stored_code(token: str) -> str | None:
    """将用户输入解析为库中存储的行情 ID（与添加自选逻辑一致）。"""
    _u = token.strip()
    if not _u:
        return None
    vix_name = get_vix_name(_u)
    if vix_name is None:
        code_id = await get_code_id(_u)
        if not code_id:
            return None
        return code_id[0]
    return f"VIX.{vix_name}"


@sv_user_info.on_command(("添加自选", "添加个股", "添加股票", "添加持仓", "加入自选"), block=True)
async def bind_uid(bot: Bot, ev: Event):
    qid = ev.user_id
    uid = ev.text.strip()
    logger.info(f"[SayuStock] 开始执行自选绑定, qid={qid}, uid={uid}")

    if not uid:
        return await bot.send(HINT1)

    u = uid.split(" ")
    add_dict = {}
    if not u:
        return await bot.send(HINT1)

    for _u in u:
        _u = _u.strip()
        if not _u:
            continue

        vix_name = get_vix_name(_u)
        if vix_name is None:
            code_id = await get_code_id(_u)
        else:
            code_id = f"VIX.{vix_name}", vix_name

        if not code_id:
            return await bot.send(f"❎[SayuStock] 股票[{_u}]不存在!")
        add_dict[f"{code_id[1]}({code_id[0]})"] = code_id[0]

    send_m = "\n".join(add_dict.keys())
    resp = await bot.receive_resp(
        f"是否确认将下列股票添加自选?\n{send_m}\n请输入是或否。",
    )
    if resp is not None:
        if resp.text == "是":
            for _u in add_dict:
                await SsBind.insert_uid(
                    qid,
                    ev.bot_id,
                    add_dict[_u],
                    ev.group_id,
                    is_digit=False,
                )
        else:
            return await bot.send("已取消!")

    return await bot.send("✅[SayuStock] 添加自选成功!\n可发送[我的自选]查看或发送[删除自选]清除！")


@sv_user_info.on_command(
    (
        "删除自选",
        "删除个股",
        "删除股票",
        "移除自选",
        "删除持仓",
    ),
    block=True,
)
async def delete_uid(bot: Bot, ev: Event):
    qid = ev.user_id
    uid = ev.text.strip()
    logger.info(f"[SayuStock] 开始执行自选解绑, qid={qid}, uid={uid}")

    if not uid:
        return await bot.send(HINT2)

    now_uid = await SsBind.get_uid_list_by_game(qid, ev.bot_id)
    if not now_uid:
        return await bot.send("您还未添加自选呢~请输入 添加自选 查看帮助!")

    u = uid.split(" ")
    add_dict = {}
    for _u in u:
        _u = _u.strip()
        if not _u:
            continue

        vix_name = get_vix_name(_u)
        if vix_name is None:
            code_id = await get_code_id(_u)
        else:
            code_id = f"VIX.{vix_name}", vix_name

        if not code_id:
            return await bot.send(f"❎[SayuStock] 股票[{_u}]不存在!")

        _name = f"{code_id[1]}({code_id[0]})"
        add_dict[_name] = code_id[0]

        if code_id[0] not in now_uid:
            return await bot.send(f"❎[SayuStock] 股票[{_name}]不在您的自选中!")

    _d = "\n".join(add_dict.keys())
    resp = await bot.receive_resp(f"是否确认将下列股票删除自选?\n{_d}\n请输入是或否。")
    if resp is not None:
        if resp.text == "是":
            for _u in add_dict:
                await SsBind.delete_uid(qid, ev.bot_id, add_dict[_u])
        else:
            return await bot.send("已取消!")

    await bot.send("✅[SayuStock] 删除自选成功!\n可发送[我的自选]查看或发送[添加自选]清除！")


@sv_user_info.on_command(("排序自选", "自选排序"), block=True)
async def reorder_watchlist(bot: Bot, ev: Event):
    """按用户给出的顺序重排全部自选。"""
    qid = ev.user_id
    raw = ev.text.strip()
    logger.info(f"[SayuStock] 排序自选, qid={qid}, raw={raw!r}")
    if not raw:
        return await bot.send(HINT_SORT)

    now_uid = await SsBind.get_uid_list_by_game(qid, ev.bot_id)
    if not now_uid:
        return await bot.send("您还未添加自选呢~请输入 添加自选 查看帮助!")

    tokens = [t for t in raw.split(" ") if t.strip()]
    if not tokens:
        return await bot.send(HINT_SORT)

    new_order: list[str] = []
    for t in tokens:
        code = await _token_to_stored_code(t)
        if code is None:
            return await bot.send(f"❎[SayuStock] 股票[{t}]不存在!")
        new_order.append(code)

    rc = await SsBind.reorder_uid_list(qid, ev.bot_id, new_order)
    if rc == -2:
        return await bot.send(
            "❎[SayuStock] 排序失败：请按「当前全部自选」列出顺序，"
            "不可重复、不可遗漏。\n可先发「我的自选」查看现有代码。"
        )
    return await bot.send(
        "✅[SayuStock] 自选顺序已更新!\n发送[我的自选]可查看新顺序。"
    )


@sv_user_info.on_command(("自选上移",), block=True)
async def move_watchlist_up(bot: Bot, ev: Event):
    """将指定自选在列表中上移一位。"""
    qid = ev.user_id
    raw = ev.text.strip()
    logger.info(f"[SayuStock] 自选上移, qid={qid}, raw={raw!r}")
    if not raw:
        return await bot.send(HINT_SORT)

    code = await _token_to_stored_code(raw.split()[0])
    if code is None:
        return await bot.send(f"❎[SayuStock] 股票[{raw}]不存在!")

    rc = await SsBind.move_uid_order(qid, ev.bot_id, code, -1)
    if rc == -1:
        return await bot.send("您还未添加自选呢~请输入 添加自选 查看帮助!")
    if rc == -2:
        return await bot.send("❎[SayuStock] 股票不在您的自选中!")
    if rc == -3:
        return await bot.send("❎[SayuStock] 已经是第一个，无法上移。")
    return await bot.send("✅[SayuStock] 已上移!\n发送[我的自选]查看。")


@sv_user_info.on_command(("自选下移",), block=True)
async def move_watchlist_down(bot: Bot, ev: Event):
    """将指定自选在列表中下移一位。"""
    qid = ev.user_id
    raw = ev.text.strip()
    logger.info(f"[SayuStock] 自选下移, qid={qid}, raw={raw!r}")
    if not raw:
        return await bot.send(HINT_SORT)

    code = await _token_to_stored_code(raw.split()[0])
    if code is None:
        return await bot.send(f"❎[SayuStock] 股票[{raw}]不存在!")

    rc = await SsBind.move_uid_order(qid, ev.bot_id, code, 1)
    if rc == -1:
        return await bot.send("您还未添加自选呢~请输入 添加自选 查看帮助!")
    if rc == -2:
        return await bot.send("❎[SayuStock] 股票不在您的自选中!")
    if rc == -3:
        return await bot.send("❎[SayuStock] 已经是最后一个，无法下移。")
    return await bot.send("✅[SayuStock] 已下移!\n发送[我的自选]查看。")
