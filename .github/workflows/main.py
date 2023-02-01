import os
import json


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


def send_to_channel(channel_id, token, payload):
    return requests.post(
        f'https://discordapp.com/api/v6/channels/{channel_id}/messages',
        headers={'authorization': f'Bot {token}'},
        json=payload,
    )


data = load_data()
with open('./config.json', 'r') as file:
    config = json.load(file)
target = config['target']
mode = config['mode']
embed = {}

EVENT_NAME = data['event_name']
REPOSITORY = data['repository']
event = data['event']

if EVENT_NAME == 'push':
    REF_NAME = data['ref_name']
    if target['push'] == [] or REF_NAME in target['push']:
        event = data['event']
        PUSHER = event['pusher']['name']
        head_commit = event['head_commit']
        # HEAD_AUTHOR = head_commit['author']['username']
        # HEAD_COMMITTER = head_commit['committer']['username']
        # HEAD_MESSAGE = head_commit['message']

        commits = event['commits']
        COMMIT_COUNT = len(commits)
        fields = [0] * COMMIT_COUNT
        for i in range(COMMIT_COUNT):
            commit = commits[i]
            # author = commit['author']['username']
            # committer = commit['committer']['username']
            message = commit['message']
            fields[i] = {'name': message, 'value': ''}

        embed['title'] = f'[ PUSH ] {REPOSITORY}'
        embed[
            'description'
        ] = f'**{PUSHER}** push **{COMMIT_COUNT}** {"commit" if COMMIT_COUNT==1 else "commits"} to **{REF_NAME}**'
        embed['color'] = 0x5FC3FF
        embed['fields'] = fields

elif EVENT_NAME == 'pull_request':
    HEAD_REF = data['head_ref']
    BASE_REF = data['base_ref']
    if target['pull_request'] == [] or BASE_REF in target['pull_request']:
        pull_request = data['event']['pull_request']
        TITLE = pull_request['title']
        COMMITS = pull_request['commits']
        USER = pull_request['user']['login']
        embed['title'] = f'[ PULL REQUEST ] {REPOSITORY}'
        embed[
            'description'
        ] = f'**{USER}** want to merge **{COMMITS}** {"commit" if COMMITS==1 else "commits"} into **{BASE_REF}** from **{HEAD_REF}**'
        embed['color'] = 0xFFAA55
        embed['fields'] = [{'name': TITLE, 'value': ''}]

if embed != {}:
    match mode:
        case 'user':
            import requests
            token = os.environ.get('token')
            channels = get_channel_ids(config['user'], token)
            for channel in channels:
                send_to_channel(channel, token, {'embeds': [embed]})
        case 'channel':
            from discordwebhook import Discord
            webhook = os.environ.get('webhook')
            discord = Discord(url=webhook)
            discord.post(
                username='Github Notification',
                avatar_url='https://avatars.githubusercontent.com/in/15368?s=64&v=4',
                embeds=[embed]
            )
        case _:
            raise Exception('mode can only be user or channel')
