import discord
from discord.ext import commands
from datetime import datetime
import asyncio
import aiosqlite
import requests
import re

quake_logo = "https://media.discordapp.net/attachments/1363337978742833409/1363342899474862233/QuakeLogo.png?ex=6805af84&is=68045e04&hm=d65ade377e31ed97126ff99ac7b7e693f63ead68d24e12903fcf7f1ad7905af0&=&format=webp&quality=lossless"
quake_color = 0x3fb7f0

color_mapping = {
    "red": 0xd40001,
    "orange": 0xff6800,
    "yellow": 0xffe600,
    "green": 0x02ce16,
    "blue": 0x0038ff,
    "purple": 0x4c00cb,
    "pink": 0xffa2ed,
    "brown": 0x752c00,
    "black": 0x000000,
    "grey": 0x909090,
    "white": 0xffffff
}

class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sniped_messages = {}

    @commands.Cog.listener()
    async def on_ready(self):
        await self.create_todo_table()
        await self.create_remind_table()
        await self.create_afk_table()
        await self.initialize_database()
        await self.create_card_table()

    async def create_todo_table(self):
        async with aiosqlite.connect("dbs/todo.db") as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS todos (
                    user_id INTEGER, 
                    todo TEXT
                )
            ''')
            await db.commit()

    async def create_remind_table(self):
        async with aiosqlite.connect("dbs/remind.db") as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS reminders (
                    user_id INTEGER,
                    server_id INTEGER,
                    time TEXT,
                    task TEXT
                )
            ''')
            await db.commit()

    async def create_afk_table(self):
        async with aiosqlite.connect("dbs/afk.db") as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS afk (
                    user_id INTEGER PRIMARY KEY,
                    afk_message TEXT,
                    afk_timestamp TEXT
                )
            ''')
            await db.commit()

    async def create_card_table(self):
        async with aiosqlite.connect("dbs/card.db") as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS card (
                    user_id INTEGER PRIMARY KEY,
                    nickname TEXT,
                    bio TEXT,
                    age INTEGER,
                    pronouns TEXT,
                    birthday TEXT,
                    ideology TEXT,
                    color TEXT
                )
            ''')
            await db.commit()

    async def get_user_card(self, user_id):
        async with aiosqlite.connect("dbs/card.db") as db:
            async with db.execute("SELECT * FROM card WHERE user_id = ?", (user_id,)) as cursor:
                return await cursor.fetchone()

    async def update_user_card(self, user_id, **kwargs):
        columns = ', '.join(f"{key} = ?" for key in kwargs.keys())
        values = list(kwargs.values()) + [user_id]
        async with aiosqlite.connect("dbs/card.db") as db:
            await db.execute(f"UPDATE card SET {columns} WHERE user_id = ?", values)
            await db.commit()

    async def create_user_card(self, user_id):
        async with aiosqlite.connect("dbs/card.db") as db:
            await db.execute("INSERT OR IGNORE INTO card (user_id) VALUES (?)", (user_id,))
            await db.commit()

    async def set_afk(self, user_id, afk_message):
        afk_timestamp = datetime.utcnow().isoformat()
        async with aiosqlite.connect("dbs/afk.db") as db:
            await db.execute("REPLACE INTO afk (user_id, afk_message, afk_timestamp) VALUES (?, ?, ?)", (user_id, afk_message, afk_timestamp))
            await db.commit()

    async def remove_afk(self, user_id):
        async with aiosqlite.connect("dbs/afk.db") as db:
            await db.execute("DELETE FROM afk WHERE user_id = ?", (user_id,))
            await db.commit()

    async def get_afk(self, user_id):
        async with aiosqlite.connect("dbs/afk.db") as db:
            async with db.execute("SELECT afk_message, afk_timestamp FROM afk WHERE user_id = ?", (user_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return row
                return None, None

    async def set_user_card_color(self, user_id, color):
        async with aiosqlite.connect("dbs/card.db") as db:
            await db.execute("UPDATE card SET color = ? WHERE user_id = ?", (hex(color), user_id))
            await db.commit()
    
    async def initialize_database(self):
        self.db_conn = await aiosqlite.connect("dbs/configs.db")

    async def has_role(self, user, guild_id, role_type):
        async with aiosqlite.connect("dbs/configs.db") as db:
            async with db.execute(f"SELECT {role_type} FROM server_configs WHERE server_id = ?", (guild_id,)) as cursor:
                row = await cursor.fetchone()
                if row and row[0]:
                    roles = row[0].split(',')
                    user_roles = [role.id for role in user.roles]
                    if any(int(role) in user_roles for role in roles):
                        return True
        return False

    async def has_admin_role(self, user, guild_id):
        return await self.has_role(user, guild_id, "admin")

    @commands.hybrid_command(description="Sends information about a user")
    async def whois(self, ctx, user: discord.Member):
        e = discord.Embed(color=quake_color)
        e.set_author(name=f"Checking Records...", icon_url=quake_logo),
        if user.avatar:
            e.set_thumbnail(url=user.avatar.url)
        e.add_field(name="📍 Mention", value=user.mention)
        e.add_field(name="🔖 ID", value=user.id)
        e.add_field(name="📑 Nickname", value=user.display_name)
        e.add_field(name="📅 Created On", value=user.created_at.strftime("`%B %d, %Y %H:%M %p`"))
        e.add_field(name="📅 Joined On", value=user.joined_at.strftime("`%B %d, %Y %H:%M %p`"))
        if user.premium_since:
            e.add_field(name=f"<a:DiscordBoost:1121298549657829436> Boosting", value=user.premium_since.strftime("`%B %d, %Y %H:%M %p`"))
        e.add_field(name="👑 Top Role", value=user.top_role.mention)
        e.add_field(name="🎲 Activity", value=f"{user.activity.name}" if user.activity is not None else None)
        emotes = {
            "hypesquad_brilliance": "<:HypeSquadBrilliance:1123772502024405053>",
            "hypesquad_bravery": "<:HypeSquadBravery:1123772444994437240>",
            "hypesquad_balance": "<:HypeSquadBalance:1123772443069259897>",
            "bug_hunter": "<:BugHunter:1123772432679981057>",
            "bug_hunter_level_2": "<:BugHunterLevel2:1123772435150422086>",
            "early_verified_bot_developer": "<:EarlyVerifiedBotDeveloper:1123772440338776064>",
            "verified_bot_developer": "<:EarlyVerifiedBotDeveloper:1123772440338776064>",
            "active_developer": "<:ActiveDeveloper:1123772429307744287>",
            "hypesquad": "<:HypeSquadEvents:1123772447125155963>",
            "early_supporter": "<:EarlySupporter:1123772438380019762>",
            "discord_certified_moderator": "<:ModeratorProgramsAlumni:1123772518365409370>",
            "staff": "<:Staff:1123772450430267393>",
            "partner": "<:Partner:1123774032932769812>",
        }
        badges = [
            emoji
            for f in user.public_flags.all()
            if (emoji := emotes.get(f.name))
        ]
        if badges:
            e.add_field(name="🧬 Flags", value=" ".join(badges))
        else:
            e.add_field(name="🧬 Flags", value="None")
        e.add_field(name="🤖 Bot?", value=user.bot)
        if user.status != user.mobile_status:
            e.add_field(name="📺 Device", value="Desktop")
        elif user.status != user.desktop_status:
            e.add_field(name="📺 Device", value="Mobile")
        req = await self.bot.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
        banner_id = req["banner"]
        if banner_id:
            banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024"
            e.add_field(name="📰 Banner", value="**Linked Below**")
            e.set_image(url=banner_url)
        else:
            e.add_field(name="📰 Banner", value="None")
        e.set_footer(text=f"Requested by {ctx.author}"),
        e.timestamp = datetime.utcnow()
        await ctx.send(embed=e)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        self.sniped_messages[message.channel.id] = (message, "deleted", datetime.utcnow())

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot: 
            return
        self.sniped_messages[before.channel.id] = (before, "edited", datetime.utcnow())
    
    def format_time_delta(self, delta):
        seconds = delta.total_seconds()
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = ""
        if hours > 0:
            time_str += f"{int(hours)}h "
        if minutes > 0:
            time_str += f"{int(minutes)}m "
        time_str += f"{int(seconds)}s"
        return time_str
    
    @commands.hybrid_command(description="Fetch a user's avatar")
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        try:
            e = discord.Embed(color=quake_color)
            e.set_author(name=f"{member.display_name}'s Avatar", icon_url=member.avatar.url)
            e.set_image(url=member.avatar.url)
            await ctx.send(embed=e)
        except Exception as e:
            print(f"Error in avatar command: {e}")

    @commands.hybrid_command(description="Sends the most recent deleted or edited message")
    async def snipe(self, ctx):
        try:
            sniped_data = self.sniped_messages.get(ctx.channel.id)
            if sniped_data is None:
                await ctx.send("There are no recently deleted or edited messages to snipe.", ephemeral=True)
                return
            sniped_message, action, timestamp = sniped_data
            time_since = datetime.utcnow() - timestamp
            action_verb = "🗑 Deleted" if action == "deleted" else "📝 Edited"
            footer_text = f"{action_verb} {self.format_time_delta(time_since)} ago"
            e = discord.Embed(color=quake_color)
            e.set_author(name=sniped_message.author.name, icon_url=sniped_message.author.avatar.url)
            e.description = f"> {sniped_message.content}" if sniped_message.content else "No text content"
            if sniped_message.attachments:
                attachment_url = sniped_message.attachments[0].url
                e.set_image(url=attachment_url)
            e.set_footer(text=footer_text)
            await ctx.send(embed=e)
            self.sniped_messages[ctx.channel.id] = None
        except Exception as e:
            print(e)

    @commands.hybrid_command(description="Set a reminder | s, m, h, d")
    async def remind(self, ctx, time, *, task):
        def convert(time):
            pos = ['s', 'm', 'h', 'd']
            time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600*24}
            unit = time[-1]
            if unit not in pos:
                return -1
            try:
                val = int(time[:-1])
            except:
                return -2
            return val * time_dict[unit]

        converted_time = convert(time)
        if converted_time == -1:
            await ctx.send("You didn't input the time correctly!")
            return
        if converted_time == -2:
            await ctx.send("The time must be an integer!")
            return

        e = discord.Embed(color=quake_color)
        e.description = "⏰ **Started Reminder** ⏰"
        e.add_field(name="Time", value=time)
        e.add_field(name="Task", value=task)
        e.set_footer(text=f"Requested by {ctx.author}")
        e.timestamp = datetime.utcnow()
        await ctx.send(embed=e)

        try:
            async with aiosqlite.connect("dbs/remind.db") as db:
                await db.execute("INSERT INTO reminders (user_id, server_id, time, task) VALUES (?, ?, ?, ?)", (ctx.author.id, ctx.guild.id, time, task))
                await db.commit()
        except Exception as e:
            print(e)

        await asyncio.sleep(converted_time)
        e = discord.Embed(color=quake_color)
        e.description = "⏰ **Time's Up** ⏰"
        e.add_field(name="Task", value=f"> {task}")
        await ctx.send(ctx.author.mention, embed=e)

        try:
            async with aiosqlite.connect("dbs/remind.db") as db:
                await db.execute("DELETE FROM reminders WHERE user_id = ? AND server_id = ? AND time = ? AND task = ?", (ctx.author.id, ctx.guild.id, time, task))
                await db.commit()
        except Exception as e:
            print(e)

    @commands.hybrid_command(description="List all your reminders")
    async def remindlist(self, ctx):
        try:
            author_id = ctx.author.id
            async with aiosqlite.connect("dbs/remind.db") as db:
                cursor = await db.execute("SELECT time, task FROM reminders WHERE user_id = ? AND server_id = ?", (author_id, ctx.guild.id))
                reminders = await cursor.fetchall()
            if not reminders:
                await ctx.send(f"**{ctx.author.name}** has no reminders set!", ephemeral=True)
            else:
                reminders_list = "\n".join([f"- ⏳ {time} **|** {task}" for time, task in reminders])
                e = discord.Embed(color=quake_color)
                e.set_author(name=f"📋 {ctx.author.name}'s Reminders 📋")
                e.description = reminders_list
                await ctx.send(embed=e, ephemeral=True)
        except Exception as e:
            print(e)

    @commands.hybrid_group(name="todo", description="Todo list commands")
    async def todo_group(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @todo_group.command(name="add", description="Add a task to your to-do list")
    async def add(self, ctx, *, task):
        author_id = ctx.author.id
        async with aiosqlite.connect("dbs/todo.db") as db:
            await db.execute("INSERT INTO todos (user_id, todo) VALUES (?, ?)", (author_id, task))
            await db.commit()
        await ctx.send(f"Added **{task}** to your todo list!", ephemeral=True)

    @todo_group.command(name="delete", description="Delete a task from your to-do list")
    async def delete(self, ctx, todo_num: int):
        author_id = ctx.author.id
        async with aiosqlite.connect("dbs/todo.db") as db:
            cursor = await db.execute("SELECT rowid, todo FROM todos WHERE user_id = ?", (author_id,))
            rows = await cursor.fetchall()
            if todo_num <= 0 or todo_num > len(rows):
                await ctx.send("Invalid todo number!", ephemeral=True)
                return
            todo_id, todo_text = rows[todo_num - 1]
            await db.execute("DELETE FROM todos WHERE rowid = ?", (todo_id,))
            await db.commit()
        await ctx.send(f"Deleted **{todo_text}** from your todo list!", ephemeral=True)

    @todo_group.command(name="clear", description="Clear all tasks from your to-do list")
    async def clear(self, ctx):
        author_id = ctx.author.id
        async with aiosqlite.connect("dbs/todo.db") as db:
            await db.execute("DELETE FROM todos WHERE user_id = ?", (author_id,))
            await db.commit()
        await ctx.send("Cleared all tasks from your todo list!", ephemeral=True)

    @todo_group.command(name="list", description="Look at your to-do list")
    async def list(self, ctx):
        author_id = ctx.author.id
        async with aiosqlite.connect("dbs/todo.db") as db:
            cursor = await db.execute("SELECT todo FROM todos WHERE user_id = ?", (author_id,))
            todos = await cursor.fetchall()
        if not todos:
            await ctx.send(f"**{ctx.author.name}** has no tasks in their todo list!", ephemeral=True)
        else:
            todo_list = "\n".join([f"> **{idx + 1})** {todo[0]}" for idx, todo in enumerate(todos)])
            e = discord.Embed(color=quake_color)
            e.set_author(name=f"📋 {ctx.author.name}'s Todo List 📋")
            e.description = todo_list
            await ctx.send(embed=e, ephemeral=True)

    @commands.hybrid_command(description="Let other users know you're going to be AFK")
    async def afk(self, ctx, *, message: str):
        try:
            await self.create_afk_table()
            await self.set_afk(ctx.author.id, message)
            await ctx.send(f"👋 **|** See you later **{ctx.author.name}**!")
        except Exception as e:
            print(e)

    @commands.hybrid_group(name="emoji", description="Emoji commands")
    async def emoji_group(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @emoji_group.command(name="steal", description="Get the file link to an emoji")
    async def steal(self, ctx, emoji: discord.PartialEmoji):
        if emoji.id:
            emoji_url = emoji.url
            await ctx.send(f":link: {emoji_url}", ephemeral=True)
        else:
            await ctx.send("Please provide a custom emoji.", ephemeral=True)

    @emoji_group.command(name="add", description="Add an emoji to the server")
    async def add(self, ctx, name: str):
        if not await self.has_admin_role(ctx.author, ctx.guild.id):
            await ctx.send("You don't have the required permissions for this command!", ephemeral=True, delete_after=10)
            return
        if len(ctx.message.attachments) == 0:
            await ctx.send("Please upload an image to add as an emoji.", ephemeral=True)
            return
        image = await ctx.message.attachments[0].read()
        try:
            emoji = await ctx.guild.create_custom_emoji(name=name, image=image)
            await ctx.send(f"Emoji `{emoji.name}` added successfully!")
        except Exception as e:
            await ctx.send(f"Failed to add emoji", ephemeral=True)
            print(e)

    @emoji_group.command(name="delete", description="Delete an emoji from the server")
    async def delete(self, ctx, name: str = None, id: int = None):
        if not await self.has_admin_role(ctx.author, ctx.guild.id):
            await ctx.send("You don't have the required permissions for this command!", ephemeral=True, delete_after=10)
            return
        emoji = None
        if name:
            emoji = discord.utils.get(ctx.guild.emojis, name=name)
        elif id:
            emoji = discord.utils.get(ctx.guild.emojis, id=id)
        if not emoji:
            await ctx.send("Emoji not found.", ephemeral=True)
            return
        try:
            await emoji.delete()
            await ctx.send(f"Emoji `{emoji.name}` deleted successfully!", ephemeral=True)
        except Exception as e:
            await ctx.send(f"Failed to delete emoji", ephemeral=True)
            print(e)

    @emoji_group.command(name="info", description="Get information about an emoji")
    async def info(self, ctx, name: str = None, id: int = None):
        emoji = None
        if name:
            emoji = discord.utils.get(ctx.guild.emojis, name=name)
        elif id:
            emoji = discord.utils.get(ctx.guild.emojis, id=id)
        if not emoji:
            await ctx.send("Emoji not found.")
            return
        timestamp = int(emoji.created_at.timestamp())
        e = discord.Embed(title=f"🔍 Emoji Info: {emoji.name}", color=quake_color)
        e.add_field(name="📑 Name", value=f"> `{emoji.name}`", inline=False)
        e.add_field(name="📌 ID", value=f"> {emoji.id}", inline=False)
        e.add_field(name="📅 Date of Creation", value=f"> <t:{timestamp}:f>", inline=False)
        e.set_thumbnail(url=emoji.url)
        await ctx.send(embed=e)

    @emoji_group.command(name="rename", description="Rename an emoji in the server")
    async def rename(self, ctx, id: int, new_name: str):
        if not await self.has_admin_role(ctx.author, ctx.guild.id):
            await ctx.send("You don't have the required permissions for this command!", ephemeral=True, delete_after=10)
            return
        emoji = discord.utils.get(ctx.guild.emojis, id=id)
        if not emoji:
            await ctx.send("Emoji not found.", ephemeral=True)
            return
        try:
            await emoji.edit(name=new_name)
            await ctx.send(f"Emoji renamed to `{new_name}` successfully!", ephemeral=True)
        except Exception as e:
            await ctx.send(f"Failed to rename emoji!", ephemeral=True)
            print(e)

    @commands.hybrid_group(name="sticker", description="Sticker commands")
    async def sticker_group(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @sticker_group.command(name="steal", description="Get the file link to a sticker")
    async def steal(self, ctx):
        await ctx.send("Post the sticker you want to steal!", ephemeral=True)
        def check_sticker(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.stickers
        try:
            sticker_message = await self.bot.wait_for('message', check=check_sticker, timeout=60)
            sticker_item = sticker_message.stickers[0]
            await sticker_message.delete()
            sticker = await self.bot.fetch_sticker(sticker_item.id)
            if sticker.format == discord.StickerFormatType.png:
                sticker_url = sticker.url
                await ctx.send(f":link: {sticker_url}", ephemeral=True)
            elif sticker.format == discord.StickerFormatType.apng:
                await ctx.send(f"Due to Discord not supporting it, I can't grab animated stickers, sorry!", ephemeral=True)
            else:
                await ctx.send("Unsupported sticker format.", ephemeral=True)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond. Please try the command again.", ephemeral=True)
        except Exception as e:
            await ctx.send(f"Failed to fetch sticker URL.", ephemeral=True)
            print(e)

    @sticker_group.command(name="add", description="Add a sticker to the server")
    async def add(self, ctx):
        if not await self.has_admin_role(ctx.author, ctx.guild.id):
            await ctx.send("You don't have the required permissions for this command!", ephemeral=True, delete_after=10)
            return
        await ctx.send("Please upload the image you want to add as a sticker (`PNG`, `APNG`, or `Lottie JSON`, under `500 KB`, `320x320` pixels).")
        def check_image(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.attachments
        try:
            image_message = await self.bot.wait_for('message', check=check_image, timeout=60)
            attachment = image_message.attachments[0]
            if attachment.size > 500 * 1024:
                await ctx.send("The uploaded file exceeds the size limit of `500 KB`. Please upload a smaller file and restart the command.", ephemeral=True)
                return
            valid_types = ["image/png", "image/apng", "application/json"]
            if attachment.content_type not in valid_types:
                await ctx.send("The uploaded file is not a valid type. Please upload a `PNG`, `APNG`, or `Lottie JSON` file. Restart the command.", ephemeral=True)
                return
            await ctx.send("Please provide the name for the sticker.")
            def check_name(message):
                return message.author == ctx.author and message.channel == ctx.channel
            name_message = await self.bot.wait_for('message', check=check_name, timeout=60)
            name = name_message.content
            await ctx.send("Please provide the emoji to tag the sticker.")
            def check_emoji(message):
                return message.author == ctx.author and message.channel == ctx.channel
            emoji_message = await self.bot.wait_for('message', check=check_emoji, timeout=60)
            emoji = emoji_message.content
            file = await attachment.to_file()
            sticker = await ctx.guild.create_sticker(name=name, file=file, description=name, emoji=emoji)
            await ctx.send(f"Sticker `{sticker.name}` added successfully!", ephemeral=True)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond. Please try the command again.", ephemeral=True)
        except Exception as e:
            await ctx.send(f"Failed to add sticker", ephemeral=True)
            print(e)

    @sticker_group.command(name="delete", description="Delete a sticker from the server")
    async def delete(self, ctx, name: str = None, id: int = None):
        if not await self.has_admin_role(ctx.author, ctx.guild.id):
            await ctx.send("You don't have the required permissions for this command!", ephemeral=True, delete_after=10)
            return
        sticker = None
        if name:
            sticker = discord.utils.get(ctx.guild.stickers, name=name)
        elif id:
            sticker = discord.utils.get(ctx.guild.stickers, id=id)
        if not sticker:
            await ctx.send("Sticker not found.", ephemeral=True)
            return
        try:
            await sticker.delete()
            await ctx.send(f"Sticker `{sticker.name}` deleted successfully!", ephemeral=True)
        except Exception as e:
            await ctx.send(f"Failed to delete sticker", ephemeral=True)
            print(e)

    @sticker_group.command(name="info", description="Get information about a sticker")
    async def info(self, ctx, name: str = None, id: int = None):
        try:
            sticker = None
            if name:
                sticker = discord.utils.get(ctx.guild.stickers, name=name)
            elif id:
                sticker = discord.utils.get(ctx.guild.stickers, id=id)
            if not sticker:
                await ctx.send("Sticker not found.", ephemeral=True)
                return
            timestamp = int(sticker.created_at.timestamp())
            e = discord.Embed(title=f"🔍 Sticker Info: {sticker.name}", color=quake_color)
            e.set_thumbnail(url=sticker.url)
            e.add_field(name="📑 Name", value=f"> `{sticker.name}`", inline=False)
            e.add_field(name="📌 ID", value=f"> {sticker.id}", inline=False)
            e.add_field(name="📅 Date of Creation", value=f"> <t:{timestamp}:f>", inline=False)
            await ctx.send(embed=e)
        except Exception as e:
            print(e)

    @sticker_group.command(name="rename", description="Rename a sticker in the server")
    async def rename(self, ctx, id: int, new_name: str):
        if not await self.has_admin_role(ctx.author, ctx.guild.id):
            await ctx.send("You don't have the required permissions for this command!", ephemeral=True, delete_after=10)
            return
        sticker = discord.utils.get(ctx.guild.stickers, id=id)
        if not sticker:
            await ctx.send("Sticker not found.", ephemeral=True)
            return
        try:
            await sticker.edit(name=new_name)
            await ctx.send(f"Sticker renamed to `{new_name}` successfully!", ephemeral=True)
        except Exception as e:
            await ctx.send(f"Failed to rename sticker!", ephemeral=True)
            print(e)

    @commands.hybrid_group(name="card", description="Card commands")
    async def card_group(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @card_group.command(name="nickname", description="Set your card nickname")
    async def nickname(self, ctx, *, nickname: str):
        await self.create_user_card(ctx.author.id)
        await self.update_user_card(ctx.author.id, nickname=nickname)
        await ctx.send(f"Your card's nickname has been updated to **{nickname}**", ephemeral=True)

    @card_group.command(name="bio", description="Set your card bio")
    async def bio(self, ctx, *, bio: str):
        await self.create_user_card(ctx.author.id)
        await self.update_user_card(ctx.author.id, bio=bio)
        await ctx.send(f"Your card's bio has been updated to: \n> {bio}", ephemeral=True)

    @card_group.command(name="age", description="Set your card age")
    async def age(self, ctx, age: int):
        if age < 13:
            await ctx.send(f"Hey pal, [**Discord TOS**](<https://discord.com/terms#2>) states you need to be **13 years or older** to use Discord, please log off and wait 'till you're older to use the application, thank you!", ephemeral=True)
            return
        else:
            await self.create_user_card(ctx.author.id)
            await self.update_user_card(ctx.author.id, age=age)
            await ctx.send(f"Your card's age has been updated to **{age}**!", ephemeral=True)

    @card_group.command(name="pronouns", description="Set your card pronouns")
    async def pronouns(self, ctx, *, pronouns: str):
        await self.create_user_card(ctx.author.id)
        await self.update_user_card(ctx.author.id, pronouns=pronouns)
        await ctx.send(f"You're cards pronouns have been updated to **{pronouns}**!", ephemeral=True)

    @card_group.command(name="birthday", description="Set your card birthday")
    async def birthday(self, ctx, month: int, day: int, year: int):
        await self.create_user_card(ctx.author.id)
        birthday = f"{month}/{day}/{year}"
        await self.update_user_card(ctx.author.id, birthday=birthday)
        await ctx.send(f"Your card's birthday has been updated to **{birthday}**!", ephemeral=True)

    @card_group.command(name="color", description="Set your card color")
    async def color(self, ctx, choice: str):
        choice = choice.lower()
        if choice in color_mapping:
            color = color_mapping[choice]
        elif re.match(r'^#?([0-9a-fA-F]{6})$', choice):
            if choice.startswith('#'):
                choice = choice[1:]
            color = int(choice, 16)
        else:
            await ctx.send("Invalid color choice. Use `cardcolorchoices` to see the available options.", ephemeral=True)
            return
        await self.set_user_card_color(ctx.author.id, color)
        await ctx.send(f"Your card color has been updated to `{choice}`!", ephemeral=True)

    @card_group.command(name="colorchoices", description="List available card color choices")
    async def colorchoices(self, ctx):
        e = discord.Embed(color=quake_color)
        e.set_author(name="Quake User Card Color Choices", icon_url=quake_logo)
        e.set_thumbnail(url=quake_logo)
        e.description = "# 🛍️ Available Color Choices 🛍️ \n> 🔴 Red \n> 🟠 Orange \n> 🟡 Yellow \n> 🟢 Green \n> 🔵 Blue \n> 🟣 Purple \n> 🌸 Pink \n> 🟤 Brown \n> ⚫️ Black \n> 🔘 Grey \n> ⚪️ White\n\n### 👾 Custom Colors 👾 \n> To set a custom color use a hex code (**Ex:** `#ff5733`)!"
        await ctx.send(embed=e, ephemeral=True)

    @card_group.command(name="show", description="Show a user's card")
    async def show(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        card = await self.get_user_card(user.id)
        if not card:
            await ctx.send(f"**{user.name}** doesn't have their card set!", ephemeral=True)
            return
        nickname, bio, age, pronouns, birthday, ideology, color = card[1:]
        e = discord.Embed(color=int(color, 16) if color else quake_color)
        e.set_author(name=f"{nickname or user.name}'s User Card", icon_url=user.avatar.url)
        e.set_thumbnail(url=user.avatar.url)
        e.add_field(name="📰 Bio", value=f"> {bio}" if bio else "> Not set", inline=False)
        e.add_field(name="📅 Age", value=f"{age}" if age else "Not set", inline=True)
        e.add_field(name="❤️ Pronouns", value=f"{pronouns}" if pronouns else "Not set", inline=True)
        e.add_field(name="🎂 Birthday", value=f"{birthday}" if birthday else "Not set", inline=True)
        await ctx.send(embed=e)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        afk_message, afk_timestamp = await self.get_afk(message.author.id)
        if afk_message:
            await self.remove_afk(message.author.id)
            await message.add_reaction("👋")
        for user in message.mentions:
            afk_message, afk_timestamp = await self.get_afk(user.id)
            if afk_message:
                nickname = user.display_name if user.display_name else user.name
                e = discord.Embed(color=quake_color)
                e.set_author(name=f"{nickname} is currently afk!", icon_url=user.avatar.url)
                e.set_thumbnail(url=user.avatar.url)
                e.description = f"> {afk_message}"
                if afk_timestamp:
                    afk_time = datetime.utcnow() - datetime.fromisoformat(afk_timestamp)
                    e.set_footer(text=f"AFK for {self.format_time_delta(afk_time)}")
                await message.channel.send(embed=e)

async def setup(bot):
    await bot.add_cog(MiscCog(bot))