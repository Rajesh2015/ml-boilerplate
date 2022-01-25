import json
import logging
import os
from logging.config import dictConfig
from .helper.logconfig import LogConfig
from fastapi import APIRouter, Depends, Request
import uvicorn
import requests
from .model import fruitmodel
from .model.fruitmodel import FruitsModel
from .model.Schemas import Fruits
from .helper.APIVersion import *
from .helper.db import get_db, engine
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from functools import lru_cache
from os import environ, path
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseSettings
from sqlalchemy.orm import Session

prefix_router = APIRouter()

basedir = path.abspath(path.dirname(__file__))
base_path = Path(__file__).parent
load_dotenv(path.join(basedir, '.env'))


class Config(BaseSettings):
    NAME = environ.get('NAME')
    DEBUG = False
    PORT = environ.get('PORT')
    major_version = 1
    minor_version = 0


@lru_cache()
def get_settings():
    return Config()


settings: Config = get_settings()
application = FastAPI(title=settings.NAME)
dictConfig(LogConfig().dict())
logger = logging.getLogger(settings.NAME)
origins = ["*"]

application.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@application.on_event("startup")
async def on_startup():
    fruitmodel.Base.metadata.create_all(bind=engine)


@prefix_router.get("/")
async def info():
    """
    Info
    """
    return f'{settings.NAME}-{settings.major_version}.{settings.minor_version} Endpoints: /api/v1.0/test, ' \
           f'/api/v1.0/predict" '


@prefix_router.get('/api/v1.0/fruits')
def get_fruits(db: Session = Depends(get_db)):
    """Handle fruits (Postgres integration)"""
    seed(db)
    fruits = db.query(fruitmodel.FruitsModel).all()
    results = [
        {
            "name": fruit.name,
            "price": fruit.price
        } for fruit in fruits]
    return JSONResponse({"items": results})


@prefix_router.post('/api/v1.0/fruits')
def post_fruits(fruit: Fruits, db: Session = Depends(get_db)):
    # print(fruit)
    logger.info(fruit)
    new_fruit = FruitsModel(name=fruit.name, price=fruit.price)
    db.add(new_fruit)
    db.commit()
    return {"message": f"fruit {new_fruit.name} has been created successfully."}


@prefix_router.post('/api/v1.0/predict')
def post_predict_response(request: Dict):
    """Execute a prediction."""
    logger.info(request)
    return predict_response(request)


@prefix_router.options('/api/v1.0/predict')
def option_predict_response(request: Dict):
    return predict_response(request)


def predict_response(request: Dict):
    """Execute a prediction."""
    try:
        data = json.dumps(request)
        headers = {'Content-type': 'application/json'}
        url = os.environ.get('MLFLOW_ENDPOINT')
        post_response = requests.post(url, data=data, headers=headers)
        logger.info(post_response.json())
        return post_response.json()
    except Exception as exc:
        logger.error(exc)
        return JSONResponse(status_code=500, content={'error': 'Error calling model engine: ' + str(exc)})


def seed(db: Session = Depends(get_db)):
    fruits = db.query(fruitmodel.FruitsModel).all()
    if len(fruits) == 0:
        db.add(FruitsModel(name='Apples', price=1.2))
        db.add(FruitsModel(name='Oranges', price=3.4))
        db.commit()


application.include_router(prefix_router)

if __name__ == "__main__":
    application.logger.info('Starting the app')
    uvicorn.run(application, port=int(settings.PORT))
