<img src="./logo.png" alt="Logo ComChoice" width="350"/>


## What it is?

ComChoice is an open-source library to aggregate individual and collective preferences in Python. This library aims to convert the state-of-the-art in Social Choice Theory, Decision-Making Process and Pairwise Comparison Optimization into easy and intuitive functions to be used by programmers and researchers with basic programming knowledge.

ComChoice provides a module to run an API to aggregate preferences. This API can be used for digital democracy platforms.

## What we provide?

- Following up of state-of-the-art in voting rules studied in Computational Social Choice (e.g., complete preferences, participatory budgeting)
- Methods to test some axiomatic properties in Social Choice Theory.
- A framework to run digital democracy platforms, by providing an easy-to-use API.

## Getting Started

### Via pip

```
pip install comchoice
```

### From source code

To install ComChoice from source, you need to clone the project repository in your laptop.

```
git clone https://github.com/CenterForCollectiveLearning/comchoice.git
cd comchoice
python setup.py install

```

## Basic background

Before starting, you will frequently find the following concepts: alternative and voter. An *alternative* is the unit that we want to measure (its score), and the voter is the one who voted for alternatives. In general, the goal is to aggregate voters' individual preferences to elect a alternative. There are multiple voting methods (either absolute or relative judgments). For instance, we can consider reviewing a place in Google Maps as a voting mechanism because a user (voter) rates a place (alternative) on a scale of 1-5 stars (value).

## Hands on Coding

ComChoice classes require a `pandas.DataFrame` or a `list` of `dict` to be initialized.

### Hello world: Election data

For starting, let's use the data of an election of 22 voters and 4 alternatives. Then, voters provided their ranking of preferences.

```
import pandas as pd
from comchoice.aggregate import borda

data = [
    {"voters": 7, "ballot": "A>B>C>D"},
    {"voters": 5, "ballot": "B>C>D>A"},
    {"voters": 6, "ballot": "D>B>C>A"},
    {"voters": 4, "ballot": "C>D>A>B"}
]

df = pd.DataFrame(data)

borda(df)
```

Here, our goal is to calculate a ranking of alternatives by using Borda count.

| alternative | value | rank |
| --------- | ----- | ---- |
| B         | 41    | 1    |
| C         | 35    | 2    |
| D         | 31    | 3    |
| A         | 25    | 4    |

As shown in the table above, `borda` method includes alternatives' Borda score and their aggregate position.

Next, if you are interested in testing other rules using the same data, you just need to execute another function to the dataframe already defined. For instance, `condorcet` method calculates the Condorcet winner of an election.

```
from comchoice.aggregate import condorcet

condorcet(df, weak=True)
```

| alternative | value    |
| --------- | -------- |
| B         | 0.833333 |

In this example, B is a weak Condorcet winner because it is ranked above any other alternative in individual matches. Still, it does not beat all the alternatives.

### Pairwise Comparison

The dataset must include the voter, the alternatives compared, and the alternative selected to use methods defined in `Pairwise`.

Let's assume we have a CSV file of an experiment with three voters and three alternatives.

| voter | option_a | option_b | selected |
| ----- | -------- | -------- | -------- |
| 1     | A        | B        | A        |
| 1     | B        | C        | C        |
| 1     | A        | C        | C        |
| 2     | A        | C        | A        |
| 3     | B        | C        | B        |

```
import pandas as pd
from comchoice.pairwise import Pairwise

df = pd.read_csv("/path/to/file/pairwise.csv")

pwc = Pairwise(df)

pwc.copeland()
```

### Conversion Data into Pairwise comparison

`comchoice` allows converting an election dataset into pairwise comparison data through `to_pairwise()` method defined in the class `Pairwise`.

Let's suppose that we have two alternatives and two voters. Voter 1 rates alternative A with 5 stars, and rates alternative B with 3 stars. In this case, we could assume that voter 1 will choose alternative A over alternative B.

Original data:

| voter | alternative | rating |
| ----- | --------- | ------ |
| 1     | A         | 5      |
| 1     | B         | 3      |
| 2     | A         | 4      |
| 2     | B         | 5      |

Pairwise comparison data:

| voter | option_a | option_b | selected |
| ----- | -------- | -------- | -------- |
| 1     | A        | B        | A        |
| 2     | A        | B        | B        |

Here an example how would be the code:

```
pch = Pairwise(df)

pch.alternative = "alternative"
pch.voter = "voter"
pch.value = "rating"

pch.to_pairwise()
```

## Do you have any questions?

We invite you to create an issue in the project's GitHub repository (https://github.com/CenterForCollectiveLearning/comchoice/issues).

## About

`ComChoice` was developed by the research group in Digital Democracy of the [Center for Collective Learning](https://centerforcollectivelearning.org/).

## MIT License

Copyright 2022 Center For Collective Learning

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
