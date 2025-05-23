# 📋 Command List
This is a list of all **Quake** commands, a description, their usage, and the minimum role required to use them.

The "role required" in the tables below shows the lowest role required to ***use*** the command, for example, if it lists "Member" as the **Role Required**, then everyone with "Member" role and above (Helpers, Moderators and Admins) can use the role.

By default commands are slash commands, and use `!`. You can customize this using `/setprefix`.

**Command Count:** `116`

## ⚖️ Roles

| Role Name |
|-----------|
| Admin     |
| Moderator |
| Helper    |
| Member    |

## 📌 General
Command | Description | Usage | Role Required
--- | --- | --- | ---
help | Public help menu displaying commands | `help` | Member
info | Shows information about **Quake** and your server | `info` | Member
about | Shows more information about **Quake** | `about` | Member
setup | Shows a user how to setup **Quake** | `setup` | Moderator
vote | Sends **Quake's** voting links | `vote` | Member
ping | Shows a users ping | `ping` | Member
suggest | Lets users make a suggestion for the server | `suggest <suggestion>` | Member
poll | Creates a poll | `poll <question> <option1> <option2> <option3> <option4> <option5>` | Moderator
review | Sends a review of Quake into the "reviews" channel in Quake Support | `review <stars> <review>` | Member
invite | Sends the link to add **Quake**, the support server, and the GitHub | `invite` | Member

## 🎉 Fun
Command | Description | Usage | Role Required
--- | --- | --- | ---
coinflip | Flips a coin | `coinflip` | Member
ask | Gives an answer to your question | `ask` | Member
reverse | Reverses a users text | `reverse <text>` | Member
say | Says the users input text | `say <text>` | Member
lovetest | Gives a love percentage between two users | `lovetest <user1> <user2>` | Member
cute | Sends a picture of a cute animal | `cute` | Member

## 🎯 Action
Command | Description | Usage | Role Required
--- | --- | --- | ---
highfive | Highfives another user | `highfive @user` | Member
poke | Pokes another user | `poke @user` | Member
pat | Pats another user | `pat @user` | Member
hug | Hugs another user | `hug @user` | Member
kiss | Kisses another user | `kiss @user` | Member
cuddle | Cuddles another user | `cuddle @user` | Member
bite | Bites another user | `bite @user` | Member
bonk | Bonks another user | `bonk @user` | Member
slap | Slaps another user | `slap @user` | Member
punch | Punches another user | `punch @user` | Member
throw | Throws another user off a cliff | `throw @user` | Member
punt | Punts another user | `punt @user` | Member

## 🧮 Misc
Command | Description | Usage | Role Required
--- | --- | --- | ---
whois | Sends information about a user's account | `whois @user` | Member
avatar | Sends a users profile picture | `avatar @user` | Member
snipe | Shows a recently deleted message and who sent it | `snipe` | Member
remind | Sets a reminder for a user about a task | `remind <number><abbreviated time length> <task>` | Member
remindlist | Shows a users reminder list | `remindlist` | Member
afk | Sets a user into "AFK Mode" | `afk <message>` | Member
card | Shows a user's user card | `card @user` | Member
cardnickname | Sets a user's nickname on their user card | `cardnickname <nickname>` | Member
cardbio | Sets a user's bio on their user card | `cardbio <bio>` | Member
cardage | Sets a user's age on their user card | `cardage <age>` | Member
cardpronouns | Sets a user's pronouns on their user card | `cardpronouns <pronouns>` | Member
cardbirthday | Sets a user's birthday on their user card | `cardbirthday <month> <day> <year>` | Member
cardcolor | Sets a user's user card embed color | `cardcolor <choice>` | Member
cardcolorchoices | Shows the color choices for user cards | `cardcolorchoices` | Member
todoadd | Adds a task to a user's "todo list" | `todoadd <task>` | Member
tododel | Removes a task from a user's "todo list" | `tdoodel <task number>` | Member
todolist | Shows a user's "todo list" | `todolist` | Member
todoclear | Clears a user's "todo list" | `todoclear` | Member
giveaway | Starts a giveaway | `giveaway <time> <winners> <prize>` | Moderator
reroll | Rerolls the giveaway | `reroll` | Moderator
emojisteal | Grabs and sends the file link from a custom emoji | `emojisteal :emoji:` | Member
emojiadd | Adds an emoji to the server | `emojiadd <name>` | Admin
emojidel | Deletes an emoji from the server | `emojidel <name> <id>` | Admin
emojiinfo | Sends information about an emoji | `emojiinfo <name> <id>` | Member
emojirename | Renames an emoji | `emojirename <id> <new_name>` | Admin
stickersteal | Grabs and sends the file link from a sticker | `stickersteal` | Member
stickeradd | Adds a sticker to the server | `stickeradd` | Admin
stickerdel | Deletes a sticker from the server | `stickerdel <name> <id>` | Admin
stickerinfo | Shows information about a sticker | `stickerinfo <name> <id>` | Member
stickerrename | Renames a sticker | `stickerrename <id> <new_name>` | Admin
menuhelp | Sends the Menu Help menu | `menuhelp` | Admin
menuinfo | Sends information about a self role menu | `menuinfo <identifier>` | Admin
menucreate | Creates a self role menu | `menucreate` | Admin
menusend | Sends a self role menu | `menusend <menu_id>` | Admin
menuedit | Edits a self role menu | `menu edit <menu_id>` | Admin

## 🔰 Staff
Command | Description | Usage | Role Required
--- | --- | --- | ---
purge | Mass deletes messages | `purge <number of messages>` | Admin
ban | Bans a user from the server | `ban @user` | Moderator
unban | Unbans a user from the server | `unban @user` | Admin
kick | Kicks a user from the server | `kick @user` | Helper
mute | Puts a user in "timeout" | `gulag @user <number><abbreviated time length> <reason>` | Helper
unmute | Removes a user from "timeout" `ungulag @user <reason>` | Helper
warn | Warns a user | `warn @user <reason>` | Helper
warnlist | Checks the warns of a user | `warnlist @user` | Helper
delwarn | Deletes a specified warn from a users warn list | `delwarn @user <warn number>` | Admin
clearwarns | Clears all a user's warns | `clearwarns @user` | Admin
highlighthelp | Sends the Highlight Help Menu | `highlighthelp` | Helper
higlightshow | Shows a user's highlight menu | `highlightshow` | Helper
highlightadd | Adds a word to a moderator's highlight list | `highlightadd <word>` | Helper
hightlightremove | Removes a word from a moderator's highlight list | `highlightremove <word>` | Helper
highlightclear | Clears a moderator's word highlight list | `highlightclear` | Helper
highlightblock | Blocks a user or channel on a moderator's highlight list | `highlightblock @user` / `highlightblock #channel` | Helper
highllightunblock | Unblocks a user or channel from a moderator's highlight list | `highlightunblock @user` / `highlightunblock #channel` | Helper
highlightdefaults | Adds a default list of slurs to a moderator's highlight list | `highlightdefaults` | Helper
highlightignore | Adds a word to a moderator's ignore list | `highlightignore <word>` | Helper
highlightunignore | Removes a word from a moderator's ignore list | `highlightunignore <word>` | Helper

## ⚙️ Config
Command | Description | Usage | Role Required
--- | --- | --- | ---
configs | Sends the Config Menu for a server | `configs` | Admin
togglelog | Toggles the logging feature for a server | `togglelog` | Admin
togglesuggest | Toggles the suggestion feature for a server | `togglesuggest` | Admin
togglestar | Toggles the starboard feature for a server | `togglestar` | Admin
togglewelcome | Toggles the welcome message feature for a server | `togglewelcome` | Admin
toggleleave | Toggles the leave message feature for a server | `toggleleave` | Admin
toggleboost | Toggles the boost message feature for a server | `toggleboost` | Admin
toggleautorole | Toggles the auto role feature for a server | `toggleautorole` | Admin
togglefilter | Toggles the chat filter feature for a server | `togglefilter` | Admin
setprefix | Sets server prefix | `setprefix <prefix>` | Admin
setlog | Sets server logging channel | `setlog` | Admin
setstaff | Sets the staff roles for a server | `setstaff` | Admin
setsuggest | Sets server suggestion channel | `setsuggest` | Admin
setstar | Sets server starboard channel | `setstar` | Admin
setwelcome | Sets the welcome message for a server | `setwelcome` | Admin
setleave | Sets the leave message for a server | `setleave` | Admin
setboost | Sets the boost message for a server | `setboost` | Admin
setautorole | Sets the auto roles for a server | `setautorole` | Admin
filterhelp | Shows the Filter Help Menu | `filterhelp` | Admin
filtershow | Shows the server's chat filter information | `filtershow` | Admin
filterdefaults | Adds a default list of slurs to a servers chat filter | `filterdefaults` | Admin
filteradd | Adds a word to a servers chat filter | `filteradd <word>` | Admin
filterremove | Removes a word from a servers chat filter | `filterremove <word>` | Admin
filterignore | Adds a word to a servers chat filter ignore list | `filterignore <word>` | Admin
filterunignore | Removes a word from a servers chat filter ignore list | `filterunignore <word>` | Admin
filterblock | Blocks a user, channel or role from a servers chat filter | `filterblock <user> <role> <channel> <category_id>` | Admin
filterunblock | Unblocks a user, channel or role from a servers chat filter | `filterunblock <user> <role> <channel> <category_id>` | Admin
filterclear | Clears a servers chat filter list | `filterclear` | Admin
testwelcome | Sends the welcome message for a server | `testwelcome` | Admin
testleave | Sends the leave message for a server | `testleave` | Admin
testboost | Sends the boost embed for a server | `testboost` | Admin
