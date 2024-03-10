from aiogram.fsm.state import StatesGroup, State


class VendorCode(StatesGroup):
    code = State()
