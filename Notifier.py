import nextcord
from nextcord.ext import commands, tasks
from Webscraper_old import Webscraper
from MarkUsUtils import Course, Assignment

class Notifier(commands.Cog):
    """
    Class which keeps track of MarkUs Assignments and notifies the user when an assignment is due
    
    === Attributes ===
    _assignments: list of assignments
    _webscraper: webscraper object used to scrape MarkUs
    _channel_id: channel id of the Discord channel to send notifications to
    _role_id: role id of the Discord role to mention when sending notifications
    ====== Representation Invariants ======
    _channel_id must be a valid channel id
    _role_id must be a valid role id
    """
    
    _assignments: dict[str, Assignment]
    _webscraper: Webscraper
    _channel_id: int
    _role_id: int
    
    def __init__(self, bot: commands.Bot, markus_url: str, course_id: int, role_id: int, channel_id: int) -> None:
        """
        Initialize a Notifier object
        """
        super().__init__()
        self.bot = bot
        self.course = Course(markus_url, course_id)
        self._role_id = role_id
        self._channel_id = channel_id
        self.check_for_assignments.start()
    
    def new_assignments_refresh(self) -> list[Assignment]:
        """
        Method invoked by the bot to get a list of all new assignments
        """
        self.course._update_assignments()
        return self.course.get_new_assignments()
    
    @tasks.loop(seconds=60)
    async def check_for_assignments(self):
        """
        Method which checks for new assignments every 60 seconds
        """
        for assignment in self.new_assignments_refresh():
            channel = self.bot.get_channel(self._channel_id)
            role = channel.guild.get_role(self._role_id)
            await channel.send(f"{role.mention} `{assignment.get_name()}` has been released on MarkUs! It is due <t:{int(assignment.get_due_date().timestamp())}:F> (<t:{int(assignment.get_due_date().timestamp())}:R>)")
            assignment.set_announced(True)
        