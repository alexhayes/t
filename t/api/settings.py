# -*- coding: utf-8 -*-
"""
    t.api.settings
    ~~~~~~~~~~~~~~

    t settings API.
"""
import os

import yaml


SETTINGS = None


def load_settings():
    global SETTINGS
    SETTINGS = open_settings()


def get_settings_path():
    return os.environ.get('T_SETTINGS_FILE')


def open_settings():
    with open(get_settings_path()) as f:
        return yaml.load(f.read())


def get_settings():
    return SETTINGS


def write_settings(settings):
    with open(get_settings_path(), 'w') as f:
        yaml.dump(settings, f)
