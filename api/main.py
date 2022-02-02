import os
import json
import requests
from typing import Dict
from fastapi import FastAPI, Depends, Request, APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI, version

from sqlalchemy.orm import Session
from .database import SessionLocal, engine

from . import models
from .models import FruitsModel
from .schemas import Fruits

# Database migration, see https://fastapi.tiangolo.com/tutorial/sql-databases/
models.Base.metadata.create_all(bind=engine)


# Dependency for database session, see https://fastapi.tiangolo.com/tutorial/sql-databases/
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Fast API app, see https://fastapi.tiangolo.com/
app = FastAPI()
root = APIRouter(tags=['root'])
app_route = APIRouter()


@root.get("/")
def read_root(request: Request):
    url_list = [
        route.path
        for route in request.app.routes
    ]

    app_router_list = [route.path
                       for route in app_route.routes]

    return {"endpoints": set(url_list+app_router_list)}


@app_route.get('/foo')
@version(1)
def foo():
    return "foo V1"


@app_route.get('/foo')
@version(2)
def foo():
    return "foo V2"


@app_route.get('/fruits')
@version(1)
def get_fruits(db: Session = Depends(get_db)):
    """Handle fruits (Postgres integration)"""
    seed(db)
    fruits = db.query(models.FruitsModel).all()
    results = [
        {
            "name": fruit.name,
            "price": fruit.price
        } for fruit in fruits]
    return JSONResponse({"items": results})


@app_route.post('/fruits')
@version(1)
def post_fruits(fruit: Fruits, db: Session = Depends(get_db)):
    new_fruit = FruitsModel(name=fruit.name, price=fruit.price)
    db.add(new_fruit)
    db.commit()
    return {"message": f"fruit {new_fruit.name} has been created successfully."}


@app_route.post('/predict')
@version(1)
def predict_response(request: Dict):
    """Execute a prediction."""
    try:
        data = json.dumps(request)
        headers = {'Content-type': 'application/json'}
        url = os.environ.get('MLFLOW_ENDPOINT')
        post_response = requests.post(url, data=data, headers=headers)
        return post_response.json()
    except Exception as exc:
        return JSONResponse(status_code=500, content={'error': 'Error calling model engine: ' + str(exc)})


# Versioned Fast API app, see https://github.com/DeanWay/fastapi-versioning
app.include_router(app_route)

app = VersionedFastAPI(app, enable_latest=True, version_format='{major}', prefix_format='/v{major}')
app.include_router(root)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def seed(db: Session = Depends(get_db)):
    fruits = db.query(models.FruitsModel).all()
    if len(fruits) == 0:
        db.add(FruitsModel(name='Apples', price=1.2))
        db.add(FruitsModel(name='Oranges', price=3.4))
        db.commit()
