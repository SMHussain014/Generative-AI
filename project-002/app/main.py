from fastapi import FastAPI

myApp = FastAPI(
    title="Hello World API", 
    version="0.0.1",
    servers=[
        {
            "url": "http://Localhost:8000",
            "description": "Development Server"
        }
    ]
)

@myApp.get("/")
def read_root():
    return {"Hello": "World"}