#! /usr/bin/python3

import tbot

@tbot.testcase
def greet_user() -> None:
    with tbot.acquire_lab() as lh:
        name = lh.exec0("id", "--user", "--name").strip()

        tbot.log.message(f"Hello {name}!")
