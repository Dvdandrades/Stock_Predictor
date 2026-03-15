from fastapi import FastAPI

from stock_predictor.user import router as user_router
from stock_predictor.stock import router as stock_router
from stock_predictor.feedback import router as feedback_router

app = FastAPI()

app.include_router(user_router.router, prefix="/user", tags=["user"])
app.include_router(stock_router.router, prefix="/stock", tags=["stock"])
app.include_router(feedback_router.router, tags=["feedback"])
