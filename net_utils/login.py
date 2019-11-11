from typing import Tuple

from pyrogram import Client
from enum import Enum
import os
from pyrogram.client.types.authorization import *
from pyrogram.errors import *
from net_utils.default_config import default_config


class AuthState(Enum):
    READY = 1
    WAIT_FOR_PHONE = 2
    WAIT_FOR_CODE = 3
    WAIT_FOR_SIGN_UP = 4
    WAIT_FOR_PASSWORD = 5
    WAIT_FOR_TERMS = 6
    WAIT_FOR_REGISTER = 7


config_dir = os.environ.get('HOME', '.') + "/.config/pytelevim/"
config_path = config_dir+"cofig.ini"
app_name = "pytelevim"


def write_default_config():
    os.makedirs(config_dir, exist_ok=True)
    exists = os.path.isfile(config_path)
    if not exists:
        with open(config_path, "w") as f:
            f.write(default_config)


def create_client():
    write_default_config()
    app = Client(
        app_name,
        workdir="/tmp",
        config_file=config_path,
    )
    return app


async def login(client: Client):
    ist = await client.connect()
    if ist:
        return AuthState.READY
    return AuthState.WAIT_FOR_PHONE


async def send_phone(client: Client, phone: str) -> (AuthState, str):
    """
    :return str:
            Type of the current sent code.
            Can be *"app"* (code sent via Telegram), *"sms"* (code sent via SMS), *"call"* (code sent via voice call) or
            *"flash_call"* (code is in the last 5 digits of the caller's phone number).
    """

    sent_code = await client.send_code(phone)
    client.phone_number = phone
    client.session.sent_code = sent_code
    return AuthState.WAIT_FOR_CODE, sent_code.type


# call this function only after send_phone_
async def send_code(client: Client, code: str) -> Tuple[AuthState, str]:
    client.phone_code = code
    sent_code = client.session.sent_code
    try:
        r = await client.sign_in(client.phone_number, sent_code.phone_code_hash, client.phone_code)
    except SessionPasswordNeeded:
        return AuthState.WAIT_FOR_PASSWORD, ""

    if isinstance(r, TermsOfService):
        client.session.terms_of_service = r
        return AuthState.WAIT_FOR_TERMS, r.text
    if not r:
        return AuthState.WAIT_FOR_REGISTER, ""
    return AuthState.READY, ""


# call this function only after send_phone
async def accept_terms_of_service(client: Client) -> AuthState:
    try:
        await client.accept_terms_of_service(client.session.terms_of_service)
    except AssertionError:
        return AuthState.WAIT_FOR_TERMS
    return AuthState.WAIT_FOR_REGISTER


# call this function only after send_phone
async def register(client: Client, first_name: str, last_name: str) -> AuthState:
    try:
        await client.sign_up(client.phone_number, client.session.sent_code.phone_code_hash, first_name, last_name)
    except BadRequest:
        return AuthState.WAIT_FOR_REGISTER
    return AuthState.READY


# call this function only after send_phone
async def send_password(client: Client, password: str):
    try:
        await client.check_password(password)
    except BadRequest:
        return AuthState.WAIT_FOR_PASSWORD
    return AuthState.READY
