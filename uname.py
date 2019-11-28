import tbot

@tbot.testcase
def test_uname() -> None:
    with tbot.acquire_lab() as lh:
        with tbot.acquire_board(lh) as b:
            with tbot.acquire_linux(b) as lnx:
                lnx.exec0("uname", "-a")
