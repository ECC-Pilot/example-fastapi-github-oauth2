# example-fastapi-github-oauth2

Example to use FastAPI with Authomatic (OAuth2) and add Authorization for this Github organization.

## install

Precondition: Python 3.11

Then run Make - it creates a `venv`, no worries:

```bash
make install
```

## start server

```bash
./venv/bin/eccpilot_authomatic_example
```

For debugging/developing:

```bash
ECCPILOT_DEBUG=1 ./venv/bin/uvicorn --host 0.0.0.0 eccpilot_authomatic_example.main:app --reload
```

## check if it works

In the browser of the machine running the service, go to [http://local.kleinundpartner.at:8000/login/github](http://local.kleinundpartner.at:8000/login/github) (the domain points to localhost).

You are redirected to Github. Accepts there and then you get a message if you are logged in or not allowed (if you are not in this ECC-Pilot organization).
