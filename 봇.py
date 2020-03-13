# imports
import asyncio
import discord
from discord.ext import commands
from discord.utils import get
import glob
import random
import time
import datetime

app = commands.Bot(command_prefix='#')

token = "Njg2NjM2MDAxNzI4NTI4NDg2.XmaxdQ.Sp4dWJcmjROOctYjg12z-Xn1f-s"
calcResult = 0

# normal functions
def setEmbed(Title, Footer, Description, Color, Inline, Thumbnail, **kwargs):
    embed = discord.Embed(title=Title, description=Description, color=Color)
    count = 0
    if Thumbnail != None:
        embed.set_thumbnail(url=Thumbnail)
    for x in kwargs.keys():
        temp = x.split("_")
        embed.add_field(name=" ".join(temp), value=kwargs[x], inline=Inline[count])
        count+=1
    embed.set_footer(text=Footer)
    return embed

def find(filename, directory):
    found = 0
    files = glob.glob(directory+"**")
    for i in range(len(files)):
        if files[i] == directory+filename:
            return True
    if found == 0:
        return False

# discord settings
@app.event
async def on_ready():
    print("다음으로 로그인합니다 : ")
    print(app.user.name)
    print(app.user.id)
    print("==========")
    game = discord.Game("토봇명령어 <- 명령어 도움말")
    await app.change_presence(status=discord.Status.online, activity=game)

# discord commands
@app.command(name="추방", pass_context=True)
@commands.has_any_role("Commander","NA","supporter","administrator","police","manager")
@commands.has_permissions(administrator=True)
async def _kick(ctx, *, user_name: discord.Member, reason=None):
    await user_name.kick(reason=reason)
    await ctx.send(str(user_name)+"을(를) 추방하였습니다.")

@_kick.error
async def _kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        print("Error1")
        await ctx.send("{}님, 당신은 이 명령을 실행하실 권한이 없습니다.".format(ctx.message.author))
    
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("유저를 넣지 않으셨습니다.")
    if isinstance(error, commands.BadArgument):
        await ctx.send("유저를 넣어주세요.")

@app.command(pass_context=True)
async def logout(ctx):
    await app.logout()
@app.command(name="밴니", pass_context=True)
@commands.has_any_role("Commander")
async def _ban(ctx, *, user_name: discord.Member):
    await user_name.ban()
    await ctx.send(str(user_name)+"을(를) 영원히 매장시켰습니다.")

@app.command(name="언밴", pass_context=True)
async def _unban(ctx, *, user_name):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = user_name.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention}을(를) 회생시켰습니다.")
            return

@app.command(name="청소", pass_context=True)
@commands.has_any_role("Commander","NA","supporter","administrator","police","manager")
async def _clear(ctx, *, amount=5):
    await ctx.channel.purge(limit=amount+1)

@app.command(name="mem", pass_context=True)
@commands.has_any_role("Commander","NA","supporter","administrator","police","manager")
async def _MembersRole(ctx, user_name: discord.Member=None):
    user_name = user_name or ctx.message.author
    id = str(user_name).split("#")
    mem_user = get(ctx.guild.members, name=id[0])
    await user_name.add_roles(get(ctx.guild.roles, name="Members"))
    await ctx.send("> ["+str(mem_user.mention)+"] 님에게 [Members] 역할이 적용되었습니다!")
    
@app.command(name="fam", pass_context=True)
@commands.has_any_role("Commander","NA","supporter","administrator","police","manager")
async def _FamilysRole(ctx, user_name: discord.Member=None):
    user_name = user_name or ctx.message.author
    id = str(user_name).split("#")
    fam_user = get(ctx.guild.members, name=id[0])
    await user_name.add_roles(get(ctx.guild.roles, name="Family"))
    await ctx.send("> ["+str(fam_user.mention)+"] 님에게 [Family] 역할이 적용되었습니다!")
    
@app.command(name="뮤트", pass_context=True)
@commands.has_any_role("Commander","NA","supporter","administrator","police","manager")
async def _mute(ctx, user_name: discord.Member=None):
    user_name = user_name or ctx.message.author
    id = str(user_name).split("#")
    mute_user = get(ctx.guild.members, name=id[0])
    await user_name.add_roles(get(ctx.guild.roles, name="경고"))
    await ctx.send("> ["+str(mute_user.mention)+"] 님에게 [경고] 역할이 적용되었습니다!")

@app.command(name="언뮤트", pass_context=True)
@commands.has_any_role("Commander","NA","supporter","administrator","police","manager")
async def _unmute(ctx, user_name: discord.Member=None):
    user_name = user_name or ctx.message.author
    id = str(user_name).split("#")
    unmute_user = get(ctx.guild.members, name=id[0])
    await user_name.remove_roles(get(ctx.guild.roles, name='경고'))
    await ctx.send("> ["+str(unmute_user.mention)+"] 님에게 [경고] 역할이 삭제되었습니다!")

@app.command(pass_context=True)
async def randomNum(ctx, num1, num2):
    picked = random.randint(int(num1), int(num2))
    await ctx.send('뽑힌 숫자는 : '+str(picked))
          
@app.command(name="밴", pass_context=True)
@commands.has_any_role("Commander","NA","supporter","administrator","police","manager")
async def _ban(ctx, user_name: discord.Member, reason="사유 없음", reason2="아이디 없음", amount=1):
    id1 = str(user_name).split("#")
    id2 = str(ctx.message.author).split("#")
    banned_user = get(ctx.guild.members, name=id1[0])
    complete_user = get(ctx.guild.members, name=id2[0])
    embed = setEmbed(Title="대 상", Footer="", Description=""+ banned_user.mention,
    Color=0xD873F1, Inline=[True, True, True], Thumbnail=None, 처리한_관리자=complete_user.mention, 사유=reason, 서버_닉네임=reason2)
    embed.set_thumbnail(url=str(user_name.avatar_url))
    embed.set_author(name="영구 추방(Ban)", icon_url="https://i.imgur.com/8U9ayci.jpg")
    embed.set_footer(text = "| KaKao Battle Ground Adult Only | ⓒ 2020.토토로 All rights reserved. |", icon_url="https://i.imgur.com/ZdoUTX4.png")
    await ctx.channel.purge(limit=1)
    await ctx.send(embed=embed)
    await user_name.ban()

@_ban.error
async def _ban_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("{}님, 당신은 이 명령을 실행하실 권한이 없습니다.".format(ctx.message.author))
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("유저를 넣지 않으셨습니다.")
    if isinstance(error, commands.BadArgument):
        await ctx.send("유저를 넣어주세요.")
            
@app.command(name="경고", pass_context=True)
@commands.has_any_role("Commander","NA","supporter","administrator","police","manager")
async def _warn(ctx, counts, user_name: discord.Member=None, reason="사유 없음", reason2="아이디 없음", amount=1):
    id1 = str(user_name).split("#")
    id2 = str(ctx.message.author).split("#")
    id3 = str(user_name).split("#")
    id4 = str(ctx.message.author).split("#")
    warnings_user = get(ctx.guild.members, name=id1[0])
    complete_user = get(ctx.guild.members, name=id2[0])
    warnings2_user = get(ctx.guild.members, name=id3[0])
    complete2_user = get(ctx.guild.members, name=id4[0])
    user_name = user_name or ctx.message.author
    await ctx.channel.purge(limit=1)
    await user_name.add_roles(get(ctx.guild.roles, name="경고"))
    if user_name == None:
        await ctx.send("자신에게 경고를 줄 수 없습니다.")
    else:
        foundfile = find(str(user_name)+".txt", "warnings\\")
        if foundfile == True:
            f = open("warnings\\"+str(user_name)+".txt", "r")
            warncount = f.read()
            f.close()
            f = open("warnings\\"+str(user_name)+".txt", "w+")
            f.write(str(int(warncount)+int(counts)))
            f.close()
            embed = setEmbed(Title="대 상", Footer="", Description=""+warnings_user.mention, Color=0xc81623,
            Inline=[True, True, True, True, True, True], Thumbnail=None, 처리한_관리자= complete_user.mention, 사유=reason, 서버_닉네임=reason2, 현재_경고_수=(str(int(warncount)+int(counts)))+"/2", 고유_ID="\\"+warnings_user.mention)
            embed.set_thumbnail(url=str(user_name.avatar_url))
            embed.set_author(name="경고(Warn)", icon_url="https://i.imgur.com/8U9ayci.jpg")
            embed.set_footer(text = "| KaKao Battle Ground Adult Only | ⓒ 2020.토토로 All rights reserved. |", icon_url="https://i.imgur.com/ZdoUTX4.png")
            await ctx.send(embed=embed)
    
        elif foundfile == False:
                f = open("warnings\\"+str(user_name)+".txt", "w+") # 파일 새로 생성
                f.write(str(int(counts))) # 경고 쓰기
                f.close() # 파일 닫기
                embed = setEmbed(Title="대 상", Footer="", Description=""+warnings2_user.mention, Color=0xc81623,
                Inline=[True, True, True, True, True, True], Thumbnail=None, 처리한_관리자= complete2_user.mention, 사유=reason, 서버_닉네임=reason2, 현재_경고_수=str(int(counts))+"/2", 고유_ID="\\"+warnings_user.mention)
                embed.set_thumbnail(url=str(user_name.avatar_url))
                embed.set_author(name="경고(Warn)", icon_url="https://i.imgur.com/8U9ayci.jpg")
                embed.set_footer(text = "| KaKao Battle Ground Adult Only | ⓒ 2020.토토로 All rights reserved. |", icon_url="https://i.imgur.com/ZdoUTX4.png")
                await ctx.send(embed=embed)
             
@app.command(pass_context=True)
async def join(ctx):
    server = ctx.message.guild.voice_client
    await server.connect()    

# discord event function
@app.event
async def on_message(message):
    await app.process_commands(message)
    if message.author.bot:
        return None
    if message.content == "토봇명령어":
        await message.channel.purge(limit=1)
        #commander = discord.utils.get(message.guild.roles, id=684817019081981952)
        #await message.channel.send("{} Python Bot에 의해 출력됨.".format(commander.mention))
        embed = discord.Embed(title="토봇 도움말", description="", color=0x00ff00)
        embed.set_author(name="~★", icon_url="https://i.imgur.com/QiAXpTI.gif")
        embed.add_field(name="**Manage**", value="**``#경고``** **``#밴``** **``#뮤트``** **``#언뮤트``** **``#mem``** **``#fam``** **``#청소``** \n**``명령어에 대한 자세한 설명은 #토봇_명령어 채널을 봐주세요``**", inline=False)
        embed.add_field(name="**Helper**", value="**``토봇안내``** **``토봇라이브``** **``토봇오픈채팅``**", inline=False)
        embed.add_field(name="**Administrator**", value="**``#신고센터``** **``#관리자``**", inline=False)
        embed.add_field(name="**Error Report**", value="**``#토토로``**", inline=False)
        embed.add_field(name="**Etc**", value="**``#계산``** **``기타 기능 추가중``**\n\n ``Administrator와 Error Report 명령어는 사용 시 모든 관리자에게 알림이 가므로 필요시에만 사용 바랍니다. 특별한 의미없이 사용 시 제재가 가해질 수 있습니다. ``", inline=False)
        embed.set_footer(text = "| KaKao Battle Ground Adult Only | ⓒ 2020.토토로 All rights reserved. |", icon_url="https://i.imgur.com/G2DrrhM.png")
        await message.channel.send(embed=embed)
    if message.content == "토봇안내":
        await message.channel.purge(limit=1)
        #commander = discord.utils.get(message.guild.roles, id=684817019081981952)
        #await message.channel.send("{} Python Bot에 의해 출력됨.".format(commander.mention))
        embed = discord.Embed(title=":sunflower: 카배성 공지입니다:grey_exclamation: :sunflower:", description="```Elm\n 안녕하세요 ★ Kakao Battle Ground ★ 성인채널 입니다!\n``````cs\n 카배성은 다 같이 모여 즐겁게 게임하기 위해 만들어진 공간입니다! \n'아래 사항을 준수해 주세요!' \n 1. 욕설, 합의되지 않은 '반말 사용, 정치적 발언 금지' (게임만 하는 공간에서 분쟁 금지) \n 2. 라이브방의 '저격 금지' \n 3. 게임 중인방의 '사플 방해' 말 없이 들어갔다 나왔다 하시는 분들 잦은 신고 들어오면 강퇴합니다. \n(마이크, 헤드셋 설정은 대기방 등 미리 설정하고 들어오세요!) \n 4. (별명 / 카배아이디) 기본 설정 안 하신 분 - '주기적으로 정리합니다.' \n'닉변 후 알려주시면 members로 등급 올려드립니다.' \n 5. 채널 내 다른 채널 홍보 및 개인 DM 인원 모집 '금지합니다!' 같이하실 분 없으면 운영진 언급해주세요! \n 24시간 대기 중 사람 구해드립니다!\n``` ```diff\n-기타 운영진의 제재 무시시 불이익은 본인에게 있습니다.\n```", color=0x0000ff)
        embed.set_footer(text = "| KaKao Battle Ground Adult Only | ⓒ 2020.토토로 All rights reserved. |", icon_url="https://i.imgur.com/G2DrrhM.png")
        await message.channel.send(embed=embed)
    if message.content == "토봇라이브":
        await message.channel.purge(limit=1)
        #commander = discord.utils.get(message.guild.roles, id=684817019081981952)
        #await message.channel.send("{} Python Bot에 의해 출력됨.".format(commander.mention))
        embed = discord.Embed(title=":sunflower: 라이브 공지입니다:grey_exclamation: :sunflower:", description="**```cs\n라이브방 이용 시 꼭! '최소 1명의' 인원 이상은 라이브를 켜고 이용 바랍니다^^ \n또는 아래쪽 일반 배그 스쿼드, 듀오, 롤 방도 있으니 참고해서 이용해 주세요! \n라이브를 켜지 않은 방은 '임의적으로' 방이 옮겨질 수 있습니다!```**", color=0x0000ff)
        embed.set_footer(text = "| KaKao Battle Ground Adult Only | ⓒ 2020.토토로 All rights reserved. |", icon_url="https://i.imgur.com/G2DrrhM.png")
        await message.channel.send(embed=embed)
    if message.content == "토봇오픈채팅":
        await message.channel.purge(limit=1)
        #commander = discord.utils.get(message.guild.roles, id=684817019081981952)
        #await message.channel.send("{} Python Bot에 의해 출력됨.".format(commander.mention))
        embed = discord.Embed(title=":four_leaf_clover: 카배성 오픈채팅 링크입니다:grey_exclamation: :four_leaf_clover:", description="https://open.kakao.com/o/gLXyngvb \n(디스코드 닉네임과 동일하게 닉네임 / 나이 / 성별으로 변경해주세요!) \n ex) 토토로 26 남", color=0x00ff00)
        embed.set_footer(text = "| KaKao Battle Ground Adult Only | ⓒ 2020.토토로 All rights reserved. |", icon_url="https://i.imgur.com/G2DrrhM.png")
        embed.set_image(url="https://i.imgur.com/WMNMTy2.jpg")
        await message.channel.send(embed=embed)

    if message.content == "#신고센터":
        police = discord.utils.get(message.guild.roles, name="police")
        await message.channel.send("{} :rotating_light: 삐용삐용 신고센터 호출! :rotating_light: 잠시만 기다려주세요!".format(police.mention))

    if message.content == "#관리자":
        Na = discord.utils.get(message.guild.roles, name="Na")
        manager = discord.utils.get(message.guild.roles, name="manager")
        administrator = discord.utils.get(message.guild.roles, name="administrator")
        await message.channel.send(format(Na.mention)+format(manager.mention)+format(administrator.mention)+" :rotating_light: 삐용삐용 관리자 호출! :rotating_light: 잠시만 기다려주세요!")

    if message.content == "#토토로":
        supporter = discord.utils.get(message.guild.roles, name="supporter")
        await message.channel.send("{} :frog: 개굴개굴 부르셨나요? :frog:".format(supporter.mention))
                
    if message.content.startswith("토봇1부터10"):
        for x in range(10):
            await message.channel.send(x+1)
    if message.content.startswith("#계산"):
        global calcResult
        param = message.content.split()
        try:
            if param[1].startswith("더하기"):
                calcResult = int(param[2])+int(param[3])
                await message.channel.send("Result : "+str(calcResult))
            if param[1].startswith("빼기"):
                calcResult = int(param[2])-int(param[3])
                await message.channel.send("Result : "+str(calcResult))
            if param[1].startswith("곱하기"):
                calcResult = int(param[2])*int(param[3])
                await message.channel.send("Result : "+str(calcResult))
            if param[1].startswith("나누기"):
                calcResult = int(param[2])/int(param[3])
                await message.channel.send("Result : "+str(calcResult))
        except IndexError:
            await message.channel.send("```cs\n '사용 방법'\n #계산 (더하기/빼기/곱하기/나누기) 숫자 숫자 \n-> '#계산 더하기 2 2' / '#계산 곱하기 3 9' \n```")
        except ValueError:
            await message.channel.send("숫자로 넣어주세요.")
        except ZeroDivisionError:
            await message.channel.send("You can't divide with 0 !")
            
    if message.content.startswith("PBOTEmbed실행"):
        embed = setEmbed(Title="Example Embed", Footer="이것은 푸터입니다.", Description="이것은 Embed입니다.", Color=0x00ff56,
    Inline=True, Thumbnail="https://i.imgur.com/8U9ayci.jpg",
    이것은_필드_1입니다="필드의 값입니다.", 이것은_필드_2입니다="필드의 값입니다.", 이것은_필드_3입니다="필드의 값입니다.", 
    이것은_필드_4입니다="필드의 값입니다.")
        await message.channel.send(embed=embed)
        
    if message.content == "앉아":
        await message.channel.purge(limit=1)
        await message.channel.send("털썩-")
        

app.run(token)
