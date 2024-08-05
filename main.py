import asyncio


async def main():
    print("Hello")
    await asyncio.sleep(1)
    counter = 0
    try:
        with open("test.txt", "r") as f:
            counter = int(f.read())
    except:
        pass
    try:
        with open("test.txt", "w") as f:
            counter += 1
            f.write(str(counter))
    except:
        pass
    print("world", counter)


if __name__ == "__main__":
    asyncio.run(main())