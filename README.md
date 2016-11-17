_So I think this works. It works for me. But it's not really ready for primetime yet. Released some others can look / play._

We're using this for helping us track our time at [Common Code](http://commoncode.io).

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


## Plugins

t comes with a basic plugin system that allows a plugin writer to hook into the
basic usage of t.

### Jira Plugin

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
plugins:
    t.plugins.jira:
      - name: "Example 1"
        host: example1.atlassian.net
        user: john
        password: s3cr3t
        projects:
          DF: 54321
          CD: 98765
    
      - name: "Example 2"
        host: example2.atlassian.net
        user: john
        password: sm1th
        projects:
          YZ: 4321
```

`projects` is a mapping of Jira project identifiers to Toggl project ids.

To ease the burden of creating these mappings there are several sub-commands 
available;

- `t jira project list` - list all available Jira projects
- `t toggl workspace list` - list all available Toggl workspaces
- `t toggl project list 123` - list all available Toggl projects for a workspace
- `t jira project map 12345 54321` - map Jira project `12345` to Toggl project `54321`

You can also define a custom message rather than using the summary from Jira,
like so;

```bash
t start df-123 "Custom description for time entry"
```

### Writing a plugin

Creating a plugin is easy, you just need to point to a module in your settings
file that contains either a `cli_hook` or `toggl_request_hook` function.

#### `cli_hook(cli, settings)`

If defined, your `cli_hook` function should accept a `cli` and `settings` attributes.

- `cli`: Is the [click](http://click.pocoo.org/5/) root group upon which you can
  attach groups/commands to. This allows you to add your own custom commands.
- `settings`: Is a dict of settings as defined in the settings file for this
  plugin.
  
#### `toggl_request_hook(action, data, settings)`

If defined, your `toggl_request_hook` function can hook into the data that is
sent to the Toggl API.

- `action`: Is either `t.consts.ACTION_START` or `t.consts.ACTION_CONTINUE`
- `data`: Is the data attribute that will be supplied to requests.
- `settings`: Is a dict of settings as defined in the settings file for this
  plugin. 


## Authors

- [Brenton Cleeland](https://github.com/sesh)
- [Alex Hayes](https://github.com/alexhayes)
