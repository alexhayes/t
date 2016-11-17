# -*- coding: utf-8 -*-
"""
    t.api.jira
    ~~~~~~~~~~

    Jira API for t.
"""
import re
from typing import Union

import click
import requests

from t.api.consts import ACTION_START
from t.api.errors import UnrecoverableError
from t.api.settings import get_settings, write_settings


class NoJiraProjectError(UnrecoverableError):
    """
    Raised when no Jira project has been defined in the Jira settings.
    """
    pass


def toggl_request_hook(action: str, data: dict, settings: dict) -> dict:
    """

    :param data: A dict of data that represents the payload that will be sent to toggl.
    :param settings: A dict of settings as defined in YAML.
    """
    if action != ACTION_START:
        return

    description = data['time_entry']['description']

    regex = (
        r"""^
        ([a-zA-Z]{1,5})-([0-9]+)  # Jira issue number
        \s?\-?                    # Possible space and dash
        (.*)                      # Custom message
        $"""
    )

    match = re.findall(regex, description, re.IGNORECASE | re.VERBOSE)

    if not match:
        # It's perfectly valid to not have a Jira issue number in a description
        return data

    jira_project = match[0][0].upper()
    jira_issue = '{}-{}'.format(*match[0][:2]).upper()
    description = match[0][2].strip()
    if len(description) == 0:
        description = None

    toggl_project_id = None

    for jira_instance in settings:
        try:
            projects = jira_instance['projects']
        except KeyError:
            pass
        else:
            if jira_project in projects.keys():
                toggl_project_id = projects[jira_project]
                host = jira_instance['host']
                auth = (jira_instance['user'], jira_instance['password'])
                break

    if toggl_project_id is None:
        raise NoJiraProjectError("No Jira project identifier '{}' in settings.".format(jira_project))

    if description is None:
        # Fetch description from Jira
        description = fetch_jira_issue(host, auth, jira_issue)['fields']['summary']

    data['time_entry']['description'] = '{} - {}'.format(jira_issue, description)
    data['time_entry']['pid'] = toggl_project_id

    return data


def cli_hook(cli, settings):
    """
    Allows the plugin to add/modify the cli.
    """
    @cli.group()
    def jira():
        pass

    @jira.group('project')
    def jira_project():
        pass

    @jira_project.command('list')
    def jira_project_list():
        """
        List Jira projects broken down by instance (as defined in settings).
        """
        for jira_instance in settings:
            try:
                name = jira_instance['name']
                user = jira_instance['user']
                password = jira_instance['password']
                host = jira_instance['host']
            except KeyError:
                raise UnrecoverableError(
                    "Jira instance '{}' must have name, user, password and host set.".format(jira_instance)
                )
            else:
                print('{} - {} ({})'.format(name, host, user))
                for project in fetch_jira_projects(host, (user, password)):
                    print('  {id: <16}{name}'.format(**project))


def request(host: str, auth: tuple, method: str, endpoint: str, data: dict=None) -> Union[list, dict]:
    url = 'https://%s/rest/api/2/%s' % (host, endpoint)
    response = getattr(requests, method)(url, auth=auth, data=data)
    return response.json()


def fetch_jira_issue(host: str, auth: tuple, issue_id: str) -> dict:
    return request(host, auth, 'get', 'issue/%s' % issue_id)


def fetch_jira_projects(host: str, auth: tuple) -> dict:
    return request(host, auth, 'get', 'project')

