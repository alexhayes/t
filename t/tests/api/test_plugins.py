# -*- coding: utf-8 -*-
"""
    t.test.api.test_plugins
    ~~~~~~~~~~~~~~~~~~~~~~~

    py.tests for t Jira integration.
"""
import pytest

from t.api.plugins import attach_cli_hook


def test_attach_cli_handles_no_projects(monkeypatch):
    monkeypatch.setattr('t.api.settings.SETTINGS', {})
    attach_cli_hook(None)


def test_attach_cli_handles_empty_projects(monkeypatch):
    monkeypatch.setattr('t.api.settings.SETTINGS', {'projects': {}})
    attach_cli_hook(None)


def test_attach_cli_can_import_dummy_plugin(monkeypatch):
    projects = {
        't.test.api.test_plugin': {}
    }
    monkeypatch.setattr('t.api.settings.SETTINGS', {'projects': projects})
    attach_cli_hook(None)
