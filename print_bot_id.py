from slackclient import SlackClient
from cred import ACTIVE_BOT_TOKEN, ACTIVE_BOT_ID, ACTIVE_BOT_NAME

"""
    Run this script to generate bot and channel IDs
"""

# TODO fill in name (string) of bot and bot's token (generated on the bot's profile page)
BOT_NAME = '???'
SLACK_BOT_TOKEN = '???'


slack_client = SlackClient(SLACK_BOT_TOKEN)


def list_channels():
    channels_call = slack_client.api_call("channels.list", exclude_archived=0)
    if channels_call.get('ok'):
        return channels_call['channels']
    return None


def find_user_id(name_str):
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == name_str:
                print("ID for '" + user['name'] + "' is " + user.get('id'))
                return user.get('id')
    else:
        print("could not find user with the name " + name_str)
        return None


if __name__ == "__main__":

    find_user_id(BOT_NAME)

    channels = list_channels()
    if channels:
        print("Channels: ")
        for c in channels:
            print(c['name'] + " (" + c['id'] + ")")
    else:
        print("Unable to authenticate.")