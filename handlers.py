import asyncio
import re

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.orm import orm_request, orm_get_db, orm_add_user, orm_update_user, orm_get_user
from keyboards import keyboard, inline_button
from states import VendorCode
from utils.get_product import get_info

router = Router()


@router.message(Command('start'))
async def start_handler(msg: types.Message, session: AsyncSession) -> None:
    try:
        await orm_add_user(session, msg)
        await msg.answer('<b>Добро пожаловать! 🖖 Ваш ID пользователя занесен в базу данных!</b>',
                         reply_markup=keyboard)
    except IntegrityError:
        await msg.answer('<b>Добро пожаловать! 🖖 Ваш ID уже есть в базе данных!</b>',
                         reply_markup=keyboard)


@router.message(F.text == 'Получить информацию по товару')
async def get_button(msg: types.Message, state: FSMContext) -> None:
    await msg.answer(text='<b>Введите артикул товара c <em>Wildberries</em></b>  🖊')
    await state.set_state(VendorCode.code)


@router.message(VendorCode.code, F.text)
async def enter_code(msg: types.Message, state: FSMContext, session: AsyncSession) -> None:
    await state.update_data(code=msg.text)
    data = await state.get_data()
    try:
        result = await get_info(data)
        await orm_request(session, data, msg)
        await msg.answer(text=result, reply_markup=inline_button)
    except:
        await msg.answer(text='<b>Что-то пошло не так... Проверьте корректность вводимых данных</b>')
    await state.clear()


@router.message(F.text == 'Получить информацию из БД')
async def get_DB(msg: types.Message, session: AsyncSession) -> None:
    db_result = await orm_get_db(session, msg)
    if db_result:
        await msg.answer(text='<b>Последние запросы:</b>')
        for obj in db_result:
            await msg.answer(text=f'<b>ID запроса:</b> <u>{obj.id}</u>\n'
                                  f'<b>ID пользователя:</b> <u>{obj.user_id}</u>\n'
                                  f'<b>Дата и время запроса:</b> <u>{obj.time}</u>\n'
                                  f'<b>Запрашиваемый артикул:</b> <u>{obj.vendor_code}</u>')
    else:
        await msg.answer(text='<b>В базе данных запросов нет</b>')


@router.callback_query()
async def subscribe_callback(callback: CallbackQuery, session: AsyncSession) -> None:
    if callback.data == 'True':
        code = re.split(r'\s', re.search(r'Артикул: (\S+)', callback.message.text)[0])
        await orm_update_user(session, callback.from_user.id, flag=True)
        await callback.message.answer(text='<b>💥 Подписка включена 💥</b>')
        while True:
            await asyncio.sleep(300)
            user = await orm_get_user(session, callback.from_user.id)
            if user.spam:
                result = await get_info({'code': code[1]})
                await callback.message.answer(result)
            else:
                break


@router.message(F.text == 'Остановить уведомления')
async def get_button(msg: types.Message, session: AsyncSession) -> None:
    await orm_update_user(session, msg.from_user.id, flag=False)
    await msg.answer(text='<b>Подписки отменены</b>  ❌')
