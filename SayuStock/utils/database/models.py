from typing import List, Optional

from sqlmodel import Field

from gsuid_core.webconsole.mount_app import PageSchema, GsAdminModel, site
from gsuid_core.utils.database.base_models import Bind, Type, T_Bind

from ..utils import convert_list
from ..watchlist_order import swap_adjacent, validate_full_reorder


class SsBind(Bind, table=True):
    __table_args__ = {"extend_existing": True}
    uid: str = Field(default=None, title="自选股票")
    push: Optional[str] = Field(
        title="股票状态推送",
        default="off",
        schema_extra={"json_schema_extra": {"hint": "开启股票推送"}},
    )

    @classmethod
    async def delete_uid(
        cls: Type[T_Bind],
        user_id: str,
        bot_id: str,
        uid: str,
        game_name: Optional[str] = None,
    ) -> int:
        result = await cls.get_uid_list_by_game(user_id, bot_id, game_name)
        if result is None:
            return -1

        result = convert_list(result)

        if uid not in result:
            return -1

        result.remove(uid)

        result = [i for i in result if i] if result else []
        new_uid = "_".join(result)

        if not new_uid:
            new_uid = None

        await cls.update_data(
            user_id,
            bot_id,
            **{cls.get_gameid_name(game_name): new_uid},
        )
        return 0

    @classmethod
    async def reorder_uid_list(
        cls: Type[T_Bind],
        user_id: str,
        bot_id: str,
        new_order: List[str],
        game_name: Optional[str] = None,
    ) -> int:
        """
        将自选按 new_order 完整重排。

        :return: 0 成功；-1 无自选；-2 顺序不合法
        """
        result = await cls.get_uid_list_by_game(user_id, bot_id, game_name)
        if not result:
            return -1
        current = convert_list(result)
        validated, err = validate_full_reorder(current, new_order)
        if err is not None or validated is None:
            return -2
        new_uid = "_".join(validated)
        if not new_uid:
            new_uid = None
        await cls.update_data(
            user_id,
            bot_id,
            **{cls.get_gameid_name(game_name): new_uid},
        )
        return 0

    @classmethod
    async def move_uid_order(
        cls: Type[T_Bind],
        user_id: str,
        bot_id: str,
        uid: str,
        delta: int,
        game_name: Optional[str] = None,
    ) -> int:
        """
        移动单只自选：delta=-1 上移，+1 下移。

        :return: 0 成功；-1 无自选；-2 代码不在列表；-3 已到边界
        """
        result = await cls.get_uid_list_by_game(user_id, bot_id, game_name)
        if not result:
            return -1
        current = convert_list(result)
        if uid not in current:
            return -2
        idx = current.index(uid)
        new_list, err = swap_adjacent(current, idx, delta)
        if err is not None or new_list is None:
            return -3
        new_uid = "_".join(new_list)
        await cls.update_data(
            user_id,
            bot_id,
            **{cls.get_gameid_name(game_name): new_uid},
        )
        return 0


@site.register_admin
class SsPushAdmin(GsAdminModel):
    pk_name = "id"
    page_schema = PageSchema(
        label="股票自选管理",
        icon="fa fa-bullhorn",
    )  # type: ignore

    # 配置管理模型
    model = SsBind
