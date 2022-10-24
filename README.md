<img src="./logo.png" alt="Logo ComChoice" width="350"/>

## What it is?

ComChoice is an open-source library to aggregate individual and collective preferences in Python. This library aims to convert the state-of-the-art in Social Choice Theory, Decision-Making Process and Pairwise Comparison Optimization into easy and intuitive functions to be used by programmers and researchers with basic programming knowledge.

ComChoice provides a module to run an API to aggregate preferences. This API can be used for digital democracy platforms.

## What we provide?

- Algorithmic implementation in Python and DataFrame objects of most of the state-of-the-art in voting rules studied in Computational Social Choice (e.g., complete preferences, participatory budgeting).
- Methods to test some axiomatic properties in Social Choice Theory.
- A robust framework to run digital democracy platforms' backends, by providing an easy-to-use API developed in FastAPI.

## Getting Started

### Via pip

```
pip install comchoice
```

### From source code

To install `comchoice` from the source, you need first to clone the project repository as follows:

```
git clone https://github.com/CenterForCollectiveLearning/comchoice.git
cd comchoice
python setup.py install

```

## Basic Background

The function parameters in this library follow, in most cases, the terminology adopted by the COMSOC community. Nonetheless, some functions includes specific parameters called by their notation in the literature.

Let $A$ a set of $n$ alternatives, such that $A = \{a_1, a_2, a_3, ..., a_n\}$. A **ballot** represents an input of preferences of a **voter** or **voters** over a set of **candidates** (either an ordered set of preferences or approved ones)\footnote{In the COMSOC literature, we find references of voters as agents, and candidates as alternatives.}. The preferences are separated by a **delimiter**, that by default is represented by $>$. In case of approval ballots, the default delimiter is the comma ($,$). For example, a ballot ($B$) for a voter is $B = \{a>b>c\}$. This ballot means that the voter prefers $a$ over $b$, $b$ over $c$, and $a$ over $c$.

In general, voting methods present two outputs: a winner or a ranking of preferences. We call _winner rule_ those that returns a winner (or group of them) of an election; whereas we refer to _voting rule_ those that returns a score for each alternative. It should be noted that a _voting rule_ can be interpreted as a _winner rule_, since the top-scored alternative is considered the winner. This option is included in the library by a parameter defined in the functions of _voting rules_.

## Hands on Coding

### Hello world: Synthethic data

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
| ----------- | ----- | ---- |
| B           | 41    | 1    |
| C           | 35    | 2    |
| D           | 31    | 3    |
| A           | 25    | 4    |

As shown in the table above, `borda` method includes alternatives' Borda score and their aggregate position.

Next, if you are interested in testing other rules using the same data, you just need to execute another function to the dataframe already defined. For instance, `condorcet` method calculates the Condorcet winner of an election.

```
from comchoice.aggregate import condorcet

condorcet(df, weak=True)
```

| alternative | value    |
| ----------- | -------- |
| B           | 0.833333 |

In this example, B is a weak Condorcet winner because it is ranked above any other alternative in individual matches. Still, it does not beat all the alternatives.

### Manage Pairwise Comparison data

#### Convert Star-rated dataset to Pairwise Comparison

`comchoice` allows converting an dataset into pairwise comparison data through `to_pairwise()` method defined in the subpackage `preprocessing`.

Let's suppose that we have two alternatives and two voters. Voter 1 rates alternative A with 5 stars, and rates alternative B with 3 stars. In this case, we could assume that voter 1 will choose alternative A over alternative B.

**Our data**:

| voter | alternative | rating |
| ----- | ----------- | ------ |
| 1     | A           | 5      |
| 1     | B           | 3      |
| 2     | A           | 4      |
| 2     | B           | 5      |

**Pairwise comparison data**:

| voter | option_a | option_b | selected |
| ----- | -------- | -------- | -------- |
| 1     | A        | B        | A        |
| 2     | A        | B        | B        |

Here an example how would be the code:

```
df = pd.DataFrame([
    (1, A, 5),
    (1, B, 3),
    (2, A, 4),
    (2, B, 5)
], columns=["voter", "alternative", "rating"])

df_pw = to_pairwise(
    df,
    value="rating"
)
```

#### Calculating metrics

Then, let's calculate some metrics using the pairwise comparison data set.

```
bradley_terry(df_pw)
```

## About

`ComChoice` was developed by the research group in Digital Democracy at the [Center for Collective Learning](https://centerforcollectivelearning.org/), Université de Toulouse.

## GPL-3 License

The `ComChoice` library is distributed under General Public License (GPL), version 3. More details [here](LICENSE.md).

## Do you have any questions?

We invite you to create an issue in the project's GitHub repository (https://github.com/CenterForCollectiveLearning/comchoice/issues).
