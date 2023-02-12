import discord
from discord.ext import commands
import datetime
import os
import asyncio

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)


# class nametag:
#
#     def __init__(self, tagname, tagid):
#         self.tagname = tagname
#         self.tagid = tagid


hotclip_id: int = None
log_id: int = None
command_id: int = None

default_delay = 10
move_delay: int = None
delay_set_ch: str = None
delay_set_ch_id: int = None


async def setup_hook():
    await bot.tree.sync()


@bot.event
async def on_ready():

    for guilds in bot.guilds:  # 서버확인
        print(f"서버 이름 : {guilds.name} , 서버 id : {guilds.id }")
    activity = discord.Game('감지')

    # bot.remove_command('help')
    # print('기본제공 help 삭제')
    # all_channel = bot.get_all_channels()
    # # print('all_channel   ----  ', all_channel)
    # for ch in all_channel:
    #     # print(f"채널명 : {ch.name} , 채널 id : {ch.id}")
    #     if '핫클립' in ch.name:
    #         hotclip_id = ch.id
    #     if 'log' in ch.name or '로그' in ch.name or 'Log' in ch.name:
    #         log_id = ch.id
    print("ready! ,set status , activity")
    await bot.change_presence(status=discord.Status.online, activity=activity)


@bot.command(aliases=['딜레이', 'd', 'D'])
async def delay(ctx, context: int):
    global move_delay
    global delay_set_ch
    global delay_set_ch_id
    global default_delay

    if context is None:
        move_delay = default_delay

    move_delay = context * 60
    all_channel = bot.get_all_channels()
    for ch in all_channel:
        if 'log' in ch.name or '로그' in ch.name or 'Log' in ch.name:
            if ctx.guild.name == ch.guild.name:
                delay_set_ch = ch.name
                delay_set_ch_id = ch.id
                # print(delay_set_ch )
                # print(delay_set_ch_id)
    c = move_delay // 60  # 출력용
    await ctx.send(f" {ctx.author.mention}님이 영상링크 이동딜레이를 {c}분으로 설정하였습니다.")


@bot.command(aliases=['help', '도움말'])
async def contacthelp(ctx):
    try:
        print('도움말 호출!')
        # $help embed
        helpembed = discord.Embed(title='Welcome', color=0xFFBBC6)
        helpembed.set_author(name='kgh')
        helpembed.add_field(name='!help, !도움말', value='딜레이 설정 : !딜레이 , !delay , !d, !D', inline=False)
        helpembed.add_field(name='기본설정 딜레이', value='10분이예요!', inline=False)
        helpembed.add_field(name='다른 기능들은', value='추후 업데이트 예정입니다', inline=False)
        await ctx.send(embed=helpembed)
        await bot.process_commands(ctx)

    except discord.ext.commands.errors.CommandInvokeError:
        pass


@bot.event
async def on_message_delete(message):
    global hotclip_id
    global log_id
    global command_id
    #  for guilds in bot.guilds:  # 서버확인
    #  print(f"서버 이름 : {guilds.name} , 서버 id : {guilds.id }")
    content = message.content
    guild = message.guild
    author = message.author
    channel = message.channel
    await bot.process_commands(message)

    print('Detect message delete')
    all_channel = bot.get_all_channels()
    for ch in all_channel:
        if 'log' in ch.name or '로그' in ch.name or 'Log' in ch.name:
            if message.guild.name == ch.guild.name:
                log_id = ch.id

    if 'http' in content:
        await bot.process_commands(message)
        return

    logchannel = bot.get_channel(log_id)

    n = datetime.datetime.now()
    time = f'{str(n.year)}년 {str(n.month)}월 {str(n.day)}일 {str(n.hour)}시 {str(n.minute)}분 {str(n.second)}초'
    task = discord.Embed(title=f"Delete", description=f"User : {author} Channel : {channel.mention}",
                         color=0xFF0000)
    task.add_field(name="Deleted Message", value=f"Contents : {content}", inline=False)
    task.set_footer(text=f"{guild.name}   |   {time}")
    await logchannel.send(embed=task)
    await bot.process_commands(message)


@bot.event
async def on_message(message):
    global hotclip_id
    global log_id
    global command_id
    global delay_set_ch
    global delay_set_ch_id
    global move_delay
    global default_delay

    if move_delay is None:
        move_delay = default_delay * 60

    print(f"딜레이 세팅 채널은 {delay_set_ch} 입니다")
    print(f"딜레이 세팅 채널id는 {delay_set_ch_id} 입니다")
    print(f"현재 설정 딜레이는 {move_delay} 입니다 \n")

    await bot.process_commands(message)

    all_channel = bot.get_all_channels()
    for ch in all_channel:
        if '핫클립' in ch.name:
            if message.guild.name == ch.guild.name:
                hotclip_id = ch.id

        elif 'log' in ch.name or '로그' in ch.name or 'Log' in ch.name:
            if message.guild.name == ch.guild.name:
                log_id = ch.id

        elif '커맨드' in ch.name:
            if message.guild.name == ch.guild.name:
                command_id = ch.id

            else:
                command_id = log_id

    # print(myChannelInfo)
    # print(myDelaySet)

    content = message.content
    guild = message.guild
    author = message.author
    channel = message.channel
    embeds = message.embeds
    youtube = ['watch?v=', 'playlist?list=', 'https://www.youtu', '//youtu', 'ttps://youtu', 'om/shorts']

    if author.bot:
        return

    if message.content == '이딴거 왜 만듦?':
        print('이걸 왜하냐고?')
        await channel.send(f'나도 몰라~~{message.author.mention}')
        await bot.process_commands(message)

    check = []
    if 'http' in content:
        if content.startswith('+'):
            return

        # print(message.channel.id)
        # print(f"메시지 채널 타입{type(message.channel)} , 핫클립 채널id 타입 {type(hotclip_id)}")

        if message.channel != hotclip_id and message.channel != command_id:
            print('http링크 추정 문자열 발견')
            for idx, val in enumerate(youtube):
                if val in content:
                    print('유투브 링크가 맞는거 같아요!')
                    check.append(idx)

        # print(len(check))
        if len(check) != 0:
            if message.channel.id == hotclip_id:
                return
            hotclip_channel = bot.get_channel(hotclip_id)  # hotclip channel id
            # print(hotclip_channel)

            embed = discord.Embed(title=f'영상 링크가 [{message.guild.name}] 의 {channel} 에서 감지되었어요!',
                                  description='똑똑한 봇이 이동처리 할게요!', color=0x00A2F4)
            embed.add_field(name=f"영상 공유한 사람 : ", value=f"{author.nick}", inline=False)
            embed.add_field(name='', value=f"핫클립😝 채널에 가서 확인해봐요!  👉🏻 {hotclip_channel.mention}")
            # hotclip channel id

            n = datetime.datetime.now()
            time = f'{str(n.year)}년 {str(n.month)}월 {str(n.day)}일 {str(n.hour)}시 {str(n.minute)}분 {str(n.second)}초'
            after = f'{author.nick} 님이 \n{time}에 공유해주신 영상이예요. \n {content}'
            # print(after)
            await asyncio.sleep(move_delay)
            await message.delete()
            await message.channel.send(content='이 메시지는 유투브 링크이므로 봇이 이동처리 했어요!')
            await message.channel.send(embed=embed)
            await hotclip_channel.send(after)
            await bot.process_commands(message)


@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('pong')
    await bot.process_commands(ctx)

token = os.environ["BOT_TOKEN"]

bot.run(token)
