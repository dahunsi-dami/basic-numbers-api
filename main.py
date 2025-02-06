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
import httpx
import math


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())


def optimus_prime(n: int) -> bool:
    """ I'll tell if a number is a prime, dear sentient being. """
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def yuh_perfect(n: int) -> bool:
    """ Mi a go tell yuh if yuh number perfect, undastan? """
    if n < 2:
        return False
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n


def is_armstrong(n: int) -> bool:
    """ I'll tell if your number is an Armstrong number. """
    digits = [int(d) for d in str(n)]
    num_digits = len(digits)
    return sum(d**num_digits for d in digits) == n


def digit_sum(n: int) -> int:
    """ I'll solve the sum of digits of a number. """
    return sum(int(d) for d in str(n))


@cache(expire=3600)
async def blab_fun_fact(n: int) -> str:
    """
    I'll read you a fun fact about any number-
    -from the Numbers API book.
    """
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
    ...,
    description="The number to classify"
)):
    try:
        if not number.lstrip('-').isdigit():
            raise ValueError("Invalid input. Provide valid integer.")

        number_int = int(number)

        properties = []
        if optimus_prime(number_int):
            properties.append("prime")
        if yuh_perfect(number_int):
            properties.append("perfect")
        if is_armstrong(number_int):
            properties.append("armstrong")
        if number_int % 2 != 0:
            properties.append("odd")
        else:
            properties.append("even")

        fun_fact = await blab_fun_fact(number_int)

        response = {
            "number": number_int,
            "is_prime": optimus_prime(number_int),
            "is_perfect": yuh_perfect(number_int),
            "properties": properties,
            "digit_sum": digit_sum(number_int),
            "fun_fact": fun_fact,
        }
        return response

    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "number": number,
                "error": True
            }
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
