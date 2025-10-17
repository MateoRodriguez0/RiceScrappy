from fastapi import FastAPI
from ..services.megatiendas import get_product_info
app = FastAPI()
 
@app.get("/products")
async def products():
    return [get_product_info()]