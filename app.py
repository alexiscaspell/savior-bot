import os

import discord
from discord import ApplicationContext
from dotenv import load_dotenv

from src.savior import PrayResponse, Savior
from typing import List
from src.utils.string_util import make_str_table,make_str_table_old
from src.utils.logger_util import get_logger

load_dotenv()

logger = get_logger(__name__)

TOKEN = os.getenv('DISCORD_TOKEN')
ADMIN_USERS = os.getenv('ADMIN_USERS',None)
ADMIN_USERS= ADMIN_USERS.split(",") if ADMIN_USERS else []

savior = Savior(os.getenv('SAVIOR_URL'))

bot = discord.Bot()

async def send_response(ctx:ApplicationContext,message):
    try:
        await ctx.respond(message)
    except Exception as _:
        await ctx.channel.send(message)

async def validate_permissions(ctx:ApplicationContext):
    message_user = ctx.author.name

    logger.info(f"{message_user} me acaba de invocar")

    if len(ADMIN_USERS)>0 and message_user not in ADMIN_USERS:
        await ctx.respond(f"**{message_user}** papu, no tenes permisos")
        raise RuntimeError(f"El usuario {message_user} no tiene permisos de admin")

# def format_results(results:List[str]):
#     str_list = ["Puntos y/o sugerencias"]+results
#     return make_str_table(str_list)
def format_results(service_name:str,results:List[str]):
    if len(results)==0:
        text = f"**No encontre nada extraño con el servicio {service_name}**\n"
        return text
    text = f"**Estos son los puntos y/o sugerencias que pude detectar para {service_name}:**\n"
    text+= f"```diff\n"
    for r in results:
        text+=f"+ {r}\n"
    text+= f"```"
    return text

def format_response(service_name:str,response:PrayResponse):
    results = []
    for rule in response.rules:
        for consequence in rule.consequences:
            results.append(str(consequence.result))

    return format_results(service_name,results)


@bot.slash_command(description="Te ayuda con tu servicio con nombre <name> en el ambiente <env> (default desa)")
async def helpme(ctx:ApplicationContext,name="my service",env="desa"):

    await ctx.respond("Salvando el dia ...")

    async with ctx.typing():
        service_id=None
        response = f"Error listando servicios que coincidan con {name}"

        logger.info(f"Buscando servicio {name} - {env}")
        
        try:

            possible_services = savior.get_by_name_like(name)
            service_name = name

            logger.info(f"Encontrados servicios {list(map(lambda s:s.name,possible_services))}")

            for s in possible_services:
                if env in s.name:
                    service_name = s.name
                    service_id = s.id

            if service_id is None:
                response = "No se encontro el servicio :("
                raise RuntimeError(f"No se encontro servicio para {name} - {env}")

            response = f"Error intentando salvar a {service_name}"

            savior_response = savior.pray(service_id)
            response = format_response(service_name,savior_response)
        except Exception as e:
            logger.error(e)


    await ctx.interaction.edit_original_response(content=response)

@bot.slash_command(description="Lista todos los servicios bajo un determinado filtro <name>")
async def list_services(ctx:ApplicationContext,name="my service"):

    await ctx.respond("Buscando servicios ...")

    async with ctx.typing():
        response = f"Error listando servicios que coincidan con {name}"

        logger.info(f"Buscando servicio {name}")
        
        try:

            possible_services = savior.get_by_name_like(name)

            service_names = list(map(lambda s:s.name,possible_services))

            logger.info(f"Encontrados servicios {service_names}")

            if not service_names:
                response = "No se encontro el servicio :("
                raise RuntimeError(f"No se encontro servicio para {name}")

            response = f"**Servicios encontrados:**\n"
            response+="```diff\n"

            for s in service_names:
                response+=f"+ {s}\n"

            response+="```"

        except Exception as e:
            logger.error(e)


    await ctx.interaction.edit_original_response(content=response)

@bot.event
async def on_ready():
    logger.info(f'{bot.user.name} has connected to Discord!')

bot.run(TOKEN)
