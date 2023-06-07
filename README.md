# example-fastapi-github-oauth2

Example to use FastAPI with Authomatic (OAuth2) and add Authorization for this Github organization.

## start server

```bash
./venv/bin/eccpilot_authomatic_example
```

For debugging/developing:

```bash
ECCPILOT_DEBUG=1 ./venv/bin/uvicorn --host 0.0.0.0 eccpilot_authomatic_example.main:app --reload
```
