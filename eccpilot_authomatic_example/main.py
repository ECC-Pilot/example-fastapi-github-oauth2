from authomatic import Authomatic
from authomatic.adapters import FastAPIAdapter
from authomatic.providers import oauth2
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

import os
import uvicorn


CONFIG = {
    "github": {
        "class_": oauth2.GitHub,
        "consumer_key": "#####",
        "consumer_secret": "#####",
        "scope": ["user:email"],
    }
}

DEBUG = os.environ.get("ARGO_FASTAPI_DEBUG", "0") == "1"

authomatic = Authomatic(config=CONFIG, secret="YOUR SUPER CONFIDENTIAL SECRET")
app = FastAPI(debug=DEBUG)


@app.get("/")
async def home():
    return "Welcome to ECC-Pilot!"


@app.api_route("/login/{provider}", methods=["GET", "POST"])
async def login(request: Request, provider: str):
    """
    There's much repetitive code, but it's just a demonstration.
    """
    response = JSONResponse(content={})
    result = authomatic.login(FastAPIAdapter(request, response), provider)

    if not result:
        return {"error": "No result!"}
    if result.error:
        return {"error": result.error.message}

    if not result.user:
        return {"warning": "No user in result!"}
    if not (result.user.name and result.user.id):
        result.user.update()

    user = result.user
    provider = result.provider

    if user:
        if provider.name == "github":
            response = JSONResponse(
                content={"message": "You're now logged in with GitHub."}
            )

            provider_response = provider.access(
                user.credentials,
                "https://api.github.com/user",
                {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                    " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
                },
            )

            if provider_response.status == 200:
                response.body += "Hello {}".format(provider_response.data.name).encode(
                    "utf-8"
                )

    return response


def start():
    uvicorn.run(app, host="0.0.0.0", port=8000)
