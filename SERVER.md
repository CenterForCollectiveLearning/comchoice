## Server

```
pip install "uvicorn[standard]"
```

```
python -m uvicorn aggregate:app --reload
python -m uvicorn aggregate:app --reload --app-dir="$(pwd)/comchoice/api"
```