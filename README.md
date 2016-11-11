_So I think this works. It works for me. But it's not really ready for primetime yet. Released some others can look / play._

## Installation

Install with pip:

```
pip3 install git@github.com:sesh/t.git
```


Or clone the repo and use pip to install:

```
git clone git@github.com:sesh/t.git
cd t
pip install .
```


## Usage

Make sure that you have exported your `TOGGL_KEY` into your environment.

```
export TOGGL_KEY='<your-api-key>'
```


Comes with three commands, `start`, `continue` and `stop`. Continue and stop are pretty straight forward.
Start let's you specify some options.

```
Usage: t start [OPTIONS] [MESSAGE]

Options:
  --git   Use the current git repo and branch name as the message
  --help  Show this message and exit.
```


