#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import click
import requests
import subprocess


def toggl_key():
    return os.environ.get('TOGGL_KEY')


def toggl(method, action, data={}):
    url = 'https://www.toggl.com/api/v8/' + action
    f = getattr(requests, method.lower())
    response = f(url, json=data, auth=(toggl_key(), 'api_token'), headers={'content-type': 'application/json'})
    return response


@click.group()
def cli():
    pass


@cli.command()
def stop():
    response = toggl('get', 'time_entries/current').json()
    if 'data' in response and response['data']:
        toggl_id = response['data']['id']
        response = toggl('put', 'time_entries/{}/stop'.format(toggl_id))
        click.echo('Timer stopped.')
    else:
        click.echo('No timer running.')

@cli.command()
@click.argument('message', default='')
@click.option('--git', is_flag=True, help="Use the current git repo and branch name as the message")
def start(message, git):
    if git:
        repo, branch = subprocess.check_output(['git', 'rev-parse', '--show-toplevel', '--abbrev-ref', 'HEAD']).splitlines()
        message = '{} - {}'.format(repo.split(b'/')[-1].decode('utf-8'), branch.decode('utf-8'))

    response = toggl('post', 'time_entries/start', {
        'time_entry': {
            'description': message,
            'created_with': 't <https://github.com/sesh/t>',
        }
    })
    click.echo('Timer started.')


@cli.command('continue')
def cont():
    response = toggl('get', 'time_entries')
    latest_entry = sorted(response.json(), key=lambda x: x['start'], reverse=True)[0]
    message = latest_entry['description']
    response = toggl('post', 'time_entries/start', {
        'time_entry': {
            'description': message,
            'created_with': 't <https://github.com/sesh/t>',
        }
    })
    click.echo('Timer started: {}'.format(message))


if __name__ == '__main__':
    cli()
