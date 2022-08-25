from plistlib import FMT_BINARY
from re import A
import discord
from discord.ext import commands
import os
from discord_slash import SlashCommand, cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
bot = commands.Bot(command_prefix='$')
print("Working...")
dirname = os.path.dirname(os.path.realpath(__file__))
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game('$도움말'))

slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

@bot.event
async def on_message(msg):
    if msg.author.bot: return None
    await bot.process_commands(msg)
        
@slash.slash(name = "송금", description = "원하는 멤버에게 돈을 보내요.")
async def 송금(ctx:SlashContext, 멤버:str, 액수:int):
    with open(dirname+'\list.txt', encoding = 'UTF-8') as file:    # hello.txt 파일을 읽기 모드(r)로 열기
      listr = file.readlines()
    with open(dirname+'\content.txt', encoding = 'UTF-8') as file_b:    # hello.txt 파일을 읽기 모드(r)로 열기
      contentr = file_b.readlines()
    sender = ctx.author.name
    sender = sender.replace(' ', '-')+"\n"
  
    reciever = 멤버
    reciever = reciever.replace(' ', '-')+"\n"
    amount = 액수
    try:
      amount = int(amount)
      if amount < 0 and not ctx.author.name == "후신라왕국 국왕":
        await ctx.send("금액 칸의 값이 음수일 수는 없어요.")
      else:
        if sender in listr and reciever in listr:
          index_sender = listr.index(sender)
          index_reciever = listr.index(reciever)
          print(contentr)
          if 'n' in contentr[index_sender]:
            sender_amount = int(str(contentr[index_sender])[:len(str(contentr[index_sender]))-2])
          else:
            sender_amount = int(contentr[index_sender])
          if int(sender_amount) < amount:
            await ctx.send("이런! **"+sender.replace('-', ' ')[:len((listr[index_sender]))-1]+"**님, 잔액이 부족하군요. 계좌의 잔액을 확인해주세요.")
          else:
            if 'n' in contentr[index_reciever]:
              reciever_amount = int(str(contentr[index_reciever])[:len(str(contentr[index_reciever]))-2])
            else:
              reciever_amount = int(contentr[index_reciever])
            sender_amount = sender_amount - amount
            reciever_amount = reciever_amount + amount
            if '\n' in contentr[index_sender]:
              sender_amount = str(sender_amount)+"\n"
            else:
              sender_amount = str(sender_amount)
            if '\n' in contentr[index_reciever]:
              reciever_amount = str(reciever_amount)+"\n"
            else:
              reciever_amount = str(reciever_amount)

            contentr[index_sender] = sender_amount
            contentr[index_reciever] = reciever_amount
            with open(dirname+'\content.txt', 'w', encoding = 'UTF-8') as enrollname:
              enrollname.write(contentr[0])
            a = 1
            for x in range(len(contentr)-1):
              with open(dirname+'\content.txt', 'a', encoding = 'UTF-8') as enrollname:
                enrollname.write(contentr[a])
              a = a+1
            await ctx.send("**"+ctx.author.name+"**님이 **"+reciever.replace('-', ' ')[:len((listr[index_reciever]))-1]+"** 님에게 "+str(amount)+"환을 송금했어요.")
        else:
          await ctx.send("송금을 받는 사용자가 은행에 등록되어있지 않아요.")

        
    except ValueError:
      await ctx.channel.send("금액 칸의 값이 정수여야만 해요.")
  
@slash.slash(name = "등록", description = "계좌를 등록해요.")
async def _등록(ctx):
  username = ctx.author.name
  username = username.replace(' ','-')+"\n"
  with open(dirname+'\list.txt', encoding = 'UTF-8') as file:    # hello.txt 파일을 읽기 모드(r)로 열기
    list = file.readlines()
  with open(dirname+'\content.txt', encoding = 'UTF-8') as file_b:    # hello.txt 파일을 읽기 모드(r)로 열기
    content = file_b.readlines()
  print(list)
  print(content)
  if username in list:
    index = list.index(username)
    await ctx.send("이런! **"+username.replace('-', ' ')[:len((list[index]))-1]+"**님은 이미 은행에 가입되어 있군요!")
  else:
    with open(dirname+'\list.txt', 'a', encoding = 'UTF-8') as enrollname:
      enrollname.write(username)
    with open(dirname+'\content.txt', 'a', encoding = 'UTF-8') as enroll:
      enroll.write("\n"+"0")
    with open(dirname+'\list.txt', encoding = 'UTF-8') as file:    # hello.txt 파일을 읽기 모드(r)로 열기
      list = file.readlines()
    with open(dirname+'\content.txt', encoding = 'UTF-8') as file_b:    # hello.txt 파일을 읽기 모드(r)로 열기
      content = file_b.readlines()
    index = list.index(username)
    await ctx.send("**"+username.replace('-', ' ')[:len((list[index]))-1]+"**님, 후신라왕국 은행에 오신것을 환영해요! 은행을 사용하시는것이 처음이라면, `$도움말`을 입력해보세요.")
@slash.slash(name = "은행", description = "은행에 등록되어있는 계좌들을 보여줘요.")
async def _은행(ctx:SlashContext):
  with open(dirname+'\list.txt', encoding = 'UTF-8') as file:
    list = file.readlines()
  with open(dirname+'\content.txt', encoding = 'UTF-8') as file_b:
    content = file_b.readlines()
  print(content)
  global A
  global T
  A = 0
  T = "```md\n"
  for x in range(len(list)):
    if A == len(list)-1:
      a = str(list[A])
      a = a.find("n")
      T = T+"<_"+str(list[A]).replace('-', ' ')[0:a]+">  "
      b = str(content[A])
      b = b.find("n")
      T = T+str(content[A])+"환\n"
      A = A+1
    else:
      a = str(list[A])
      a = a.find("n")
      T = T+"**"+str(list[A]).replace('-', ' ')[0:a]+"** - "
      b = str(content[A])
      b = b.find("n")
      T = T+"<"+str(content[A])[0:b]+"환>\n"
      A = A+1
  T = T+"\n```"
  embed = discord.Embed(title = "은행", description = T[1:], colour = 0x7DB249)
  await ctx.send(embed = embed)
@slash.slash(name = "잔액", description = "내 계좌의 잔액을 보여줘요.")
async def _잔액(ctx:SlashContext):
  with open(dirname+'\list.txt', encoding = 'UTF-8') as file:    # hello.txt 파일을 읽기 모드(r)로 열기
    listr = file.readlines()
  with open(dirname+'\content.txt', encoding = 'UTF-8') as file_b:    # hello.txt 파일을 읽기 모드(r)로 열기
    contentr = file_b.readlines()
  username = ctx.author.name
  username = username.replace(' ','-')+"\n"
  if username in listr:
    index = listr.index(username)
    if '\n' in str(contentr[index]):
      embed = discord.Embed(title = "**"+str(listr[index]).replace('-', ' ')[:len((listr[index]))-1]+"**님의 계좌", description = "**"+str(listr[index]).replace('-', ' ')[:len((listr[index]))-1]+"**님의 잔액은 **"+str(contentr[index])[:len((str(contentr[index])))-1]+"환** 입니다.", colour = 0x7DB249)
      await ctx.send(embed=embed)
    else:
      embed = discord.Embed(title = "**"+str(listr[index]).replace('-', ' ')[:len((listr[index]))-1]+"**님의 계좌", description = "**"+str(listr[index]).replace('-', ' ')[:len((listr[index]))-1]+"**님의 잔액은 **"+str(contentr[index])+"환** 입니다.", colour = 0x7DB249)
      await ctx.send(embed=embed)
  else:
    embed = discord.Embed(title = "이런!", description = "먼저, `/등록` 명령어로 은행에 가입해 주세요. 만일 **닉네임을 변경했다면, 봇이 못 알아들을 수도 있답니다.**", colour = 0x7DB249)
    await ctx.send(embed=embed)

@slash.slash(name = "도움말", description = "사용 가능한 명령어들을 보여줘요.")
async def _도움말(ctx:SlashContext):
  embed = discord.Embed(title = "도움말", description = "**후신라은행을 이용해주셔서 진심으로 감사드립니다.**", colour = 0x7DB249)
  embed.add_field(name="/등록", value="계좌를 은행에 등록합니다.", inline = False)
  embed.add_field(name="/은행", value="은행 계좌의 목록을 보여줍니다.", inline = False)
  embed.add_field(name="/잔액", value="자신의 잔액을 보여줍니다.", inline = False)
  embed.add_field(name="/송금", value="다른 계좌에 돈을 보냅니다.")
  await ctx.send(embed = embed)

@bot.command()
async def 임베드(ctx):
  embed = discord.Embed(title="1", description = "1", color = 0x62c1cc)
  embed.set_footer(text = "1")
  await ctx.channel.send(embed=embed)

bot.run(os.environ['token'])