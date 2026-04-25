from fastapi.responses import JSONResponse


def success_res(message: str, status_code: int = 200, **kwargs):
    return JSONResponse(
        status_code=status_code,
        content={"success": True, "message": message, **kwargs},
    )


def error_res(err: str, status_code: int):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": err,
        },
    )
