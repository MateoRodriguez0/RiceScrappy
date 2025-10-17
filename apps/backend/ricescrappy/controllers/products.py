from fastapi import FastAPI
from concurrent.futures import ThreadPoolExecutor
import asyncio
from ..services.megatiendas import get_product_info as megatienda_info
from ..services.D1 import get_product_info as d1_info
from ..services.Exito import get_product_info as exito_info
from ..services.Jumbo import get_product_info as jumbo_info
from ..services.LaRebaja import get_product_info as rebaja_info
from ..services.Olimpica import get_product_info as olimpica_info

app = FastAPI()

@app.get("/products")
async def products():
    return [
        megatienda_info(), 
        olimpica_info()
    ]

@app.get("/products/all")
async def products_all():
    loop = asyncio.get_running_loop()
    funcs = [
        megatienda_info,
        d1_info,
        exito_info,
        jumbo_info,
        rebaja_info,
        olimpica_info
    ]
    results = []
    # Use ThreadPoolExecutor for concurrent execution of blocking functions
    with ThreadPoolExecutor(max_workers=len(funcs)) as executor:
        tasks = [loop.run_in_executor(executor, func) for func in funcs]
        for coro in asyncio.as_completed(tasks):
            try:
                result = await coro
                results.append(result)
            except Exception as e:
                results.append({"error": str(e)})
    return results
