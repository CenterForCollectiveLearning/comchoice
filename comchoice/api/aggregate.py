import pandas as pd
from typing import Union

from fastapi import FastAPI
import comchoice.aggregate as agg

app = FastAPI()

fake_df = pd.DataFrame([
    {"voters": 7, "ballot": "A>B>C>D"},
    {"voters": 5, "ballot": "B>C>D>A"},
    {"voters": 6, "ballot": "D>B>C>A"},
    {"voters": 4, "ballot": "C>D>A>B"}
])


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/api/aggregate/{method}")
def aggregate_data(
    method: str,
    q: Union[str, None] = None
) -> dict:
    """API to aggregate preferences by using comchoice methods.

    Parameters
    ----------
    method : str
        Comchoice method.
    q : Union[str, None], optional
        Query, by default None

    Returns
    -------
    _type_
        _description_
    """
    valid_methods = ["borda", "condorcet", "copeland"]

    if method in valid_methods:
        return {
            "data": getattr(agg, method)(fake_df).to_dict(orient="records"),
            "q": q
        }

    return {
        "data": [],
        "message": "Aggregation method not valid. Pleasy try another option."
    }
