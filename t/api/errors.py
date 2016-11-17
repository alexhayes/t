# -*- coding: utf-8 -*-
"""
    t.api.errors
    ~~~~~~~~~~~~

    Defines errors that can be raised by t or it's plugins.
"""
from click.exceptions import ClickException


class UnrecoverableError(ClickException):
    pass
