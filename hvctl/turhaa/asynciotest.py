import asyncio

xq = asyncio.Queue()

async def get_x():
    ret = await xq.get()
    return ret
    
def main():
    print('alkaa')
    x = get_x()
    xq.put(5)
    print(f'x={x}')
    
main()