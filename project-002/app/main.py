from fastapi import FastAPI

myApp = FastAPI(
    title="Hello World API", 
    version="0.0.2",
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development Server"
        }
    ]
)

@myApp.get("/")
def read_root():
    return {"Hello": "World"}