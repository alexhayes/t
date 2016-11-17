#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from pprint import pprint

import click
from click.exceptions import ClickException

from t.api.plugins import attach_cli_hook
from t.api.settings import load_settings, get_settings, write_settings
from t.api.toggl import timer_continue, timer_start, fetch_toggl_projects, timer_stop, fetch_toggl_workspaces, toggl_key


@click.group()
def cli():
    pass


@cli.command()
def stop():
    """
    Stop the currently running timer.
    """
    if timer_stop():
        click.echo('Timer stopped.')
    else:
        click.echo('No timer running.')


@cli.command()
@click.argument('issue', default='')
@click.argument('description', default=None, required=False)
@click.option('--git', is_flag=True, help="Use the current git repo and branch name as the description")
def start(issue: str, description: str, git: bool):
    """
    Start a timer.

    :param description: Message to use when starting the timer. If it looks like a Jira ticket number (ie.. BT-123) and
                    you've setup Jira,
    """
    message = issue

    if git:
        repo, branch = subprocess.check_output(['git', 'rev-parse', '--show-toplevel', '--abbrev-ref', 'HEAD']).splitlines()
        message = '{} - {}'.format(repo.split(b'/')[-1].decode('utf-8'), branch.decode('utf-8'))

    if description:
        message += ' - {}'.format(description)

    message = timer_start(message)

    click.echo('Timer started: %s' % message)


@cli.command('continue')
def cont():
    message = timer_continue()
    click.echo('Timer started: {}'.format(message))


@cli.group()
def toggl():
    pass


@toggl.group('workspace')
def toggl_workspace():
    """
    Toggl has workspaces?!
    """
    pass


@toggl_workspace.command('list')
def toggl_workspace_list():
    for workspace in fetch_toggl_workspaces():
        click.echo('{id: <16}{name}'.format(**workspace))


@toggl.group('project')
def toggl_project():
    """
    Toggl has projects!
    """
    pass


@toggl_project.command('list')
@click.argument('workspace-id')
def toggl_project_list(workspace_id):
    for project in fetch_toggl_projects(workspace_id):
        click.echo('{id: <16}{name}'.format(**project))


@cli.group('settings')
def settings():
    pass


@settings.command('show')
def settings_show():
    pprint(get_settings())


def main():
    try:
        load_settings()
    except FileNotFoundError:
        try:
            if toggl_key():
                # They must have set the TOGGL_KEY env var, that's OK... (no Jira mode)
                pass
        except TypeError:
            raise ClickException('You must set env var TOGGL_KEY or T_SETTINGS_FILE.')

    attach_cli_hook(cli)
    cli()


if __name__ == '__main__':
    main()
