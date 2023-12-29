import discord
import random
from random import randint
from discord.ext import commands
from discord.ui import View , Button , Select
from discord import Color, Embed, Interaction, app_commands, ButtonStyle
import json
from discord.ext.commands import cooldown, BucketType
from dispie import EmbedCreator
import wikipediaapi
import asyncio
from bs4 import BeautifulSoup
import requests

timers = {}
MEHR_NEWS_URL = 'https://www.mehrnews.com/rss'
mainShop = [{"name":"ELX","price":1000,"description":"Car"},
            {"name":"405-GLX","price":355,"description":"Car"},
            {"name":"GTR","price":1000000,"description":"Car"}]
token = ""
intents = discord.Intents.all()
PREFIX = "!"
bot = commands.Bot(command_prefix = PREFIX, intents=intents)


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59'}
wiki_wiki = wikipediaapi.Wikipedia('fa', headers=headers)
@bot.tree.command(name='wiki', description="daryaft etelaat az wikipedia")
@app_commands.describe(query = "yek nam ra vared konid")
async def wikipedia_search(interaction : discord.Interaction, *, query : str= None):
    page_py = wiki_wiki.page(query)
    if page_py.exists():
        await interaction.response.send_message(page_py.text[:2000])  # محدودیت طول پیام در دیسکورد
    else:
        await interaction.response.send_message("متاسفانه هیچ صفحه‌ای پیدا نشد.")


async def open_acc(user: discord.User):
    users = await get_pomes()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["Story"]= None
        
    with open("Poems.json", "w") as f:
        json.dump(users, f)
    return True


async def get_pomes():
    with open("Poems.json", "r") as f:
        users = json.load(f)
    return users
    

@bot.tree.command(name="random_story", description="ersal dastan random")
async def random_story_command(interaction : discord.Interaction) -> None:
  
    stories = []
  
    with open("Poems.json") as f:
        data = json.load(f)
    for item in data.values():
        stories.append(item["Story"])

  
    random_story = random.choice(stories)
    embed = discord.Embed(title="Random Story", color=discord.Color.yellow())
    embed.add_field(name="Random Story", value=random_story)
    embed.set_footer(text=f"requested by {interaction.user} | ", icon_url=interaction.user.avatar)
    embed.timestamp = interaction.created_at
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="sabt_dastan", description="sabt dastan khod")
@app_commands.checks.cooldown(1, 3600.0, key=lambda i: (i.guild_id, i.user.id))
async def sabt_dastan(interaction : discord.Interaction, *,dastan: str = None):
    await open_acc(interaction.user)
    users = await get_pomes()
    user = interaction.user
    if dastan == None:
        await interaction.response.send_message("lotfan dastan khod ra vared konid")
    else:
        users[str(user.id)]["Story"] = str(dastan)
        with open("Poems.json", "w") as f:
            json.dump(users, f)
        mbed = discord.Embed(title="✔️" , description="Dastan shoma ba movafaghiyat sabt shod" , color=discord.Color.yellow())
        mbed.set_thumbnail(url="https://dribbble.com/shots/1082594-Tick-GIF/attachments/8651840?mode=media")
        mbed.set_footer(text=f"requested by {interaction.user} | ", icon_url=interaction.user.avatar)
        mbed.timestamp = interaction.created_at
        await interaction.response.send_message(embed=mbed)



@sabt_dastan.error
async def on_test_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(str(error), ephemeral=True)


@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx: commands.Context, member: discord.Member, *, reason: str = "None"): 
    Ownembed = discord.Embed(title=f"User Kicked", description=f"**Kicked User Name** : `{member.display_name}`\n"
    f"**kicked By** : `{ctx.author.display_name}`\n"
    f"**Reason** : `{reason}`", color= discord.Color.yellow())
    await member.kick(reason=reason)
    await ctx.send(embed=Ownembed)

@bot.event
async def on_ready():
    activity = discord.Game(name=f"Nothing", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("bot ready")
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command")
    except Exception as e:
        print(e)


@bot.tree.command(name="help", description="help command")
async def help_1(interaction : discord.Interaction):
    mbed = discord.Embed(title="list dastorat bot", description="bot command", color=discord.Color.yellow())
    mbed.add_field(name="/ping", value="show bot ping", inline=False)
    mbed.add_field(name="/news", value="akhbar khabar gozari mehr")
    mbed.add_field(name="/wiki (chizi ke mikhay)", value="az wikipedia etelaat midi", inline=False)
    mbed.add_field(name="/avatar", value="avatar khdet va digaran", inline=False)
    mbed.add_field(name="/userinfo", value="etelaat member", inline=False)
    mbed.add_field(name="/serverinfo", value="etelaat server", inline=False)
    await interaction.response.send_message(embed=mbed)




@bot.tree.command(name="economy-help", description="help command economy")
async def help_2(interaction: discord.Interaction):
    mbed = discord.Embed(title="list dastorat economy bot", description="bot economy command", color=discord.Color.yellow())
    mbed.add_field(name="/sabt_dastan", value="dastan khodeton ro mitonid sabt konid", inline=False)
    mbed.add_field(name="/random_story", value="besorat random dastan hayi ke digaran sabt karadan ro mide", inline=False)
    mbed.add_field(name="/kar", value="kar kardan", inline=False)
    mbed.add_field(name="/balance", value="mizan pool shoma", inline=False)
    mbed.add_field(name="/dozdi", value="dozdi az gavsandogh", inline=False)
    mbed.add_field(name="/dozdiazmember", value="dozdi az member", inline=False)
    mbed.add_field(name="/withdraw", value="bardasht pool az bank", inline=False)
    mbed.add_field(name="/deposit", value="gozashtan pool dar bank", inline=False)
    mbed.add_field(name="/sendmoney", value="ersal pool be digaran", inline=False)
    mbed.add_field(name="/buy (esm item)", value="kharid item", inline=False)
    mbed.add_field(name="/bag", value="item hay shoma", inline=False)
    mbed.add_field(name="/shop", value="list item ha", inline=False)
    mbed.add_field(name="/slots", value="shart bandi", inline=False)

    await interaction.response.send_message(embed=mbed)






@bot.tree.command(name="ping", description="bot ping")
async def ping(interaction : discord.Interaction):
    await interaction.response.send_message(f"bot ping is {round(bot.latency* 1000)}ms")

@bot.event
async def on_message_delete(message):
    embed = discord.Embed(title="{} deleted a message".format(message.author.name),description="", color=0xFF0000)
    embed.add_field(name=message.content, value="This is the message that he has deleted",inline=True)
    channel = bot.get_channel(1145340270498549770)
    await channel.send(channel, embed=embed)




@bot.event
async def on_message_edit(message_before, message_after):
    embed = discord.Embed(title="{} edited a message".format(message_before.author.name),description="", color=0xFF0000)
    embed.add_field(name=message_before.content, value="This is the message before any edit",inline=True)
    embed.add_field(name=message_after.content, value="This is the message after the edit",inline=True)
    channel = bot.get_channel(1145340270498549770)
    await channel.send(channel, embed=embed)


@bot.tree.command(name="avatar", description="avatar member")
async def avatar(interaction : discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    embed = discord.Embed(title=f'{member.global_name}\'s Avatar', color=0x00ff00)
    embed.set_image(url=member.avatar)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="embed-gen")
@commands.has_permissions(administrator=True)
async def embed_creator(interaction : discord.Interaction):
    view = EmbedCreator(bot=bot)
    await interaction.response.send_message(embed=view.get_default_embed, view=view)

@embed_creator.error
async def mod_ban_error(error, ctx : commands.Context):
    if isinstance(error):
        await bot.send_message(ctx.message.channel, "Looks like you don't have the perm.")

@bot.tree.command(name="userinfo",description="etelaat member")
async def userinfo(interaction: discord.Interaction, member: discord.Member):
    roles = [role.name for role in member.roles]
    toprole = member.top_role.name
    embed = discord.Embed(title="userinfo", description=f"{member.mention} user info", color= discord.Color.random())
    embed.add_field(name="NICKNAME", value=member.display_name)
    embed.add_field(name="NAME", value=member.name)
    embed.add_field(name="ID", value=f"user id {member.id}")
    embed.add_field(name="STATUS", value=str(interaction.user.status))
    embed.add_field(name="ROLE" , value=", ".join(roles))
    embed.add_field(name="TOP ROLE", value=toprole)
    embed.add_field(name="JOIN", value=member.joined_at.strftime("%a, %B %#d, %Y, %I:%M %p"))
    embed.add_field(name="Created At", value=member.created_at.strftime("%a, %B %#d, %Y, %I:%M %p"))
    embed.add_field(name="bot?", value=member.bot)
    embed.set_footer(text=f"requested by {interaction.user}")
    embed.timestamp = interaction.created_at
    embed.set_thumbnail(url=member.avatar)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="say")
async def say(interaction : discord.Interaction):
    await interaction.response.send_message('hello')

@bot.tree.command(name="gaysanj", description='میزان گی بودن شما')
async def gaysanj(interaction : discord.Interaction):
    await interaction.response.send_message(f"شما {randint(0, 100)}% گی هستید")

@bot.tree.command(name="prosanj", description='میزان پرو بودن شما')
async def prosanj(interaction : discord.Interaction):
    await interaction.response.send_message(f"شما {randint(0, 100)}% پرو هستید")

@bot.tree.command(name="havalsanj", description='میزان هول بودن شما')
async def havalsanj(interaction : discord.Interaction):
    await interaction.response.send_message(f"شما {randint(0, 100)}% هول هستید")

@bot.tree.command(name="noobsanj",description='میزان نوب بودن شما')
async def noobsanj(interaction : discord.Interaction):
    await interaction.response.send_message(f"شما {randint(0, 100)}% نوب هستید")

@bot.tree.command(name="samsanj", description='میزان سم بودن شما')
async def samsanj(interaction : discord.Interaction):
    await interaction.response.send_message(f"شما {randint(0, 100)}% سم هستید")


@bot.tree.command(name="balance", description="میزان پول شما در بانک و کیف پول")
async def balance(interaction : discord.Interaction):
    await open_account(interaction.user)
    user = interaction.user
    users = await get_bank_data()
    wallet_amt = users[str(user.id)]["wallet"] 
    bank_amt = users[str(user.id)]["bank"] 
    em =  discord.Embed(title=f"{interaction.user.global_name} balance", color= discord.Color.red())
    em.add_field(name= "Wallet balance", value=wallet_amt)
    em.add_field(name= "bank balance", value=bank_amt)
    await interaction.response.send_message(embed=em)


@bot.event
async def on_member_join(member:discord.Member):
    channel = discord.utils.get(member.guild.channels, id=1143569538743533738)
    if channel is not None:
        await channel.send(f'Welcome {member.mention} to the server!')


@bot.tree.command(name = "dozdi", description = "dozdi az bank")
@app_commands.checks.cooldown(1, 600.0, key=lambda i: (i.guild_id, i.user.id))
async def dozdi(interaction):
    async def callback1(interaction : Interaction):
        if ramz == ramz1:
            pool = "500$"
            col = int("52ea6e", 16)
            embed = Embed(
                title = "",
                description = f"رمز گاوصندوق درست بود و {pool} گیرت اومد.|✅",
                color = Color(col)
            )
            await update_bank(user = interaction.user, change = 500)
            await interaction.response.edit_message(embed = embed, view = None)
        else:
            col = int("f75b2c", 16)
            embed = Embed(
                title = "",
                description = f"رمز گاوصندوق اشتباه بود و گوز گیرت نیومد|❌",
                color = Color(col)
            )
            await interaction.response.edit_message(embed = embed, view = None)
    async def callback2(interaction : Interaction):
        if ramz == ramz2:
            pool = "500$"
            col = int("52ea6e", 16)
            embed = Embed(
                title = "",
                description = f"رمز گاوصندوق درست بود و {pool} گیرت اومد. | ✅",
                color = Color(col)
            )
            await update_bank(user = interaction.user, change = 500)
            await interaction.response.edit_message(embed = embed, view = None)
        else:
            col = int("f75b2c", 16)
            embed = Embed(
                title = "",
                description = f"رمز گاوصندوق اشتباه بود و گوز گیرت نیومد | ❌",
                color = Color(col)
            )
            await interaction.response.edit_message(embed = embed, view = None)
    ramz1_ = random.randint(20, 90)
    ramz2_ = random.randint(50, 90)
    ramz1 = ramz1_ * ramz2_
    ramz2 = ramz1 + 1
    ramz_list = [ramz1, ramz2]
    ramz = random.choice(ramz_list)
    col = int("e02878", 16)
    embed = Embed(
        title = "",
        description = f"ده ثانیه وقت داری رمز گاوصندوق رو حل کنی\n| 🅱 **{ramz1_} × {ramz2_}**",
        color = Color(col)
    )
    embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/1094273639366537427/1169320613039575111/safe-icon2.jpg?ex=6554f9af&is=654284af&hm=260758c2cd53d47d2b7d6ba42e2a1f28c73e3c146874c2e03b553a20a26b8fc2&")
    button1 = Button(label = f"{ramz}", style = ButtonStyle.primary)
    if ramz == ramz1:
        button2 = Button(label = f"{ramz2}", style = ButtonStyle.primary)
    else:
        button2 = Button(label = f"{ramz1}", style = ButtonStyle.primary)
    view = View()
    view.add_item(button1)
    view.add_item(button2)
    button1.callback = callback1
    button2.callback = callback2
    await interaction.response.send_message(embed = embed, view = view)


@dozdi.error
async def on_test_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(str(error), ephemeral=True)

@bot.tree.command(name="kar", description="کار کردن و داشتن درآمد")
@app_commands.checks.cooldown(1, 3600.0, key=lambda i: (i.guild_id, i.user.id))
async def kar(interaction: discord.Interaction, esmkar : str = None):
    await open_account(interaction.user)
    users = await get_bank_data()
    user = interaction.user
    earnings = random.randrange(255)
    if esmkar == None:
        esmkar = "مفت خور"
    else:
        em = discord.Embed(title=f"{esmkar}", description=f"مبلغی که درآوردید {earnings} تومن است", color=discord.Color.random())
        await interaction.response.send_message(embed=em)

        users[str(user.id)]["wallet"] += earnings
        with open("RADIOACTIVE-BOT-SAVE.json", "w") as f:
            json.dump(users, f)


@kar.error
async def on_test_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(str(error), ephemeral=True)

@bot.tree.command(name="shop", description="شاپ")
async def shop(interaction : discord.Interaction):
    em = discord.Embed(title="$Shop$")

    for item in mainShop:
        name = item["name"]
        price = item["price"]
        des = item["description"]
        em.add_field(name=f"{name}", value=f"{price} | {name}")

    await interaction.response.send_message(embed=em)




@bot.tree.command(name="buy", description="خریدن آیتم")
@app_commands.describe(item = "item ro vared konid")
async def buy(interaction : discord.Interaction,item : str,amount : int = 1):
    await open_account(interaction.user)

    res = await buy_this(interaction.user,item,amount)

    if not res[0]:
        if res[1]==1:
            await interaction.response.send_message("آن شی وجود ندارد!")
            return
        if res[1]==2:
            await interaction.response.send_message(f"برای خرید {amount} {item} پول کافی در کیف پول خود ندارید")
            return


    await interaction.response.send_message(f"You just bought {amount} {item}")




@bot.tree.command(name="bag",description="آیتم هایی که شما دارید")
async def bag(interaction : discord.Interaction):
    await open_account(interaction.user)
    user = interaction.user
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    em = discord.Embed(title = "Bag", color=discord.Color.random())
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = name, value = amount)    

    await interaction.response.send_message(embed = em)   


@bot.tree.command(name="withdraw",description="bardashtan pool az bank")
@app_commands.describe(amount = "amount ro vared konid")
async def withdraw(interaction : discord.Interaction,amount :int = None):
    await open_account(interaction.user)
    if amount == None:
        await interaction.response.send_message("مقدار را وارد کنید")
        return

    bal = await update_bank(interaction.user)
    amount = int(amount)
    if amount>bal[1]:
        await interaction.response.send_message("به اندازه کافی پول ندارید")
        return
    if amount<0:
        await interaction.response.send_message("مقدار باید بیشتر باشد")
        return
    await update_bank(interaction.user, amount)
    await update_bank(interaction.user,-1* amount, "bank")
    embed = discord.Embed(title="bardasht pool az bank", description=f"میزان {amount} تومن پول برداشتی")
    embed.set_footer(text=f"requested by {interaction.user} | ", icon_url=interaction.user.avatar)
    embed.timestamp = interaction.created_at
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="deposit", description="gozashtan pool dar bank")
@app_commands.describe(amount = "amount ro vared konid")
@app_commands.checks.cooldown(1, 3600.0, key=lambda i: (i.guild_id, i.user.id))
async def deposit(interaction : discord.Interaction,amount :int = None):
    await open_account(interaction.user)
    if amount == None:
        await interaction.response.send_message("مقدار را وارد کنید")
        return

    bal = await update_bank(interaction.user)
    amount = int(amount)
    if amount>bal[0]:
        await interaction.response.send_message("به اندازه کافی پول نداری")
        return
    if amount<0:
        await interaction.response.send_message("مقدار باید بیشتر باشد")
        return
    await update_bank(interaction.user,-1* amount)
    await update_bank(interaction.user, amount, "bank")
    embed = discord.Embed(title="gozashtan pool dar bank", description=f"میزان {amount} تومن در بانک ریخیتد")
    embed.set_footer(text=f"requested by {interaction.user} | ", icon_url=interaction.user.avatar)
    embed.timestamp = interaction.created_at
    await interaction.response.send_message(embed=embed)


@deposit.error
async def on_test_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(str(error), ephemeral=True)


@bot.tree.command(name="sendmoney",description="ersal pool be digaran")
@app_commands.describe(amount = "amount ro vared konid")
@app_commands.checks.cooldown(1, 600.0, key=lambda i: (i.guild_id, i.user.id))
async def sendMoney(interaction : discord.Interaction,member : discord.Member,amount :int = None):
    await open_account(interaction.user)
    await open_account(member)

    if amount == None:
        await interaction.response.send_message("لطفا مقدار را وارد کنید")
        return

    bal = await update_bank(interaction.user)
    amount = int(amount)
    if amount>bal[1]:
        await interaction.response.send_message("به اندازه کافی پول نداری")
        return
    if amount<0:
        await interaction.response.send_message("مقدار باید بیشتر باشد")
        return
    await update_bank(interaction.user,-1* amount, "bank")
    await update_bank(member, amount, "bank")
    embed = discord.Embed(title="transfer", description=f"میزان {amount} تومن کمک کردی")
    embed.set_footer(text=f"requested by {interaction.user} | ", icon_url=interaction.user.avatar)
    embed.timestamp = interaction.created_at
    await interaction.response.send_message(embed=embed)

@sendMoney.error
async def on_test_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(str(error), ephemeral=True)
@bot.tree.command(name="dozdiazmember", description="dozdi az member")
async def dozdiAzMember(interaction : discord.Interaction,member : discord.Member):
    await open_account(interaction.user)
    await open_account(member)

    bal = await update_bank(member)
    
    if bal[0]<100:
        await interaction.response.send_message("ارزش نداره")
        return

    earnings = random.randrange(0 , bal[0])
    
    await update_bank(interaction.user, earnings)
    await update_bank(member, -1*earnings)
    embed = discord.Embed(title="dozdi az member", description=f"دزدی کردی و {earnings} پول گرفتی")
    embed.set_footer(text=f"requested by {interaction.user} | ", icon_url=interaction.user.avatar)
    embed.timestamp = interaction.created_at
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="slots", description="shart bandi")
@app_commands.describe(amount = "meghdar ro vared konid")
async def slots(interaction: discord.Interaction, amount : int= None):
    await open_account(interaction.user)
    if amount == None:
        await interaction.response.send_message("مقدار را وارد کنید")
        return

    bal = await update_bank(interaction.user)
    amount = int(amount)
    if amount>bal[0]:
        await interaction.response.send_message("شما انقدر پول ندارید!")
        return
    if amount<0:
        await interaction.response.send_message("مقدار باید بیشتر باشد!")
        return
    
    final = []
    for i in range(3):
        a = random.choice(["X","O","Q"])
        final.append(a)

    await interaction.response.send_message(str(final))
    if final [0] == final[1] or final [0] == final[2] or final [2] == final[1]:
        await update_bank(interaction.user,2*amount)
        await interaction.channel.send("هووورااا تو بردی")
    else:
        await update_bank(interaction.user,-1*amount)
        await interaction.channel.send("شانس با تو یار نبود")



async def open_account(user : discord.User):
    users = await get_bank_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("RADIOACTIVE-BOT-SAVE.json", "w") as f:
        json.dump(users,f)
    return True


async def get_bank_data():
    with open("RADIOACTIVE-BOT-SAVE.json", "r") as f:
        users = json.load(f)
    return users
    



async def update_bank(user: discord.User,change = 0,mode = "wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change
    with open ("RADIOACTIVE-BOT-SAVE.json","w") as f:
        json.dump(users,f)

    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
    return bal


async def buy_this(user: discord.User,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainShop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        

    with open("RADIOACTIVE-BOT-SAVE.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"wallet")

    return [True,"Worked"]


@bot.tree.command(name="server",description=' etelaat server')
async def serverinfo(interaction: discord.Interaction):
    server = interaction.guild
    embed = discord.Embed(title="serverinfo", description=f"{server.name} info", color= discord.Color.random())
    embed.add_field(name="NAME", value=server.name)
    embed.add_field(name="ID", value=f"{server.id}")
    embed.add_field(name="OWNER", value=f"{server.owner}")
    embed.add_field(name="Created At", value=server.created_at.strftime("%a, %B %#d, %Y, %I:%M %p"))
    embed.set_footer(text=f"requested by {interaction.user}")
    embed.set_thumbnail(url=server.icon)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="news", description="akhbar khabar gozari mehr")
@app_commands.checks.cooldown(1, 3600.0, key=lambda i: (i.guild_id, i.user.id))
async def news(interaction : discord.Interaction):
    response = requests.get(MEHR_NEWS_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

  
    titles = soup.find_all('title')[2:]
    links = soup.find_all('link')[2:]


    for title, link in zip(titles, links):
        title = title.get_text(strip=True)
        link = link.get_text(strip=True)

        embed = discord.Embed(title=title, url=link, color=discord.Color.random())
        await interaction.channel.typing()
        await asyncio.sleep(1.5)
        await interaction.channel.send(embed=embed)


@news.error
async def on_test_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(str(error), ephemeral=True)




@bot.command()
async def start_timer(ctx, timer_name: str, duration: int):
    if timer_name in timers:
        await ctx.send(f'Timer "{timer_name}" is already running.')
    else:
        timers[timer_name] = duration
        await ctx.send(f'Timer "{timer_name}" started for {duration} seconds.')

        await asyncio.sleep(duration)
        await ctx.send(f'Timer "{timer_name}" has ended.')

        del timers[timer_name]

@bot.command()
async def active_timers(ctx):
    if timers:
        active_timers_str = "\n".join([f'{timer}: {duration} seconds' for timer, duration in timers.items()])
        await ctx.send(f'Active Timers:\n{active_timers_str}')
    else:
        await ctx.send('No active timers.')






bot.run(token)