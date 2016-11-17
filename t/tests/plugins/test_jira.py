# -*- coding: utf-8 -*-
"""
    t.test.api.test_jira
    ~~~~~~~~~~~~~~~~~~~~

    py.tests for t Jira integration.
"""
import pytest
import requests_mock

from t.api.consts import ACTION_START
from t.plugins.jira import toggl_request_hook, NoJiraProjectError

SETTINGS = [
    {
        'name': 'Example 1',
        'host': 'example1.atlassian.net',
        'user': 'john',
        'password': 't0ps3cr3t',
        'projects': {
            'A': 1,
            'BT': 2,
        }
    },
    {
        'name': 'Example 2',
        'host': 'example2.atlassian.net',
        'user': 'john.doe',
        'password': 's3cr3t',
        'projects': {
            'ST': 3,
            'MAR': 3,
        }
    },
]


@pytest.mark.parametrize('input, expected', [
    ('A-1 - Hello world', {'description': 'A-1 - Hello world', 'pid': 1}),
    ('BT-123 - Universe', {'description': 'BT-123 - Universe', 'pid': 2}),
])
def test_toggl_request_hook_with_custom_description(input, expected):
    data = {
        'time_entry': {
            'description': input
        }
    }
    actual = toggl_request_hook(ACTION_START, data, SETTINGS)
    assert actual['time_entry'] == expected


@pytest.mark.parametrize('input, host, expected', [
    ('A-1', SETTINGS[0]['host'], {'description': 'A-1 - Jira summary', 'pid': 1}),
    ('BT-123', SETTINGS[0]['host'], {'description': 'BT-123 - Jira summary', 'pid': 2}),
    ('ST-546', SETTINGS[1]['host'], {'description': 'ST-546 - Jira summary', 'pid': 3}),
    # Case insensitive
    ('mar-546', SETTINGS[1]['host'], {'description': 'MAR-546 - Jira summary', 'pid': 3}),
])
def test_toggl_request_hook_no_description(input, host, expected):
    with requests_mock.Mocker() as m:
        m.get(
            'https://{}/rest/api/2/issue/{}'.format(host, input),
            json={
                'fields': {
                    'summary': 'Jira summary'
                }
            }
        )
        data = {
            'time_entry': {
                'description': input
            }
        }
        actual = toggl_request_hook(ACTION_START, data, SETTINGS)
        assert actual['time_entry'] == expected


def test_toggl_request_hook_raises():
    with pytest.raises(NoJiraProjectError):
        data = {
            'time_entry': {
                'description': 'UK-123'
            }
        }
        toggl_request_hook(ACTION_START, data, SETTINGS)
