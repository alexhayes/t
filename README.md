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

## Jira Integration

You can automatically set the message to a Jira ticket number followed by the 
summary of the Jira ticket, for example;

```
t start df-435
```

Would fetch ticket `DF-435` from Jira and;

- Set the message to: `DF-435 - Summary of Jira ticket`
- Set the Toggl project

To do this you need to create a YAML file and export `T_SETTINGS_FILE` into your 
environment.

```
export T_SETTINGS_FILE='/path/to/t.yaml'
```

Your `t.yaml` file should be in the following structure;

```yaml
toggl_key: <your-api-key>
jira:
  host: example.atlassian.net
  user: john
  password: s3cr3t
  projects:
    12345: 54321
    56789: 98765
```

The setting `jira -> projects` is a mapping of Jira project ids to Toggl project 
ids.

To ease the burden of creating these mappings there are several sub-commands 
available;

- `t jira project list` - list all available Jira projects
- `t toggl workspace list` - list all available Toggl workspaces
- `t toggl project list 123` - list all available Toggl projects for a workspace
- `t jira project map 12345 54321` - map Jira project `12345` to Toggl project `54321`


