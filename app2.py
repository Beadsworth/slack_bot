import os
import time
import datetime
from slackclient import SlackClient


message_throttle = 0

testing_channel_ID = 'C0PK4DX5K'
jimmies_URL = 'https://slack-files.com/T0FK55ALT-F2JA5NF6X-31845ac3f0'

# starterbot's ID as an environment variable
# TODO fix virtualenvironment, i.e. the two lines below
# BOT_ID = os.environ.get("BOT_ID")
ACTIVE_BOT_ID = 'U2J800Z1D'
PLEDGE_BOT_ID = 'U2J6LRM8U'

# constants
AT_BOT = "<@" + ACTIVE_BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# instantiate Slack & Twilio clients
# TODO fix virtualenvironment, i.e. the three lines below
# slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
ACTIVE_BOT_TOKEN = '?????'
PLEDGE_BOT_TOKEN = '?????'
active_bot = SlackClient(ACTIVE_BOT_TOKEN)
pledge_bot = SlackClient(PLEDGE_BOT_TOKEN)


# def handle_command(command, channel):
#     """
#         Receives commands directed at the bot and determines if they
#         are valid commands. If so, then acts on the commands. If not,
#         returns back what it needs for clarification.
#     """
#     response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
#                "* command with numbers, delimited by spaces."
#     if command.startswith(EXAMPLE_COMMAND):
#         response = "Sure...write some more code then I can do that!"
#
#     reit_text = 'ATTENTION: ' + str(command)
#
#     pledge_bot.api_call("chat.postMessage", channel='C2J7GQUNS',
#                         text=reit_text, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    global message_throttle

    joke_string = 'harambe'
    harambe_death_date = datetime.datetime(year=2016, month=5, day=28).date()
    harambe_emoji = 'harambe'
    harambe_URL = 'https://emoji.slack-edge.com/T0FK55ALT/harambe/36e7e02ae6e6a643.jpg'
    target_emoji = 'salty'
    flag_emoji = 'jimmies'

    if output_list and len(output_list) > 0:  # if there was a message

        for output in output_list:

            if output and 'text' in output and joke_string in output['text'].lower():  # if 'harambe' mention
                if 'subtype' in output and output['subtype'] == 'bot_message':  # break to avoid infinite loop
                    return None, None
                if 'user' in output and output['user'] == 'USLACKBOT':  # avoid slackbot
                    return None, None

                temp_channel = output['channel']
                today = datetime.datetime.now().date()
                date_diff = today - harambe_death_date
                num_of_days = date_diff.days
                out_message = 'It has been ' + str(num_of_days) + ' days since Harambe was brutally murdered.  Does Harambe still live in your heart?  Up-harambe if the spirit of Harambe still watches over you.'
                response = active_bot.api_call("chat.postMessage", channel=temp_channel, \
                                    text=out_message, as_user=False, username='Harambe\'s Ghost', icon_url=harambe_URL)

                message_throttle += 18000

                if response['ok']:
                    temp_channel = response['channel']
                    temp_ts = response['ts']
                    active_bot.api_call("reactions.add", name=harambe_emoji, channel=temp_channel, \
                                        timestamp=temp_ts)
                    print('Harambe successfully remembered')

            elif output and 'type' in output and output['type'] == 'reaction_added' \
                    and output['reaction'] == target_emoji:  # if salty emote added

                temp_item = output['item']
                temp_channel = temp_item['channel']
                temp_ts = temp_item['ts']
                temp_type = temp_item['type']
                response = active_bot.api_call("reactions.get", channel=temp_channel, timestamp=temp_ts)

                temp_item_reactions = response['message']['reactions']
                if response['ok'] is False:
                    print('Bad response')
                    return None, None

                for reaction in temp_item_reactions:
                    if reaction['name'] == flag_emoji and reaction['count'] > 0:  # break out if flag emoji present
                        return None, None
                    if reaction and reaction['name'] == target_emoji and reaction['count'] == 3:
                        # add jimmies emoji to original message and post jimmies_url
                        pf = active_bot.api_call("reactions.add", name=flag_emoji, channel=temp_channel,\
                                                 timestamp=temp_ts)
                        if pf['ok']:
                            active_bot.api_call("chat.postMessage", channel=temp_channel,\
                                            text=jimmies_URL, as_user=False)
                            print('Jimmies have been rustled!')
                            message_throttle += 18000
                        else:
                            print('Jimmies failed!')


                #print(temp_item_reactions)
#
                #return 'print_jimmy', output['channel']

    return None, None


if __name__ == "__main__":

    pledge_bot.api_call("users.setPresence", presence='auto')
    pledge_bot.api_call("users.setActive")
    active_bot.api_call("users.setPresence", presence='auto')
    active_bot.api_call("users.setActive")

    #active_bot.api_call("chat.postMessage", channel=testing_channel_ID,
    #                    text=jimmies_URL, as_user=True)

    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if active_bot.rtm_connect():
        print("StarterBot connected and running!")
        while True:

            rtm_output = active_bot.rtm_read()
            if rtm_output:
                print(rtm_output)

            command, channel = parse_slack_output(rtm_output)
            if command and channel:
                # handle_command(command, channel)
                pass

            if message_throttle > 85000:
                raise RuntimeError('Too many messages, shutting down.')
            elif message_throttle <= 0:
                message_throttle = 0
            else:
                message_throttle -= 1

            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")