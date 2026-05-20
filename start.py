from src.bootstrap.init import init

if __name__ == '__main__':
    init()

    print("OK..")
    print("Starting app")
    import asyncio
    from src.main import App

    bot = App()
    asyncio.run(bot._start())