from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from typing import Optional, Annotated

app = FastAPI()

player_inventory = []
game_locations ={
    "start":{
        "description":"You are just about to launch this game.",
        "items":["sword","matchete"]
    },
    "explore":{
        "description":"You are exploring this location",
        "items":["food","bullet"]
    },
    
    "end":{
        "description":"You have completed the game",
        "items":["key","points"]        
    }
}




class GameState(BaseModel):
    item_name: str
    description: str
    items_available: bool

@app.get("/") 
async def read_root():
    return {"message": "Welcome to the world of 👍Game!"}

@app.post("/inventory/add")
async def add_item_to_inventory(item:GameState,gamestate:GameState, q:Annotated,Query =(...,[str | None])):
    if item.item_name in [i["item_name"] for i in player_inventory]:
        raise HTTPException(status_code = 400,details ="the item name is duplicated and its not accepted")
    
    player_inventory.append(item.dict())
    return JSONResponse(status_code = 200,content ={"data":player_inventory,"message":"item added successfully to the inventory"})
    
    
@app.post("/inventoryy/remove")
async def delete_method(item:GameState):
    if item.item_name not in [i["item_name"] for i in player_inventory]:
        raise HTTPException(status_code = 404,details ="the item name is not in the inventory")
    player_inventory.remove(item.item_name)

    return JSONResponse(status_code = 200,content = {"data":GameState[item],"message":"item removed."})
        
        
@app.get("/explore/{location_name}")
async def explore_location(location_name:str):
    if location_name not in [l["Game_State"] for l in game_locations]:
        raise HTTPException(status_code = 404,detail ="the location does not exist")
    
    
    return JSONResponse(status_code = 200,content ={"data":GameState[location_name],"message":"location found"})
