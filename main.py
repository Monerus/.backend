from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from api.repositories.user_repository import router as user_router
from api.repositories.message_repository import router as messages_router
from api.repositories.post_repository import router as post_router
from api.repositories.comment_repository import router as comment_router
from api.repositories.vote_repository import router as vote_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(messages_router)
app.include_router(post_router)
app.include_router(comment_router)
app.include_router(vote_router)



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)