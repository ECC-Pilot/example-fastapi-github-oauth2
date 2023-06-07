from authomatic import Authomatic
from authomatic.adapters import FastAPIAdapter
from authomatic.providers import oauth2
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

import os
import uvicorn


ALLOWED_ORGA = "ECC-Pilot"

CONFIG = {
    "github": {
        "class_": oauth2.GitHub,
        "consumer_key": "2b196df3bec16f2b39db",
        "consumer_secret": "c59f1120159fcd7017144918cfd2921ff37d41a5",
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
    example usage
    """
    response = JSONResponse(content="")
    result = authomatic.login(FastAPIAdapter(request, response), provider)

    if not result:
        return response
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
            userdata_response = provider.access(
                "https://api.github.com/user",
                headers={"User-Agent": "Authomatic (ECC Pilot 1.0)"},
            )
            if userdata_response.status != 200:
                return JSONResponse(
                    content={"error": "Can not fetch userdata from GitHub."}
                )

            orga_data_response = provider.access(
                userdata_response.data["organizations_url"],
                headers={"User-Agent": "Authomatic (ECC Pilot 1.0)"},
            )
            if orga_data_response.status != 200:
                return JSONResponse(
                    content={
                        "error": "Can not fetch your organizations data from GitHub."
                    }
                )
            if not [
                orga
                for orga in orga_data_response.data
                if orga["login"] == ALLOWED_ORGA
            ]:
                return JSONResponse(
                    content={"error": "You're not allowed to use ECC Pilot."}
                )
            response = JSONResponse(
                content={
                    "message": f"You're now logged in with GitHub as {userdata_response.data['name']}."
                }
            )

    return response


def start():
    uvicorn.run(app, host="0.0.0.0", port=8000)
