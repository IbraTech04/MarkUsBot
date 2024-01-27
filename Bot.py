import nextcord
from nextcord.ext import commands, tasks
import os
import dotenv
dotenv.load_dotenv("tokens.env")
from Notifier import Notifier
from Exceptions import *


markusbot = commands.Bot()

notifiers = []

@markusbot.slash_command(name="add", description="Adds a course to the list of courses to be notified about")
async def add(interaction: nextcord.Interaction):
    pass

@add.subcommand(name="standard", description="Add a standard course notifier")
async def addnotifiernew(interaction: nextcord.Interaction, course_id: int, instance_url: str, channel: nextcord.abc.GuildChannel, role: nextcord.Role):
    # Make sure the user has the manage server permission
    if not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message("You do not have the manage server permission.", ephemeral=True)
        return
    await interaction.response.defer()    
    try:
        new = Notifier(markusbot, instance_url, course_id, int(role.id), int(channel.id))
        markusbot.add_cog(new)
    except InvalidCourseID:
        await interaction.followup.send("Invalid course ID. Please check your course ID.")
    else:
        await interaction.followup.send(f"Successfully added notifier for {course_id} in {channel.mention}.")

@add.subcommand(name="shibboleth", description="Add a course notifier for a Shibboleth course")
async def addnotifiershibboleth(interaction: nextcord.Interaction, courseid: str, instance_url: str, channel: nextcord.abc.GuildChannel, role: nextcord.Role, username: str, password: str):
    pass

# The main loop that checks for new assignments
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