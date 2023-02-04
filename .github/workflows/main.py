import os
import json
import requests


def load_data():
    data = os.environ.get('github')
    if data is not None:
        return json.loads(data)


def get_channel_ids(user_ids, token):
    channels = []
    for user_id in user_ids:
        channels.append(
            requests.post(
                "https://discordapp.com/api/v6/users/@me/channels",
                headers={'authorization': f'Bot {token}'},
                json={'recipient_id': user_id},
            ).json()['id']
        )
    return channels


data = load_data()
with open('./config.json', 'r') as file:
    config = json.load(file)
target = config.get('target')
mode = config.get('mode')
embed = {}

EVENT_NAME = data.get('event_name')
REPOSITORY = data.get('repository')
event = data.get('event')

if EVENT_NAME == 'push':
    REF_NAME = data.get('ref_name')
    push_target = target.get('push', [])
    if push_target == [] or REF_NAME in push_target:
        PUSHER = event.get('pusher').get('name')
        head_commit = event.get('head_commit')
        # HEAD_AUTHOR = head_commit.get('author').get('username')
        # HEAD_COMMITTER = head_commit.get('committer').get('username')
        # HEAD_MESSAGE = head_commit.get('message')

        commits = event.get('commits')
        COMMIT_COUNT = len(commits)
        fields = [{'name': commit.get('message'), 'value': ''} for commit in commits]
        # author = commit.get('author').get('username')
        # committer = commit.get('committer').get('username')

        embed['title'] = f'[ PUSH ] {REPOSITORY}'
        embed[
            'description'
        ] = f'**{PUSHER}** push **{COMMIT_COUNT}** {"commit" if COMMIT_COUNT==1 else "commits"} to **{REF_NAME}**'
        embed['color'] = 0x5FC3FF
        embed['fields'] = fields

elif EVENT_NAME == 'pull_request':
    HEAD_REF = data.get('head_ref')
    BASE_REF = data.get('base_ref')
    if target.get('pull_request', []) == [] or BASE_REF in target.get('pull_request'):
        pull_request = event.get('pull_request')
        TITLE = pull_request.get('title')
        COMMITS = pull_request.get('commits')
        USER = pull_request.get('user').get('login')
        embed['title'] = f'[ PULL REQUEST ] {REPOSITORY}'
        embed[
            'description'
        ] = f'**{USER}** want to merge **{COMMITS}** {"commit" if COMMITS==1 else "commits"} into **{BASE_REF}** from **{HEAD_REF}**'
        embed['color'] = 0xFFAA55
        embed['fields'] = [{'name': TITLE, 'value': ''}]

if embed != {}:
    match mode:
        case 'user':
            token = os.environ.get('token')
            if token is None:
                raise Exception('you need to set discord bot token')
            users = config.get('user', [])
            if users == []:
                raise Exception('you need to add user id to list')
            channels = get_channel_ids(users, token)
            for channel in channels:
                requests.post(
                    f'https://discordapp.com/api/v6/channels/{channel}/messages',
                    headers={'authorization': f'Bot {token}'},
                    json={'embeds': [embed]},
                )
        case 'channel':
            webhook = os.environ.get('webhook')
            if webhook is None:
                raise Exception('you need to set discord webhook')
            requests.post(
                webhook,
                json={
                    'username': 'Github Notification',
                    'avatar_url': 'https://avatars.githubusercontent.com/in/15368?s=64&v=4',
                    'embeds': [embed],
                },
            )
        case _:
            raise Exception('mode can only be user or channel')
