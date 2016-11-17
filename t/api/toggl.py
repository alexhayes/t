# -*- coding: utf-8 -*-
"""
    t.api.toggl
    ~~~~~~~~~~~

    Toggl API for t.
"""
import os

import requests

from t.api.consts import ACTION_START, ACTION_CONTINUE
from t.api.errors import UnrecoverableError
from t.api.plugins import attach_toggl_request_hook
from .settings import get_settings


def toggl_key():
    return os.environ.get('TOGGL_KEY', get_settings()['toggl_key'])


def toggl(method, endpoint, data={}):
    url = 'https://www.toggl.com/api/v8/' + endpoint
    f = getattr(requests, method.lower())
    response = f(url, json=data, auth=(toggl_key(), 'api_token'), headers={'content-type': 'application/json'})

    if response.status_code < 400:
        return response
    else:
        raise UnrecoverableError("Error requesting Toggl API: {} {} - {}".format(
            response.status_code,
            response.reason,
            response.text
        ))


def timer_start(message) -> str:
    data = {
        'time_entry': {
            'description': message,
            'created_with': 't <https://github.com/sesh/t>',
        }
    }

    data = attach_toggl_request_hook(ACTION_START, data)

    toggl('post', 'time_entries/start', data)

    return data['time_entry']['description']


def timer_stop() -> bool:
    """
    Attempts to stop the running timer.

    :return: True if the timer was running, False if no timer is running.
    """
    response = toggl('get', 'time_entries/current').json()
    if 'data' in response and response['data']:
        toggl_id = response['data']['id']
        toggl('put', 'time_entries/{}/stop'.format(toggl_id))
        return True
    else:
        return False


def timer_continue() -> str:
    response = toggl('get', 'time_entries')
    latest_entry = sorted(response.json(), key=lambda x: x['start'], reverse=True)[0]
    message = latest_entry['description']
    project_id = latest_entry['pid']
    data = {
        'time_entry': {
            'description': message,
            'pid': project_id,
            'created_with': 't <https://github.com/sesh/t>',
        }
    }
    data = attach_toggl_request_hook(ACTION_CONTINUE, data)
    toggl('post', 'time_entries/start', data)

    return data['time_entry']['description']


def fetch_toggl_workspaces():
    response = toggl('get', 'workspaces')
    return response.json()


def fetch_toggl_projects(workspace_id):
    response = toggl('get', 'workspaces/%s/projects' % workspace_id)
    return response.json()
