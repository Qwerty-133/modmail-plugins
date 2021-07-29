def setup(bot):
    old_process_commands = bot.process_commands

    async def process_commands(self, message):
        if message.content.startswith(self.prefix):
            cmd = message.content[len(self.prefix):].strip().lower()

            # Convert message contents to lowercase if a snippet exists
            if cmd in self.snippets:
                message.content = self.prefix + cmd

        await old_process_commands(message)

    type(bot).process_commands = process_commands
