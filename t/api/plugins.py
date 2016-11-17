# -*- coding: utf-8 -*-
"""
    t.api.plugins
    ~~~~~~~~~~~~~

    Utilities for t's plugin system
"""

from importlib import import_module

from t.api.settings import get_settings


def import_path(path):
    """
    Dynamically import a path.

    :type path: str
    """
    parts = path.split('.')
    module = import_module('.'.join(parts[:-1]))
    try:
        return getattr(module, parts[-1:][0])
    except AttributeError:
        raise ImportError("Could not import path '{}'".format(path))


def attach_cli_hook(cli):
    """
    Attach each plugin to the cli.
    """
    settings = get_settings()

    try:
        plugins = settings['plugins']
    except KeyError:
        pass
    else:
        for plugin_module, plugin_settings in plugins.items():
            # Ensure the plugin module can be imported
            import_module(plugin_module)

            try:
                cli_hook = import_path('{}.cli_hook'.format(plugin_module))
            except ImportError:
                # The plugin module exists, but it doesn't have a cli_hook (which is OK)
                pass
            else:
                cli_hook(cli=cli, settings=plugin_settings)


def attach_toggl_request_hook(action: str, data: dict):
    """
    Attach each plugin to the toggl request so that it can augment the request.
    """
    settings = get_settings()

    try:
        plugins = settings['plugins']
    except KeyError:
        pass
    else:
        for plugin_module, plugin_settings in plugins.items():
            # Ensure the plugin module can be imported
            import_module(plugin_module)

            try:
                toggl_request_hook = import_path('{}.toggl_request_hook'.format(plugin_module))
            except ImportError:
                # The plugin module exists, but it doesn't have a cli_hook (which is OK)
                pass
            else:
                data = toggl_request_hook(action=action, data=data, settings=plugin_settings)

    return data

