# -*- coding: utf-8 -*-
"""
    t.api.jira
    ~~~~~~~~~~

    Jira API for t.
"""
import re

import requests

from .settings import get_settings


def is_jira_issue(message: str) -> bool:
    """
    Return True if message looks like it's a Jira issue.
    """
    return re.match(r'^[a-zA-Z]+-[0-9]+$', message) is not None


def get_jira_host() -> str:
    return get_settings()['jira']['host']


def get_jira_auth() -> tuple:
    return (
        get_settings()['jira']['user'],
        get_settings()['jira']['password'],
    )


def get_jira_projects() -> dict:
    return get_settings()['jira']['projects']


def jira(method, action, data=None):
    url = 'https://%s/rest/api/2/%s' % (get_jira_host(), action)
    auth = get_jira_auth()
    response = getattr(requests, method)(url, auth=auth, data=data)
    return response.json()


def fetch_jira_issue(issue_id: str) -> dict:
    return jira('get', 'issue/%s' % issue_id)


def fetch_jira_projects() -> dict:
    return jira('get', 'project')


def get_toggl_project_id(issue: dict) -> int:
    projects = get_jira_projects()
    jira_project_id = int(issue['fields']['project']['id'])
    return int(projects[jira_project_id])


def get_jira_issue(issue_id: str) -> str:
    issue = fetch_jira_issue(issue_id)
    issue_id = issue['key']
    message = issue['fields']['summary']
    project_id = get_toggl_project_id(issue)
    return project_id, '%s - %s' % (issue_id, message)
