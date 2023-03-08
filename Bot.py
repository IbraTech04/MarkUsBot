import nextcord
from nextcord.ext import commands
import os
import dotenv
dotenv.load_dotenv("tokens.env")
from nextcord.ext import tasks
from Notifier import Notifier

markusbot = commands.Bot()

notifiers = []

@markusbot.slash_command(name="addnotifier", description="Adds a course to the list of courses to be notified about")
async def addnotifider(interaction: nextcord.Interaction, username: str, password: str, courseid: str, channel: nextcord.abc.GuildChannel, role: nextcord.Role):
    # defer the response so that the bot doesn't time out
    await interaction.response.defer()
    notifiers.append(Notifier(username, password, courseid, int(channel.id), int(role.id)))
    await interaction.followup.send(f"Added notifier for {courseid} in {channel.mention} with role {role.mention}")

@tasks.loop(seconds=60)
async def check_for_assignments():
    for notifier in notifiers:
        assignments_to_announce = notifier.get_released_assignments()
        for assignment in assignments_to_announce:
            channel = markusbot.get_channel(notifier._channel_id)
            role = channel.guild.get_role(notifier._role_id)
            await channel.send(f"{role.mention} `{assignment.get_name()}` has been released on MarkUs!")    
check_for_assignments.start()

@markusbot.event
async def on_ready():
    print(f"Logged in as {markusbot.user}")

markusbot.run(os.getenv("BOT_TOKEN"))