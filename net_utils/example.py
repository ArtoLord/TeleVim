from net_utils.login import *
import asyncio


async def main():
    cl = create_client()
    current_state = await login(cl)
    while True:
        if current_state == AuthState.READY:
            print("signed in")
            break
        if current_state == AuthState.WAIT_FOR_PHONE:
            a = input("enter phone number: ")
            current_state, state = await send_phone(cl, a)
            print("your code was sended by %s" % state)
            continue
        if current_state == AuthState.WAIT_FOR_CODE:
            a = input("enter your code: ")
            current_state, _ = await send_code(cl, a)
            continue
        print(current_state)


asyncio.run(main())
