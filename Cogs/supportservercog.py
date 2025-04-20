import discord
from discord.ext import commands

quake_logo = "https://media.discordapp.net/attachments/1363337978742833409/1363342899474862233/QuakeLogo.png?ex=6805af84&is=68045e04&hm=d65ade377e31ed97126ff99ac7b7e693f63ead68d24e12903fcf7f1ad7905af0&=&format=webp&quality=lossless"
quake_color = 0x3fb7f0
owner_id = 532706491438727169
ssid = 1363337977459118280

class SupportServerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def postrules(self, ctx):
        if ctx.author.id == owner_id:
            e = discord.Embed(color=quake_color)
            e.set_thumbnail(url=quake_logo)
            e.set_author(name="Quake Information", icon_url=quake_logo)
            e.description = "# Quake Support Server Rules \n ### *STRIKE SYSTEM* \n> <:GreyTick:1363355146968367246> **10 Minute Mute:** No strike handed \n> :yellow_circle: **Strike 1:** 1 Hour Mute \n> :orange_circle: **Strike 2:** 24 Hour Mute \n> :red_circle: **Strike 3:** 1 Week Mute \n> <a:Alert:1363355200450203820>  **Final Strike:** Permanent Ban \n> **A third strike will result in a banning motion.** \n> **Depending on the severity of the offense, punishment will be up to Staff discretion.** \n ### *MUTE* \n> <a:Alert:1363355200450203820>  Aggressive arguing \n> <:GreyTick:1363355146968367246> Disrespecting **ANY** server member (ie personal attacks) \n ### *STRIKE 1* \n> :yellow_circle: Bullying/Harrassment \n> :yellow_circle: Spamming server members or members of the server staff \n> :yellow_circle: Bad faith arguing \n> :yellow_circle: Hasty generalizations of ideologies, groups of people, etc \n> :yellow_circle: Any form of microaggressions (severity of offense will depend on punishment) \n> :yellow_circle: Pointless pinging of moderators \n> :yellow_circle: NSFW conversations outside of appropriate channels. \n ### *STRIKE 2* \n> :orange_circle: Calls for violence/Fetishizing violence \n> :orange_circle: Telling someone to kill themselves \n> :orange_circle: Sexual discussion in general channels (outside of the mature channel) \n> :orange_circle: Inciting Infighting \n ### *STRIKE 3* \n> :red_circle: Extreme trolling (i.e. roleplaying as a Nazi) \n> :red_circle: Joking/accusing pedophilia in any form **WITHOUT PROOF** \n> :red_circle: Engaging in E-Sex \n> :red_circle: Minors having 18+ role and/or being in the adult corner category \n ### *IMMEDIATE BAN* \n> <a:Alert:1363355200450203820> Being a Nazi \n> <a:Alert:1363355200450203820> Malicious Bigotry \n> <a:Alert:1363355200450203820> Pedophilia of any form \n> <a:Alert:1363355200450203820> Minors soliciting Adults \n> <a:Alert:1363355200450203820> Posting Pornography in the server \n ### *SERVER GUIDELINES* \n> :green_circle: Abide by [**Discord ToS**](https://discord.com/terms) and [**Guidelines**](https://discord.com/guidelines) at all times \n> :green_circle: Do not DM other members without permission \n> :green_circle: If making a complaint about someone in the server, link messages and provide screenshots \n> :green_circle: Be respectful to other members whether or not you agree with them \n> :green_circle: Remember to practice Minor Safety within the server \n> :green_circle: Use appropriate tone indicators in discussions \n> :green_circle: Users reserve the right to request the transcript to any ticket they are a part of \n> :green_circle: Good luck, and have fun! \n \n *If you have any questions, comments or concerns please let a Staff member know! Thank you!*"
            await ctx.send(embed=e)
        else:
            return

    @commands.command()
    async def postgi(self, ctx):
        if ctx.author.id == owner_id:
            e = discord.Embed(color=quake_color)
            e.description = "# General Information \n This is an explanation of terms with various examples. \n\n **Microaggressions:** *Insulting, offensive or invalidating behavior which may seem well intentioned or innocuous but happens everyday to marginalized people, and become heavy and frustrating.* \n\n**Examples of 'microaggressions' can look like:** \n> ⚠️ Repeated 'mistakes' (Ex: consistently misgendering someone as a mistake without putting the effort in to change the behavior). \n> ⚠️ Unchallenged biases (Ex: Never caring to notice the lack of access to bathrooms for disabled folks, because the person is able-bodied themselves and does not challenge their privilege). \n> ⚠️ Backhanded compliments (Ex: “Your English is so good” to a person of color, immigrant or not). \n> ⚠️ Insensitive questions (Ex: Asking a trans person if they got “the surgery”). \n> ⚠️ Denial of individual bigotry, either because of connections or experiences (Ex: “I have a gay friend, im not homophobic!” or “I’m a woman, so I really know what you go through as a person of color!”). \n> ⚠️ Certain looks or behaviors (Ex: Judgemental looks, clutching your bag, moving away from the person or following them in a store…). \n\n**Bad Faith Arguing:** *Arguing in bad faith means that you are not being honest, respectful and/or genuine in the discussion. This could be considered as “arguing to win”, not to learn and expand your knowledge and points of view.* \n\n**Examples of 'bad faith arguing' can look like:** \n> ⚠️ Leaving out some crucial information as to mislead others and make your argument seem more plausible. \n> ⚠️ Employing logical fallacies, nitpicking, whataboutism, etc. \n> ⚠️ Not actually listening to your opponent, simply waiting for them to finish talking so you can counter. \n > ⚠️ Refusing to ever concede arguments, or to be nuanced in their position (can be spotted with an over usage of “agree to disagree”). \n> ⚠️ Attacking the other person instead of the argument itself."
            await ctx.send(embed=e)
        else:
            return

    @commands.command()
    async def postreqs(self, ctx):
        if ctx.author.id == owner_id:
            e = discord.Embed(color=quake_color)
            e.set_thumbnail(url=quake_logo)
            e.description = "# *Looking to join the team?* \n Before you open a ticket and apply for the **Quake Staff Team**, make sure you meet our requirements! \n\n### Quake Staff Requirements \n> 👴 **Must be 18+ IRL** \n> ⏳ **Have been in the server for 1 Month or more** \n> **📈 Have been active in the server during that time** \n> 🎖 **Level 5 or higher on** <@437808476106784770> \n\n*These are non-negotiable.*"
            await ctx.send(embed=e)
        else:
            return

    @commands.command()
    async def postpartner(self, ctx):
        if ctx.author.id == owner_id:
            e = discord.Embed(color=quake_color)
            e.set_thumbnail(url=quake_logo)
            e.description = "# *Want to become a Partner?* \n Before you open a ticket to become a partner and get <@&1363337977475891277>, make sure you qualify! \n\n### Partnership Requirements \n> - Server has 25+ Members (Non-Bots) \n> - SFW server/bot \n> - Server Rep must stay in **Quake Support** \n> - Server must add **Quake** (negotiable)"
            await ctx.send(embed=e)
        else:
            return

    @commands.command()
    async def postroles(self, ctx):
        if ctx.author.id == owner_id:
            e = discord.Embed(color=quake_color)
            e.set_author(name="Quake Roles", icon_url=quake_logo)
            e.description = "Choose your role color! \n\n> 🔴 <@&1363337977488736314> \n> 🔵 <@&1363337977488736313> \n> 🟢 <@&1363337977488736312> \n> 🟡 <@&1363337977488736311> \n> 🌸 <@&1363337977488736310> \n> 🟣 <@&1363337977488736309> \n> 🟠 <@&1363337977488736308> \n> 🟤 <@&1363337977488736307> \n> 🔘 <@&1363337977488736306> \n> ⚫️ <@&1363337977475891279>"
            view = discord.ui.View()
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, label="🔴", custom_id="red"))
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, label="🔵", custom_id="blue"))
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, label="🟢", custom_id="green"))
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, label="🟡", custom_id="yellow"))
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, label="🌸", custom_id="pink"))
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, label="🟣", custom_id="purple"))
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, label="🟠", custom_id="orange"))
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, label="🟤", custom_id="brown"))
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, label="🔘", custom_id="gray"))
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, label="⚫️", custom_id="black"))
            await ctx.send(embed=e, view=view)
        else:
            return

    @commands.command()
    async def postping(self, ctx):
        if ctx.author.id == owner_id:
            e = discord.Embed(color=quake_color)
            e.set_author(name="Quake Roles", icon_url=quake_logo)
            e.description = "Choose a role to get pinged when things occur! \n\n> 🔔 <@&1363337977475891273> \n> 🛑 <@&1363337977475891271> \n> 📊 <@&1363337977475891272>"
            view = discord.ui.View()
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, label="🔔", custom_id="updatepings"))
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, label="🛑", custom_id="statuspings"))
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.secondary, label="📊", custom_id="pollpings"))
            await ctx.send(embed=e, view=view)
        else:
            return

    added_embed = discord.Embed(color=quake_color)
    added_embed.title = "✅ Role Added ✅"
    added_embed.description = "The role has been added!"

    removed_embed = discord.Embed(color=quake_color)
    removed_embed.title = "❌ Role Removed ❌"
    removed_embed.description = "The role has been removed!"
    
    role_mappings = {
        'red': 'Red',
        'blue': 'Blue',
        'green': 'Green',
        'yellow': 'Yellow',
        'pink': 'Pink',
        'purple': 'Purple',
        'orange': 'Orange',
        'brown': 'Brown',
        'gray': 'Gray',
        'black': 'Black',
        'updatepings': 'Update Pings',
        'statuspings': 'Status Pings',
        'pollpings': 'Poll Pings'
    }
    
    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        try:
            if interaction.guild.id == ssid:
                if interaction.type == discord.InteractionType.component:
                    custom_id = interaction.data['custom_id']
                    role_name = self.role_mappings.get(custom_id)
                    if role_name:
                        role = discord.utils.get(interaction.guild.roles, name=role_name)
                        if role in interaction.user.roles:
                            await interaction.user.remove_roles(role)
                            await interaction.response.send_message(embed=self.removed_embed, ephemeral=True)
                        else:
                            await interaction.user.add_roles(role)
                            await interaction.response.send_message(embed=self.added_embed, ephemeral=True)
            else:
                return
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_member_join(self, member, ctx):
        try:
            member_role = discord.utils.get(member.guild.roles, name="💮 Member")
            await member.add_roles(member_role)
        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(SupportServerCog(bot))

