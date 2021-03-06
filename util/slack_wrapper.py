from slackclient import SlackClient
from util.util import *


class SlackWrapper:
    """
    Slack API wrapper
    """

    def __init__(self, api_key):
        """
        SlackWrapper constructor.
        Connect to the real-time messaging API and
        load the bot's login data.
        """
        self.api_key = api_key
        self.client = SlackClient(self.api_key)
        self.connected = self.client.rtm_connect()
        self.server = None
        self.username = None
        self.user_id = None

        if self.connected:
            self.server = self.client.server
            self.username = self.server.username
            self.user_id = self.server.login_data.get("self").get("id")

    def read(self):
        """Read from the real-time messaging API."""
        return self.client.rtm_read()

    def invite_user(self, user, channel, is_private=False):
        """
        Invite a user to a given channel.
        """

        api_call = "groups.invite" if is_private else "channels.invite"
        return self.client.api_call(api_call, channel=channel, user=user)

    def set_purpose(self, channel, purpose, is_private=False):
        """
        Set the purpose of a given channel.
        """

        api_call = "groups.setPurpose" if is_private else "channels.setPurpose"
        return self.client.api_call(api_call, purpose=purpose, channel=channel)

    def get_members(self):
        """
        Return a list of all members.
        """
        return self.client.api_call("users.list", presence=True)

    def get_member(self, user_id):
        """
        Return a member for a given user_id.
        """
        return self.client.api_call("users.info", user=user_id)

    def create_channel(self, name, is_private=False):
        """
        Create a channel with a given name.
        """
        api_call = "groups.create" if is_private else "channels.create"
        return self.client.api_call(api_call, name=name, validate=False)

    def rename_channel(self, channel_id, new_name, is_private=False):
        """
        Rename an existing channel.
        """
        api_call = "groups.rename" if is_private else "channels.rename"

        return self.client.api_call(api_call, channel=channel_id, name=new_name, validate=False)

    def get_channel_info(self, channel_id, is_private=False):
        """
        Return the channel info of a given channel ID.
        """

        api_call = "groups.info" if is_private else "channels.info"
        return self.client.api_call(api_call, channel=channel_id)

    def update_channel_purpose_name(self, channel_id, new_name, is_private=False):
        """
        Updates the channel purpose 'name' field for a given channel ID.
        """

        # Update channel purpose
        channel_info = self.get_channel_info(channel_id, is_private)
        key = "group" if is_private else "channel"

        if channel_info:
            purpose = load_json(channel_info[key]['purpose']['value'])
            purpose['name'] = new_name

            self.set_purpose(channel_id, json.dumps(purpose), is_private)

    def post_message(self, channel_id, text, parse="full"):
        """
        Post a message in a given channel.
        channel_id can also be a user_id for private messages.
        """
        self.client.api_call("chat.postMessage", channel=channel_id,
                             text=text, as_user=True, parse=parse)

    def get_public_channels(self):
        """Fetch all public channels."""
        return self.client.api_call("channels.list")

    def get_private_channels(self):
        """Fetch all private channels in which the user participates."""
        return self.client.api_call("groups.list")

    def archive_private_channel(self, channel_id):
        """Archive a private channel"""
        return self.client.api_call("groups.archive", channel=channel_id)
