import discord
from discord.ext import commands
import datetime
import os

log_ch_id = os.environ["LOG_CHANNEL"]
hotclip_ch_id = os.environ["HOTCLIP_CHANNEL"]

# log_ch_id = 1073635083577196625
# hotclip_ch_id = 1056575267121930290

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


async def setup_hook():
    await bot.tree.sync()


@bot.event
async def on_ready():
    print("ready!")

    activity = discord.Game('감지')
    await bot.change_presence(status=discord.Status.online, activity=activity)


@bot.event
async def on_message_delete(message):
    content = message.content
    guild = message.guild
    author = message.author
    channel = message.channel
    print('Detect message delete')
    if 'http' in content:
        return
    logchannel = bot.get_channel(log_ch_id)  # log channel id

    n = datetime.datetime.now()
    time = f'{str(n.year)}년 {str(n.month)}월 {str(n.day)}일 {str(n.hour)}시 {str(n.minute)}분 {str(n.second)}초'
    task = discord.Embed(title=f"Delete", description=f"User : {author} Channel : {channel.mention}",
                         color=0xFF0000)
    task.add_field(name="Deleted Message", value=f"Contents : {content}", inline=False)
    task.set_footer(text=f"{guild.name}   |   {time}")
    await logchannel.send(embed=task)


@bot.event
async def on_message(message):
    content = message.content
    guild = message.guild
    author = message.author
    channel = message.channel
    embeds = message.embeds
    youtube = ['watch?v=', 'playlist?list=', 'https://www.youtu', '//youtu', 'ttps://youtu', 'om/shorts']

    if author.bot:
        return

    if content.startswith('!도움말') or content.startswith('!help'):
        print('도움말 호출!')
        # $help embed
        helpembed = discord.Embed(title='Welcome', color=0xFFBBC6)
        helpembed.set_author(name='kgh')
        helpembed.add_field(name='!help,!도움말', value='도움이 필요하면 불러봐요', inline=True)
        helpembed.add_field(name='다른 기능들', value='추후 업데이트 예정입니다', inline=True)
        await channel.send(embed=helpembed)

    if message.content == '이딴거 왜 만듦?':
        print('이걸 왜하냐고?')
        await channel.send(f'나도 몰라~~{message.author.mention}')
        await message.edit(content='ㅋㅋ루삥뽕')

    check = []
    if 'http' in content:
        print('http링크 추정 문자열 발견')
        for idx, val in enumerate(youtube):
            if val in content:
                print('유투브 링크가 맞는거 같아요!')
                check.append(idx)
        # print(len(check))
        if len(check) != 0:
            hotclip_channel = bot.get_channel(hotclip_ch_id)  # hotclip channel id
            # print(hotclip_channel)

            embed = discord.Embed(title=f'영상 링크가 [{message.guild.name}] 의 {channel} 에서 감지되었어요!',
                                  description='똑똑한 봇이 이동처리 할게요!', color=0x00A2F4)
            embed.add_field(name=f"영상 공유한 사람 : ", value=f"{author.nick}", inline=False)
            embed.add_field(name='', value=f"핫클립😝 채널에 가서 확인해봐요!  👉🏻 {bot.get_channel(hotclip_ch_id).mention}")
            # hotclip channel id

            # print(embed)
            after = f'{author.nick} 님이 공유해주신 영상이예요. \n {content}'
            # print(after)

            await message.channel.send(content='이 메시지는 유투브 링크이므로 봇이 이동처리 했어요!')
            await asyncio.sleep(1)
            await message.channel.send(embed=embed)
            await hotclip_channel.send(after)


@bot.command(name='ping')
async def ping(message):
    await message.channel.send('pong')

token = os.environ["BOT_TOKEN"]

bot.run(token)
