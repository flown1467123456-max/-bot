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
def 銀行資料(interaction):
    data=load_bank()
    user_id=str(interaction.user.id)
    return(f"bank:{data[user_id]['bank']}元\n"f"wallet:{data[user_id]['wallet']}元\n"f"balance:{data[user_id]['bank']+data[user_id]['wallet']}元\n"f"level:{data[user_id]['level']}級")

def dmg(interaction):
    user_id=str(interaction.user.id)
    data=load_bank()
    level=data[user_id]['level']
    damage = 0
    for lv in range(1, level+1):
        damage += 5 + ( (lv-1)//3 )
    return int(damage)

def dfs(interaction):
    damage=dmg(interaction)
    defense=damage * 1.25
    return(defense)

def 格式更新(interaction):
    data=load_bank()
    user_id=str(interaction.user.id)
    if user_id not in data:
        data[user_id]=user_id
    account=data[user_id]
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
    data[user_id]['damage']=dmg(interaction)
    data[user_id]['defense']=dfs(interaction)
    save_bank(data)
    return data[user_id],fixed

def balance(interaction):
    user_id=str(interaction.user.id)
    data=load_bank()
    if user_id not in data:
        data[user_id]={"wallet": 0, "bank": 1000, "level": 1}
    格式更新(interaction)
    return("給點建議吧，這裡不知道要寫什麼\n"+銀行資料(interaction))
        
def deposit(interaction,money):
    user_id=str(interaction.user.id)
    data=load_bank()
    if user_id not in data:
        return('還未開戶，請使用*/balance*')
    else:
                             if money>data[user_id]['wallet']:
                                 return(f"你的現金不足\n"+銀行資料(interaction))
                             elif money<0:
                                 return(f"腦洞挺大的(不能存負數)\n"+銀行資料(interaction))
                             else:
                                 data[user_id]['wallet']-=money
                                 data[user_id]['bank']+=money
                                 save_bank(data)
                                 return(f"已存入{money}元\n"+銀行資料(interaction))

def withdraw(interaction,money):
    user_id=str(interaction.user.id)
    data=load_bank()
    if user_id not in data:
        return('還未開戶，請使用*/balance*')
    else:
            if money>data[user_id]["bank"]:
                return(f"你的金額不足\n"+銀行資料(interaction))
            elif money<0:
                return(f"腦洞挺大的\n"+銀行資料(interaction))
            else:
                data[user_id]['wallet']+=money
                data[user_id]['bank']-=money
                save_bank(data)
                return(f"已取出{money}元\n"+銀行資料(interaction))

def rob(interaction,target):
    data=load_bank()
    user_id=str(interaction.user.id)
    if user_id not in data:
        return('還未開戶，請使用*/balance*')
    target_id=str(target.id)
    if target_id not in data:
        return('對方還未開戶，請使用*/rob*重新選一個人')
    user_name=interaction.user.display_name
    target_name=target.display_name
    try:
        damage=data[user_id]['damage']
    except:
        return("你的資料裡沒有*damage*，請使用*/balance*更新資料")
    try:
        defense=data[target_id]['defense']
    except:
        return("對方的資料裡未有*defense*，請使用*/rob*重新選一個人")
    破防率=min(damage / defense, 1)
    理論搶走的錢=int(damage * 破防率)
    實際搶走的錢=min(int(data[target_id]['bank']),理論搶走的錢)
    data[target_id]['bank']-=實際搶走的錢
    data[user_id]['wallet']+=實際搶走的錢
    save_bank(data)
    return(f"{user_name}搶了{target_name}{實際搶走的錢}元\n"+銀行資料(interaction))

#主要程式
class Client(commands.Bot):
    async def on_ready(self):
        await self.tree.sync()
        print(f'{self.user}已就緒')

client=Client(command_prefix='!',intents=intents)
#斜槓指令
@client.tree.command(name='balance',description='查看銀行+自動開戶')
async def balance_slash(interaction:discord.Interaction):
    print(f'{interaction.user}使用balance')
    格式更新(interaction)
    await interaction.response.send_message(balance(interaction))

@client.tree.command(name='deposit',description='存錢')
async def deposit_slash(interaction:discord.Interaction,amount:int):
    print(f'{interaction.user}使用deposit')
    格式更新(interaction)
    await interaction.response.send_message(deposit(interaction,amount))

@client.tree.command(name='withdraw',description='取錢')
async def withdraw_slash(interaction:discord.Interaction,amount:int):
    print(f'{interaction.user}使用withdraw')
    格式更新(interaction)
    await interaction.response.send_message(withdraw(interaction,amount))

@client.tree.command(name='rob',description='搶銀行')
async def rob_slash(interaction:discord.Interaction,target:discord.Member):
    print(f'{interaction.user}使用rob')
    格式更新(interaction) 
    await interaction.response.send_message(rob(interaction,target))
#token
TOKEN = os.environ["DISCORD_TOKEN"]
client.run(TOKEN)
