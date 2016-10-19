import os
import time
from slackclient import SlackClient


# starterbot's ID as an environment variable
# TODO fix virtualenvironment, i.e. the lines below
# BOT_ID = os.environ.get("BOT_ID")
# TODO enter bot_id (generated from print_bot_id.py)
BOT_ID = '???'

# constants
AT_BOT = "<@" + BOT_ID + ">"

# instantiate Slack & Twilio clients
# TODO fix virtualenvironment, i.e. lines below
# slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# TODO enter bot's token
BOT_TOKEN = '???'
bot = SlackClient(BOT_TOKEN)


def handle_command(command, channel):
    """
        Reiterates text posted after @bot_name
    """

    reit_text = 'ATTENTION: ' + str(command)

    bot.api_call("chat.postMessage", channel=channel,
                 text=reit_text, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip(), \
                       output['channel']
    return None, None


if __name__ == "__main__":

    bot.api_call("users.setPresence", presence='auto')
    bot.api_call("users.setActive")

    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if bot.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            slack_output = bot.rtm_read()

            # print output to terminal -- helpful to understand JSON format
            if slack_output:
                print(slack_output)

            command, channel = parse_slack_output(slack_output)
            if command and channel:
                handle_command(command, channel)

            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")


