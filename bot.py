import discord
import os
import json
from discord.ext import commands
from discord import app_commands
print(os.getcwd())
#機器人設定
intents = discord.Intents.default()
intents.message_content=True
#遊戲設定
BANK_DIR = os.path.join(os.environ['HOME'], "bot")
os.makedirs(BANK_DIR, exist_ok=True)
BANK_FILE = os.path.join(BANK_DIR, "bank.json")

def load_bank():
    if not os.path.exists(BANK_FILE):
        return {}
    try:
        with open(BANK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        # JSON 壞掉防止報錯
        return {}
        
def save_bank(data):
    with open(BANK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
#檢查資料
print("目前資料:", load_bank())
print("銀行檔案實際路徑:", os.path.abspath(BANK_FILE))

#函式
def 格式更新(user_id,account:dict):
    data=load_bank()
    DEFAULT_ACCOUNT={'wallet':0,'bank':1000,'level':1}
    fixed=False
    for key,default_value in  DEFAULT_ACCOUNT.items():
        if key not in account:
            data[user_id][key]=default_value
            fixed=True
    for key in list(account.keys()):
        if key not in DEFAULT_ACCOUNT:
            del data[user_id][key]
            fixed=True
    save_bank(data)
    return data[user_id],fixed

def balance(user_id):
    user_id=str(user_id)
    data=load_bank()
    if user_id not in data:
        data[user_id] = {'wallet':0,'bank':1000,'level':1}
        save_bank(data)
        return("已自動開戶\n""給點建議吧，這裡不知道要寫什麼\n"f"bank:{data[user_id]['bank']}元\n"f"wallet:{data[user_id]['wallet']}元\n"f"balance:{data[user_id]['bank']+data[user_id]['wallet']}元\n"f"level:{data[user_id]['level']}級")
    else:
        return("給點建議吧，這裡不知道要寫什麼\n"f"bank:{data[user_id]['bank']}元\n"f"wallet:{data[user_id]['wallet']}元\n"f"balance:{data[user_id]['bank']+data[user_id]['wallet']}元\n"f"level:{data[user_id]['level']}級")
        
def deposit(user_id,money):
    user_id=str(user_id)
    data=load_bank()
    if user_id not in data:
        data[user_id] = {'bank': 1000,'wallet':0,'level':1}
        save_bank(data)
        return("已自動開戶\n"f"你的現金不足(指令是存錢)\n"f"bank:{data[user_id]['bank']}元\n"f"wallet:{data[user_id]['wallet']}元\n"f"balance:{data[user_id]['bank']+data[user_id]['wallet']}元\n"f"level:{data[user_id]['level']}級")
    else:
                    if money>data[user_id]['wallet']:
                        return(f"你的現金不足\n"f"bank:{data[user_id]['bank']}元\n"f"wallet:{data[user_id]['wallet']}元\n"f"balance:{data[user_id]['bank']+data[user_id]['wallet']}元\n"f"level:{data[user_id]['level']}級")
                    elif money<0:
                        return(f"腦洞挺大的(不能存負數)\n"f"bank:{data[user_id]['bank']}元\n"f"wallet:{data[user_id]['wallet']}元\n"f"balance:{data[user_id]['bank']+data[user_id]['wallet']}元\n"f"level:{data[user_id]['level']}級")
                    else:
                        data[user_id]['wallet']-=money
                        data[user_id]['bank']+=money
                        save_bank(data)
                        return(f"已存入{money}元\n"f"bank:{data[user_id]['bank']}元\n"f"wallet:{data[user_id]['wallet']}元\n"f"balance:{data[user_id]['bank']+data[user_id]['wallet']}元\n"f"level:{data[user_id]['level']}級")
                        
def withdraw(user_id,money):
    user_id=str(user_id)
    data=load_bank()
    if user_id not in data:
        data[user_id] = {'bank': 1000,'wallet':0,'level':1}
        save_bank(data)
        return(f"已自動開戶\n"f"bank:{data[user_id]['bank']}元\n"f"wallet:{data[user_id]['wallet']}元\n"f"balance:{data[user_id]['bank']+data[user_id]['wallet']}元\n"f"level:{data[user_id]['level']}級")
    else:
        if money>data[user_id]["bank"]:
            return(f"你的金額不足\n"f"bank:{data[user_id]['bank']}元\n"f"wallet:{data[user_id]['wallet']}元\n"f"balance:{data[user_id]['bank']+data[user_id]['wallet']}元\n"f"level:{data[user_id]['level']}級")
        elif money<0:
            return(f"腦洞挺大的\n"f"bank:{data[user_id]['bank']}元\n"f"wallet:{data[user_id]['wallet']}元\n"f"balance:{data[user_id]['bank']+data[user_id]['wallet']}元\n"f"level:{data[user_id]['level']}級")
        else:
            data[user_id]['wallet']+=money
            data[user_id]['bank']-=money
            save_bank(data)
            return(f"已取出{money}元\n"f"bank:{data[user_id]['bank']}元\n"f"wallet:{data[user_id]['wallet']}元\n"f"balance:{data[user_id]['bank']+data[user_id]['wallet']}元\n"f"level:{data[user_id]['level']}級")

#主要程式
class Client(commands.Bot):
    async def on_ready(self):
        await self.tree.sync()
        print(f'{self.user}已就緒')

client=Client(command_prefix='!',intents=intents)

#斜槓指令
@client.tree.command(name='balance',description='查看銀行+自動開戶')
async def Balance(interaction:discord.Interaction):
    print(f'{interaction.user}使用balance')
    await interaction.response.send_message(balance(interaction.user.id))
    格式更新(str(interaction.user.id),load_bank()[str(interaction.user.id)])

@client.tree.command(name='deposit',description='存錢')
async def Deposit(interaction:discord.Interaction,amount:int):
    print(f'{interaction.user}使用deposit')
    await interaction.response.send_message(deposit(str(interaction.user.id),amount))
    格式更新(str(interaction.user.id),load_bank()[str(interaction.user.id)])

@client.tree.command(name='withdraw',description='取錢')
async def Withdraw(interaction:discord.Interaction,amount:int):
    print(f'{interaction.user}使用withdraw')
    await interaction.response.send_message(withdraw(str(interaction.user.id),amount))
    格式更新(str(interaction.user.id),load_bank()[str(interaction.user.id)])
#token
TOKEN = os.environ["DISCORD_TOKEN"]
client.run(TOKEN)