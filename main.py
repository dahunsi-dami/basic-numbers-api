#!/bin/env/python3
"""
I'll be your weird autistic friend who can blab fun facts and
math properties about numbers all day. :)
"""

from fastapi import FastAPI, Query, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import httpx
import math


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "number": "alphabet",
            "error": True
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "number": "alphabet",
            "error": True
        }
    )


@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())


def optimus_prime(n: int) -> bool:
    """ I'll tell if a number is a prime, dear sentient being. """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    for i in range(5, int(math.isqrt(n)) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True


def yuh_perfect(n: int) -> bool:
    """ Mi a go tell yuh if yuh number perfect, undastan? """
    if n < 2:
        return False
    divisors = [1]
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    return sum(divisors) == n


def is_armstrong(n: int) -> bool:
    """ I'll tell if your number is an Armstrong number. """
    if n < 0:
        return False
    digits = [int(d) for d in str(abs(n))]
    num_digits = len(digits)
    return sum(d**num_digits for d in digits) == n


def digit_sum(n: int) -> int:
    """ I'll solve the sum of digits of a number. """
    return sum(int(d) for d in str(abs(n)))


@cache(expire=3600)
async def blab_fun_fact(n: int) -> str:
    """
    I'll read you a fun fact about any number-
    -from the Numbers API book.
    """
    # print("n value is: ", n)
    url = f"http://numbersapi.com/{n}/math?json"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("text", "No fun fact available.")
    return "No fun fact available."


@app.get("/api/classify-number")
@cache(expire=3600)
async def classify_number(number: str = Query(
    default=None,
    description="The number to classify"
)):
    if number is None or number == "":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": True}
        )
    try:
        if not number or number == '-':
            raise ValueError("Invalid input. Give a valid integer.")

        if not (number.startswith('-') and number[1:].isdigit() or number.isdigit()):
            raise ValueError("Invalid input. Give a valid integer.")

        number_int = int(number)

        properties = []
        if optimus_prime(abs(number_int)):
            properties.append("prime")
        if yuh_perfect(abs(number_int)):
            properties.append("perfect")
        if is_armstrong(number_int):
            properties.append("armstrong")
        if number_int % 2 != 0:
            properties.append("odd")
        else:
            properties.append("even")

        # print("number to API is: ", number_int)
        fun_fact = await blab_fun_fact(number_int)

        response = {
            "number": number_int,
            "is_prime": optimus_prime(abs(number_int)),
            "is_perfect": yuh_perfect(abs(number_int)),
            "properties": properties,
            "digit_sum": digit_sum(number_int),
            "fun_fact": fun_fact,
        }
        return response

    except Exception as e:
        # print("Error is: ", e)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "number": "alphabet",
                "error": True
            }
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
