import discord
from discord.ext import commands, tasks
from discord.commands import Option, OptionChoice
from discord.ui import View
from discord.ui.button import Button
from discord.ui.select import Select
from discord.ui.modal import Modal
from discord.ui.input_text import InputText
import datetime
import humanfriendly
import asyncio
import ipapi

intents = discord.Intents.default()
intents.members = True

class PersistentViewBot(commands.Bot):
    def __init__(self):
        super().__init__()
        self.persistent_views_added = False


    async def on_ready(self):
        await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name=f"Pycord 2.5"))
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")

        try:
            global lastMessageId
            timestamp = datetime.datetime.now().timestamp()
            canal = bot.get_channel(1220895264538234881)
            lat = round(bot.latency * 1000)
            embed = discord.Embed(title="Bot online!", description=f"Started: <t:{int(timestamp)}:R>", color=discord.Color.green())

            if lat <= 50:
                button = Button(label=f"{lat} ms", emoji="<:goodping:1155332960443191306>",style=discord.ButtonStyle.grey, disabled=True)        

            elif lat <= 200:
                button = Button(label=f"{lat} ms", emoji="<:midping:1155332958249558116>",style=discord.ButtonStyle.grey, disabled=True)

            elif lat > 200:
                button = Button(label=f"{lat} ms", emoji="<:badping:1155332772219592704>",style=discord.ButtonStyle.grey, disabled=True)


            view = View(timeout=None)
            view.add_item(button)     
            
            message = await canal.send(embed=embed, view=view)

            lastMessageId = message.id

        except discord.NotFound:
            print("Uptime channel not found")

bot = PersistentViewBot()

class CustomEmbed(Modal):
    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
    
        self.add_item(InputText(label="Title", placeholder="Título da embed", style=discord.InputTextStyle.short, required=False))
        self.add_item(InputText(label="Description", placeholder="Descrição da embed", style=discord.InputTextStyle.long, required=False))
        self.add_item(InputText(label="Footer", placeholder="Rodapé da embed", style=discord.InputTextStyle.short, required=False))
        self.add_item(InputText(label="Imagem (opcional)", placeholder="Link da imagem", style=discord.InputTextStyle.short, required=False))
        self.add_item(InputText(label="Cor (opcional)", placeholder="Código hex", style=discord.InputTextStyle.short, required=False))
    
    async def callback(self, interaction: discord.Interaction):
    
        if str(self.children[4].value) != "":
            cor = self.children[4].value.replace('#', '')
            embed=discord.Embed(title=self.children[0].value, description=self.children[1].value, color=int(cor, base = 16))
            embed.set_image(url=self.children[3].value)
            embed.set_footer(text=self.children[2].value)
    
            await interaction.response.send_message(embed=embed)
        
        else:
            embed=discord.Embed(title=self.children[0].value, description=self.children[1].value, color=discord.Color.from_rgb(47, 49, 54))
            embed.set_thumbnail(url=self.children[4].value)
            embed.set_image(url=self.children[3].value)
            embed.set_footer(text=self.children[2].value)
      
            await interaction.response.send_message(embed=embed)

#events -----------------------------------------------------------------

# @bot.event
# async def on_member_join(member):

#     canal = 942896597044453426

#     await canal.send(f"{member} entrou no servidor")

# @bot.event
# async def on_member_leave(member):

#     canal = 942896597044453426

#     await canal.send(f"{member} saiu do servidor")
            
# misc ------------------------------------------------------------------


tipos_canal = [
    OptionChoice(name="Canal de texto", value="texto"),
    OptionChoice(name="Canal de voz", value="voz")
]



# -------------------------------------------------------------------
@bot.slash_command(description="Para o bot")
async def stop(ctx):

    davi = await bot.fetch_user(808413547574591548)

    if ctx.author != davi:
        await ctx.respond(":no_entry: Você não tem permissão para fazer isso.", ephemeral=True)        

    else:

        await ctx.respond("Stopping bot...", ephemeral=True)

        global lastMessageId

        canal = bot.get_channel(1220424323400208524)


        if lastMessageId:
            try:
                last_message = await canal.fetch_message(lastMessageId)
                await last_message.delete()
            except discord.NotFound:
                pass   

        embed=discord.Embed(title="Bot offline", color=discord.Color.red())

        await canal.send(embed=embed)
        await bot.close()

@bot.slash_command(description="Comando privado")
async def say(ctx, msg : str):

    davi = await bot.fetch_user(808413547574591548)
  
    if ctx.author != davi:
        await ctx.respond(":no_entry: Você não tem permissão para fazer isso.", ephemeral=True)
    
    else:
        await ctx.respond("enviando <a:loading:1155312687731978320>", ephemeral=True)
        await ctx.send(msg)
      

@bot.slash_command(description="Comando privado")
async def sayfile(ctx, file : Option(discord.Attachment, description="Adicione um arquivo", required=True)):

    davi = await bot.fetch_user(808413547574591548)
  
    if ctx.author != davi:
        await ctx.respond(":no_entry: Você não tem permissão para fazer isso.", ephemeral=True)
    
    else:
        await ctx.respond("enviando <a:loading:1155312687731978320>", ephemeral=True)
  
        file = await file.to_file()
        await ctx.send(file=file)

@bot.slash_command(description="Comando privado")
async def saydm(ctx, membro : discord.Member, msg : str):

    davi = await bot.fetch_user(808413547574591548)
  
    if ctx.author == davi:
        try:
            await membro.send(msg)
            await ctx.respond("enviado :ballot_box_with_check:", ephemeral=True)
        
        except:
            await ctx.respond(":no_entry: DM bloqueada", ephemeral=True)
      
    else:
        await ctx.respond(":no_entry: Você não tem permissão para fazer isso.", ephemeral=True)

@bot.slash_command(description="Comando privado")
async def sayfiledm(ctx, membro : discord.Member, file : Option(discord.Attachment, description="Adicione um arquivo", required=True)):

    davi = await bot.fetch_user(808413547574591548)
  
    if ctx.author == davi:
        try:
            file = await file.to_file()
            await membro.send(file=file)
            await ctx.respond("enviado :ballot_box_with_check:", ephemeral=True)

        except:
            await ctx.respond(":no_entry: DM bloqueada", ephemeral=True)

    else:
        await ctx.respond(":no_entry: Você não tem permissão para fazer isso.", ephemeral=True)

@bot.slash_command(description="Veja a latência do bot")
async def ping(ctx):

    lat = round(bot.latency * 1000)

    if lat <= 50:
        await ctx.respond(f"<:goodping:1155332960443191306> `{lat} ms`")

    elif lat <= 200:
        await ctx.respond(f"<:midping:1155332958249558116> `{lat} ms`")

    elif lat > 200:
        await ctx.respond(f"<:badping:1155332772219592704> `{lat} ms`")

@bot.slash_command(description='Mostra informações sobre o ip de alguém')
async def ipinfo(ctx, ip : Option(str, description='IP do computador/celular do usuário.', required=True)):
  
    infoip = ipapi.location(ip=ip, output='json')
    
    embed = discord.Embed(title=f'Informações de {ip}', colour=discord.Colour.blue())
    embed.add_field(name='Versão', value=infoip['version'], inline=True)
    embed.add_field(name='Continente', value=infoip['continent_code'], inline=True)
    embed.add_field(name='Nome do país', value=infoip['country_name'], inline=True)
    embed.add_field(name='Código do país', value=infoip['country_code_iso3'], inline=True)
    embed.add_field(name='Nome da capital', value=infoip['country_capital'], inline=True)
    embed.add_field(name='Estado', value=infoip['region'], inline=True)
    embed.add_field(name='Código estado', value=infoip['region_code'], inline=True)
    embed.add_field(name='Cidade', value=infoip['city'], inline=True)
    embed.add_field(name='Postal', value=infoip['postal'], inline=True)
    embed.add_field(name='Línguas', value=infoip['languages'], inline=True)
    embed.add_field(name='Área do país', value=f"{infoip['country_area']} km²", inline=True)
    embed.add_field(name='População', value=infoip['country_population'], inline=True)
    embed.add_field(name='Código da moeda', value=infoip['currency'], inline=True)
    embed.add_field(name='Moeda', value=infoip['currency_name'], inline=True)
    embed.add_field(name='Fuso horário', value=infoip['timezone'], inline=True)
    embed.add_field(name='UTC offset', value=infoip['utc_offset'], inline=True)
    embed.add_field(name='Código de Telefone', value=infoip['country_calling_code'], inline=True)
    embed.add_field(name='ORG', value=infoip['org'], inline=True)

    buttonLat = Button(label=f"Latitude: {infoip['latitude']}", disabled=True)
    buttonLong = Button(label=f"Longitude: {infoip['longitude']}", disabled=True)
    
    view = View(timeout=None)
    view.add_item(buttonLat)
    view.add_item(buttonLong)
    
    await ctx.respond(embed=embed, view=view)


@bot.slash_command(description="Veja todos meus comandos")
async def ajuda(ctx):
    
        embed=discord.Embed(title="Ajuda", description="Selecione na caixa de seleção abaixo o comando em que você está em dúvida", color=discord.Color.blurple())
        embedEmbed=discord.Embed(title="/embed", description="Esse comando é usado para criar embeds de forma amigável para o usuário", color=discord.Color.blurple())
        embedPing=discord.Embed(title="/ping", description="Mostra a latência do bot", color=discord.Color.blurple())
        embedIpinfo=discord.Embed(title="/ipinfo", description="Mostra informações sobre o computador de alguem a partir de um endereço de ip. Use `/ipinfo <ip>`", color=discord.Color.blurple())
        embedMute=discord.Embed(title="/mute", description="Muta/silência um membro. Use: `/mute <membro> <tempo> (motivo)`", color=discord.Color.blurple())
        embedUnmute=discord.Embed(title="/unmute", description="Desmute/dessilência um membro. Use: `/unmute <membro>`", color=discord.Color.blurple())
        embedLock=discord.Embed(title="/lock", description="Bloqueia um canal de texto contra usuários comuns, assim eles não podem falar", color=discord.Color.blurple())
        embedUnlock=discord.Embed(title="/unlock", description="Desbloqueia um canal de texto contra usuários comuns, assim eles podem falar novamente", color=discord.Color.blurple())
        embedSlowmode=discord.Embed(title="/slowmode", description="Ativa o modo lento em um canal de texto. Use `/slowmode <tempo>`", color=discord.Color.blurple())
        embedKick=discord.Embed(title="/kick", description="Expulsa um membro do servidor. Use: `/kick <membro> (motivo)`", color=discord.Color.blurple())
        embedBan=discord.Embed(title="/ban", description="Bane um membro do servidor. Use: `/ban <membro> (motivo)`", color=discord.Color.blurple())
        embedUnban=discord.Embed(title="/unban", description="Desbane um membro do servidor, assim ele pode entrar de novo se desejar. Use: `/unban <usuário>`", color=discord.Color.blurple())
        embedAddrole=discord.Embed(title="/addrole", description="Adiciona um cargo à um membro. Use: `/addrole <membro> <cargo>`", color=discord.Color.blurple())
        embedRemoverole=discord.Embed(title="/removerole", description="Retira um cargo de um membro. Use: `/removerole <membro> <cargo>`", color=discord.Color.blurple())
        embedDelete=discord.Embed(title="/delete", description="Deleta/apaga um canal de texto para sempre", color=discord.Color.blurple())

        select = Select(placeholder="Escolha um comando", options=[
            discord.SelectOption(label="Início", value="INICIO", description="Volta à tela inicial"),
            discord.SelectOption(label="/embed", value="EMBED"),
            discord.SelectOption(label="/ping", value="PING"),
            discord.SelectOption(label="/ipinfo", value="IPINFO"),
            discord.SelectOption(label="/mute", value="MUTE"),
            discord.SelectOption(label="/unmute", value="UNMUTE"),
            discord.SelectOption(label="/lock", value="LOCK"),
            discord.SelectOption(label="/unlock", value="UNLOCK"),
            discord.SelectOption(label="/slowmode", value="SLOWMODE"),
            discord.SelectOption(label="/kick", value="KICK"),
            discord.SelectOption(label="/ban", value="BAN"),
            discord.SelectOption(label="/unban", value="UNBAN"),
            discord.SelectOption(label="/delete", value="DELETE"),
            discord.SelectOption(label="/addrole", value="ADDROLE"),
            discord.SelectOption(label="/removerole", value="REMOVEROLE")
        ], row=1)

        async def selectCallback(interaction):
            if select.values[0] == "INICIO":
                await interaction.response.edit_message(embed=embed)
            elif select.values[0] == "EMBED":
                await interaction.response.edit_message(embed=embedEmbed)
            elif select.values[0] == "PING":
                await interaction.response.edit_message(embed=embedPing)
            elif select.values[0] == "IPINFO":
                await interaction.response.edit_message(embed=embedIpinfo)
            elif select.values[0] == "MUTE":
                await interaction.response.edit_message(embed=embedMute)
            elif select.values[0] == "UNMUTE":
                await interaction.response.edit_message(embed=embedUnmute)
            elif select.values[0] == "LOCK":
                await interaction.response.edit_message(embed=embedLock)
            elif select.values[0] == "UNLOCK":
                await interaction.response.edit_message(embed=embedUnlock)
            elif select.values[0] == "SLOWMODE":
                await interaction.response.edit_message(embed=embedSlowmode)
            elif select.values[0] == "KICK":
                await interaction.response.edit_message(embed=embedKick)
            elif select.values[0] == "BAN":
                await interaction.response.edit_message(embed=embedBan)
            elif select.values[0] == "UNBAN":
                await interaction.response.edit_message(embed=embedUnban)
            elif select.values[0] == "DELETE":
                await interaction.response.edit_message(embed=embedDelete)
            elif select.values[0] == "ADDROLE":
                await interaction.response.edit_message(embed=embedAddrole)
            elif select.values[0] == "REMOVEROLE":
                await interaction.response.edit_message(embed=embedRemoverole)
            
        select.callback = selectCallback
        
        view = View(timeout=None)
        view.add_item(select)

        await ctx.respond(embed=embed, view=view)


# admin ----------------------------------------------------------------------------------

@bot.slash_command(description="Criador de embeds dinâmico")
@commands.has_permissions(manage_messages=True)
async def embed(ctx):

    modal = CustomEmbed(title="Criador de Embed")
    await ctx.send_modal(modal)

@bot.slash_command(description="Mostra algumas informações")
async def info(ctx):

    embed=discord.Embed(title="Info", description="Sou um bot interativo, meu principal objetivo é fazer com que o gerenciamento do servidor seja mais facil e divertido para todos", color=discord.Color.blurple())
    embed.add_field(name="<:devBOT:942899235274235934> Comandos", value="Para saber todos meus comandos digite `/ajuda`", inline=False)
    embed.add_field(name="<:Python:945804727160045619> Suporte", value="O bot está em desenvolvimento constante. Nos dê sugestões ou tire duvidas no canal #canal", inline=False)

    await ctx.respond(embed=embed)

@bot.slash_command(description='Silência um membro')
@commands.has_permissions(administrator=True)
async def mute(ctx, membro : Option(discord.Member, description="Escolha um membro", required=True), tempo : Option(str, description='EXEMPLO: 10s = segundos, 10m = minutos, 10h = horas, 10d = dias, 10w = semanas.', required=True), motivo=None):

    punishments = ctx.guild.get_channel(1149157075956531231)
    
    time = humanfriendly.parse_timespan(tempo)
    
    minuto = time / 60
    hora = minuto / 60
    dia = hora / 24
    semana = dia / 7

    
    if time <= 60:

        embedpv=discord.Embed(title="Mute", description=f"Você foi silênciado em **{discord.Guild.name}**. Motivo: {motivo}", color=discord.Color.red())
        embedctx=discord.Embed(title=None, description=f"{membro.mention} Mutado com sucesso por {time} segundo(s). Motivo: {motivo}", color=discord.Color.green())
        embedpunishments=discord.Embed(title="Mute", description=f"{membro.mention} Foi silenciado por {time} segundo(s).", color=discord.Color.red())
        embedpunishments.add_field(name="Motivo:",value=f"{motivo}")

    elif time > 60:

        embedpv=discord.Embed(title="Mute", description=f"Você foi silênciado em **{discord.Guild.name}**. Motivo: {motivo}", color=discord.Color.red())
        embedctx=discord.Embed(title=None, description=f"{membro.mention} Mutado com sucesso por {minuto} minuto(s). Motivo: {motivo}", color=discord.Color.green())
        embedpunishments=discord.Embed(title="Mute", description=f"{membro.mention} Foi silenciado por {minuto} minuto(s).", color=discord.Color.red())
        embedpunishments.add_field(name="Motivo:",value=f"{motivo}")
    
        if minuto > 60:

            embedpv=discord.Embed(title="Mute", description=f"Você foi silênciado em **{discord.Guild.name}**. Motivo: {motivo}", color=discord.Color.red())
            embedctx=discord.Embed(title=None, description=f"{membro.mention} Mutado com sucesso por {hora} hora(s). Motivo: {motivo}", color=discord.Color.green())
            embedpunishments=discord.Embed(title="Mute", description=f"{membro.mention} Foi silenciado por {hora} hora(s).", color=discord.Color.red())
            embedpunishments.add_field(name="Motivo:",value=f"{motivo}")

            if hora > 24:

                embedpv=discord.Embed(title="Mute", description=f"Você foi silênciado em **{discord.Guild.name}**. Motivo: {motivo}", color=discord.Color.red())
                embedctx=discord.Embed(title=None, description=f"{membro.mention} Mutado com sucesso por {dia} dia(s). Motivo: {motivo}", color=discord.Color.green())
                embedpunishments=discord.Embed(title="Mute", description=f"{membro.mention} Foi silenciado por {dia} dia(s).", color=discord.Color.red())
                embedpunishments.add_field(name="Motivo:",value=f"{motivo}")

                if dia > 7:

                    embedpv=discord.Embed(title="Mute", description=f"Você foi silênciado em **{discord.Guild.name}**. Motivo: {motivo}", color=discord.Color.red())
                    embedctx=discord.Embed(title=None, description=f"{membro.mention} Mutado com sucesso por {semana} semana(s). Motivo: {motivo}", color=discord.Color.green())
                    embedpunishments=discord.Embed(title="Mute", description=f"{membro.mention} Foi silenciado por {semana} semana(s).", color=discord.Color.red())
                    embedpunishments.add_field(name="Motivo:",value=f"{motivo}")

    try:
        await membro.timeout(until = discord.utils.utcnow() + datetime.timedelta(seconds=time), reason=motivo)
        await ctx.respond(embed=embedctx)
        await punishments.send(embed=embedpunishments)
        try:
            await membro.send(embed=embedpv)
        except:
            await ctx.respond("Não consegui mandar uma mensagem de aviso para este membro. Provavelmente sua DM é bloqueada", ephemeral=True)
    except:
        await ctx.respond("Não tenho permissão para mutar esse usuário", ephemeral=True)
    

@bot.slash_command(description='Des-silência um membro')
@commands.has_permissions(administrator=True)
async def unmute(ctx, membro : Option(discord.Member, description="Escolha um membro")):

    embedpv=discord.Embed(title="Unmute", description=f"Você foi desmutado em **{discord.Guild.name}**.", color=discord.Color.green())
    embedctx=discord.Embed(title=None, description=f"{membro.mention} foi desmutado",color=discord.Color.green())

    try:
        await membro.timeout(until=None)
        await ctx.respond(embed=embedctx)
        try:
            await membro.send(embed=embedpv)
        except:
            await ctx.respond("Não consegui mandar uma mensagem de aviso para este membro. Provavelmente sua DM é bloqueada", ephemeral=True)
    except:
        await ctx.respond("Não tenho permissão para desmutar esse usuário", ephemeral=True)

@bot.slash_command(description='Desativa a permissão de membros falarem neste canal')
@commands.has_permissions(manage_channels=True)
async def lock(ctx):

    embedctx=discord.Embed(title=None, description=f"{ctx.channel.mention} foi trancado", color=discord.Color.red())
  
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.respond(embed=embedctx)

@bot.slash_command(description='Ativa a permissão de membros falarem neste canal')
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):

    embedctx=discord.Embed(title=None, description=f"{ctx.channel.mention} foi destrancado",color=discord.Color.green())
  
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.respond(embed=embedctx)

@bot.slash_command(description='Bane um membro do servidor')
@commands.has_permissions(ban_members=True)
async def ban(ctx, membro : Option(discord.Member, description="Escolha um membro"), motivo=None):

    punishments = ctx.guild.get_channel(1149157075956531231)
  
    embedctx=discord.Embed(title=None, description=f"{membro.mention} foi banido com sucesso", color=discord.Color.green())
    embedpv=discord.Embed(title=None, description=f"Você foi banido de **{discord.Guild.name}**. Motivo: {motivo}", color=discord.Color.red())
    embedpunishments=discord.Embed(title="Ban", description=f"{membro.mention} foi banido do servidor", color=discord.Color.red())
    embedpunishments.add_field(name="Motivo:", value=f"{motivo}", inline=False)

    await ctx.respond(embed=embedctx)
    await punishments.send(embed=embedpunishments)
    await membro.ban(reason=motivo)
    try:
        await membro.send(embed=embedpv)
    except:
        await ctx.respond("Não consegui mandar uma mensagem de aviso para este membro. Provavelmente sua DM é bloqueada", ephemeral=True)

@bot.slash_command(description='Desbane um membro. Use nome e código EX: Wumpus#0000')
@commands.has_permissions(ban_members=True)
async def unban(ctx):

    await ctx.respond("Comando temporariamente desativado por motivos de manutenção", ephemeral=True)


# @bot.slash_command(description='Desbane um membro. Use nome e código EX: Wumpus#0000')
# @commands.has_permissions(ban_members=True)
# async def unban(ctx, membro : Option(str, description="Use nome e código EX: Wumpus#0000", required=True)):

  # punishments = ctx.guild.get_channel(1149157075956531231)
    
#   embedctx=discord.Embed(title=None, description=f"{membro} desbanido com sucesso", color=discord.Color.green())
#   embedpunishments=discord.Embed(title="Unban", description=f"{membro} foi desbanido do servidor", color=discor.Color.green())
  
#   banned_users = await ctx.guild.bans()
#   member_name, member_disc = membro.split('#')

#   for banned_entry in banned_users:
#     user = banned_entry.user
#     if(user.name, user.discriminator)==(member_name, member_disc):
#       await ctx.guild.unban(user)
#       await ctx.respond(embed=embedctx)
#       return
#   await ctx.respond('este usuário não foi banido, ou não foi encontrado. \n **você tem que usar o nome e o código do usuário** ex: Wumpus#0000\n use `/banlist` para saber mais informações', ephemeral=True)

@bot.slash_command(description='Expulsa um membro do servidor')
@commands.has_permissions(kick_members=True)
async def kick(ctx, membro : Option(discord.Member, description="Escolha um membro"), motivo=None):

    punishments = ctx.guild.get_channel(1149157075956531231)
    
    embedctx=discord.Embed(title=None, description=f"{membro.mention} expulso com sucesso", color=discord.Color.red())
    embedpv=discord.Embed(title="Kick", description=f"Você foi expulso de **{discord.Guild.name}**. Motivo: {motivo}", color=discord.Color.red())
    embedpunishments=discord.Embed(title="Kick", description=f"{membro.mention} foi expulso do servidor", color=discord.Color.red())
    embedpunishments.add_field(name="Motivo:", value=f"{motivo}")

    await ctx.respond(embed=embedctx)
    await punishments.send(embed=embedpunishments)
    await membro.kick(reason=motivo)
    try:
        await membro.send(embed=embedpv)
    except:
        await ctx.respond("Não consegui mandar uma mensagem de aviso para este membro. Provavelmente sua DM é bloqueada", ephemeral=True)

@bot.slash_command(description='Adiciona um cargo a alguém')
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, membro : Option(discord.Member, description="Escolha um membro"), cargo : Option(discord.Role, description="Escolha um cargo")):

    embedsuccess=discord.Embed(title=None, description=f"O cargo {cargo.mention} foi adicionado para {membro.mention}", color=discord.Color.green())
    
    embederror=discord.Embed(title=None, description="Você não pode usar esse comando em si mesmo.",color=discord.Color.red())
    
    
    if membro == ctx.author:
        await ctx.respond(embed=embederror, ephemeral=True)
    else:
        await membro.add_roles(cargo)
        await ctx.respond(embed=embedsuccess)

@bot.slash_command(description='Tira um cargo de alguém')
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, membro : Option(discord.Member, description="Escolha um membro"), cargo : Option(discord.Role, description="Escolha um cargo")):

    embedsuccess=discord.Embed(title=None, description=f"O cargo {cargo.mention} foi removido de {membro.mention}", color=discord.Color.green())
    
    embederror=discord.Embed(title=None, description="Você não pode usar esse comando em si mesmo.",color=discord.Color.red())
    
    if membro == ctx.author:
        await ctx.respond(embed=embederror, ephemeral=True)
    else:
        await membro.remove_roles(cargo)
        await ctx.respond(embed=embedsuccess)

# @bot.slash_command(description="Cria um canal de texto")
# @commands.has_permissions(manage_channels=True)
# async def create(ctx, nome : discord.Option(str, description="Nome do canal", required=True), tipo : discord.Option(description="Selecione o tipo de canal", choices=tipos_canal, required=True), cargo : Option(discord.Role, description="Caso o canal for privado, selecione um cargo", required=False)):

#   await ctx.channel_create()

@bot.slash_command(description='Deleta um canal')
@commands.has_permissions(manage_channels=True)
async def delete(ctx):

    embed=discord.Embed(title=None, description=f"Tem certeza que deseja DELETAR {ctx.channel.mention} PARA SEMPRE?",color=discord.Color.red())

    button = Button(label="Sim", style=discord.ButtonStyle.red)
    button2 = Button(label="Não", style=discord.ButtonStyle.gray)

    view = View(timeout=None)
    view.add_item(button)
    view.add_item(button2)

    async def button_callback(interaction):
        await interaction.response.send_message("Deletando canal <a:carregando:957292255901782036>")
        await asyncio.sleep(2)
        await interaction.channel.delete()
        
    button.callback = button_callback

    async def button2_callback(interaction):
        await interaction.response.send_message("Ok, cancelado", ephemeral=True)
    button2.callback = button2_callback

    await ctx.respond(embed=embed, view=view, ephemeral=True)

@bot.slash_command(description="define o modo lento em segundos para o canal atual")
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, tempo : Option(int, description="Escolha a quantidade de tempo em segundos", required=True)):

    await ctx.channel.edit(slowmode_delay=tempo)

    if tempo > 0:
        await ctx.respond(f"Modo lento definido para {tempo} segundos.")
    elif tempo <= 0:
        await ctx.respond("O modo lento foi desligado.")

# TOKEN = os.environ['TOKEN']
# bot.run(TOKEN)

bot.run("MTE0ODQxMTAxNTk4NjQyNTg3Nw.GEKuPR.Ist-5qZpw8U41VRFIjD2Bw1UozsTA0QfaHnnM0")