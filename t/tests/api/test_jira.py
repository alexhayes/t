# -*- coding: utf-8 -*-
"""
    t.test.api.test_jira
    ~~~~~~~~~~~~~~~~~~~~

    py.tests for t Jira integration.
"""
import pytest
import requests_mock

from ...api.jira import is_jira_issue, get_jira_issue, get_jira_projects


@pytest.mark.parametrize('input, expected', [
    ('BT-123', True),
    ('ST-1', True),
    ('MAR-454', True),
    ('Foo bar', False),
])
def test_is_jira_issue(input, expected):
    assert is_jira_issue(input) is expected


SETTINGS = {
    'jira': {
        'host': 'example.atlassian.net',
        'user': 'user',
        'password': 'password',
        'projects': {
            3765272: 1234,
            3762: 121,
        }
    }
}


def test_get_jira_issue(monkeypatch):
    monkeypatch.setattr('t.api.settings.SETTINGS', SETTINGS)
    with requests_mock.Mocker() as m:
        m.get(
            'https://example.atlassian.net/rest/api/2/issue/t-123',
            json=dict(
                key='T-123',
                fields=dict(
                    summary='A dummy ticket',
                    project=dict(
                        id=3762
                    )
                )
            )
        )

        actual = get_jira_issue('t-123')
        expected = (121, 'T-123 - A dummy ticket')

        assert actual == expected


def test_get_toggl_projects(monkeypatch):
    monkeypatch.setattr('t.api.settings.SETTINGS', SETTINGS)
    actual = get_jira_projects()
    expected = {
        3765272: 1234,
        3762: 121,
    }

    assert actual == expected
