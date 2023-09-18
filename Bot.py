import nextcord
from nextcord.ext import commands
import os
import dotenv
dotenv.load_dotenv("tokens.env")
from nextcord.ext import tasks
from Notifier import Notifier
from Exceptions import *


markusbot = commands.Bot()

notifiers = []

@markusbot.slash_command(name="addnotifier", description="Adds a course to the list of courses to be notified about")
async def addnotifiernew(interaction: nextcord.Interaction, courseid: str, instance_url: str, channel: nextcord.abc.GuildChannel, role: nextcord.Role):
    
    # Make sure the user has the manage server permission
    if not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message("You do not have the manage server permission.", ephemeral=True)
        return
    
    try:
        new = Notifier(courseid, int(channel.id), int(role.id))
        notifiers.append(new)
    except InvalidCourseID:
        await interaction.followup.send("Invalid course ID. Please check your course ID.")
    else:
        await interaction.followup.send(f"Successfully added notifier for {courseid} in {channel.mention}.")

        

@markusbot.slash_command(name="viewassignments", description="View the assignments for a course")
@commands.is_owner()
async def viewassignments(interaction: nextcord.Interaction):
    msg = "```"
    for assignment in notifiers[0]._assignments:
        msg += str(notifiers[0]._assignments[assignment]) + "\n"
    msg += "```"
    await interaction.response.send_message(msg)

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