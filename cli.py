#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from pprint import pprint

import click
from click.exceptions import ClickException

from t.api.jira import is_jira_issue, get_jira_issue, fetch_jira_projects
from t.api.settings import load_settings, get_settings, write_settings
from t.api.toggl import timer_continue, timer_start, fetch_toggl_projects, timer_stop, fetch_toggl_workspaces, toggl_key


@click.group()
def cli():
    try:
        load_settings()
    except FileNotFoundError:
        try:
            if toggl_key():
                # They must have set the TOGGL_KEY env var, that's OK... (no Jira mode)
                pass
        except TypeError:
            raise ClickException('You must set env var TOGGL_KEY or T_SETTINGS_FILE.')


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
@click.argument('message', default='')
@click.option('--git', is_flag=True, help="Use the current git repo and branch name as the message")
@click.option('--nojira', is_flag=True, help="Do not fetch details from Jira")
def start(message: str, git: bool, nojira: bool):
    """
    Start a timer.

    :param message: Message to use when starting the timer. If it looks like a Jira ticket number (ie.. BT-123) and
                    you've setup Jira,
    """
    if git:
        repo, branch = subprocess.check_output(['git', 'rev-parse', '--show-toplevel', '--abbrev-ref', 'HEAD']).splitlines()
        message = '{} - {}'.format(repo.split(b'/')[-1].decode('utf-8'), branch.decode('utf-8'))

    # If it looks like a Jira ticket, attempt to get details of it
    if not nojira and is_jira_issue(message):
        project_id, message = get_jira_issue(message)
    else:
        project_id = None

    timer_start(message, project_id)
    click.echo('Timer started: %s' % message)


@cli.command('continue')
def cont():
    message = timer_continue()
    click.echo('Timer started: {}'.format(message))


@cli.group()
def jira():
    pass


@jira.group('project')
def jira_project():
    pass


@jira_project.command('list')
def jira_project_list():
    for project in fetch_jira_projects():
        print('{id: <16}{name}'.format(**project))


@jira_project.command('map')
@click.argument('jira-project-id', type=int)
@click.argument('toggl-project-id', type=int)
def jira_project_map(jira_project_id: int, toggl_project_id: int):
    """
    Map a Jira project to a Toggl project and write to YAML config file.
    """
    settings = get_settings()

    if 'jira' not in settings:
        settings['jira'] = {
            'host': '',
            'user': '',
            'password': '',
            'projects': {}
        }
    if 'projects' not in settings['jira']:
        settings['jira']['projects'] = {}

    settings['jira']['projects'][jira_project_id] = toggl_project_id

    write_settings(settings)


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


if __name__ == '__main__':
    cli()
