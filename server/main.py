from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from src.configs import Base, engine
from src.routes import root_router, auth_router
from src.utils import error_res

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(root_router)
app.include_router(auth_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    first_error = exc.errors()[0]
    field = ".".join(str(x) for x in first_error["loc"] if x != "body")

    return error_res(f"{field} field is required", 422)
