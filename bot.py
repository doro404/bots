import mercadopago
import json
import string
import telebot
import Levenshtein
import time
import datetime
import shutil
import os
import threading
import random
import api
from api import gn
from os import system
from telebot import types
from telebot.types import InlineKeyboardButton
from telebot.types import InlineKeyboardMarkup
from datetime import timezone
from pytz import timezone
print("Codigo iniciado...")

sdk = mercadopago.SDK(api.CredentialsChange.InfoPix.token_mp())
bot = telebot.TeleBot(api.CredentialsChange.token_bot())
bot.send_message(chat_id=api.CredentialsChange.id_dono(), text='🤖 <b>SEU BOT FOI REINICIADO!</b> 🤖', parse_mode='HTML', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔧 PAINEL ADM', callback_data='voltar_paineladm')]]))

#Painel adm
@bot.message_handler(commands=['admin'])
def painel_admin(message, opcao:str|None=None):
    if opcao == None:
        opcao = 'total'
    if api.Admin.verificar_admin(message.chat.id) == True or int(message.chat.id) == int(api.CredentialsChange.id_dono()):
        if opcao == 'total':
            tipo = 'TOTAL'
            mudar = 'today'
            resp = api.MetricasVendas.total()
            receita, gasto = resp["receita"], resp["gasto"]
        if opcao == 'today':
            tipo = 'HOJE'
            mudar = '7'
            resp = api.MetricasVendas.hoje()
            receita, gasto = resp["receita"], resp["gasto"]
        if opcao == '7':
            tipo = '7 DIAS'
            mudar = '30'
            resp = api.MetricasVendas.sete()
            receita, gasto = resp["receita"], resp["gasto"]
        if opcao == '30':
            tipo = '30 DIAS'
            mudar = 'total'
            resp = api.MetricasVendas.trinta()
            receita, gasto = resp["receita"], resp["gasto"]
        b = InlineKeyboardButton(f'🔄 RECEITA: {tipo}', callback_data=f'mudar_receita {mudar}')
        bt = InlineKeyboardButton('🔧 CONFIGURAÇÕES', callback_data='admin_configuracoes')
        bt2 = InlineKeyboardButton('✍️ MENU DE EDIÇÕES', callback_data='menu_edicoes')
        bt3 = InlineKeyboardButton('🖥 MONITORAMENTO CONTA GN', callback_data='monitoramentognconta')
        bt4 = InlineKeyboardButton('🎁 GIFT CARD 🎁', callback_data='gift_card')
        texto = f'⚙️ <b>PAINEL DE GERENCIAMENTO @{api.CredentialsChange.user_bot()}</b>\n📘 <b>Estatísticas:</b>\n📊 Usuarios: {api.Admin.total_users()}\n📈 <b>Receita <i>({tipo})</i>:</b> R${receita}\n🔻 <b>Gasto na api <i>({tipo})</i>:</b> R${gasto}\n\n🛠 <i>Use os botões abaixo para me configurar</i>'
        markup = InlineKeyboardMarkup([[b], [bt], [bt2], [bt3], [bt4]])
        if message.text != '/admin':
            bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, parse_mode='HTML', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, texto, parse_mode='HTML', reply_markup=markup)
    else:
        bot.reply_to(message, "Você não é um adm!")
        return
@bot.message_handler(commands=['mudar_api'])
def handle_changeapi(message):
    txt = message.text
    if len(txt.split(' ')) == 2:
        api_nova = txt.split(' ')[1]
        with open('settings/credenciais.json', 'r') as f:
            data = json.load(f)
        data["api-sms"] = str(api_nova).strip()
        with open('settings/credenciais.json', 'w') as f:
            json.dump(data, f, indent=4)
        bot.reply_to(message, "Alterado com sucesso!")
    else:
        bot.reply_to(message, "Você enviou em um formato não permitido. Envie:\n\n/mudar_api TOKEN DA API AQUI")
def admin_configuracoes(message):
    bt = InlineKeyboardButton('⚙️ CONFIGURAÇÕES GERAIS ⚙️', callback_data='configuracoes_geral')
    bt2 = InlineKeyboardButton('🕵️ CONFIGURAR ADMINS', callback_data='configurar_admins')
    bt3 = InlineKeyboardButton('👥 CONFIGURAR AFILIADOS', callback_data='configurar_afiliados')
    bt4 = InlineKeyboardButton('👤 CONFIGURAR USUARIOS', callback_data='configurar_usuarios')
    bt5 = InlineKeyboardButton('💠 CONFIGURAR PIX', callback_data='configurar_pix')
    bt6 = InlineKeyboardButton('🖥 CONFIGURAR VALORES', callback_data='configurar_valores')
    bt7 = InlineKeyboardButton('🚨 AVISO DE SALDO (api)', callback_data='configurar_aviso_saldo_api')
    bt8 = InlineKeyboardButton('🔙 VOLTAR', callback_data='voltar_paineladm')
    markup = InlineKeyboardMarkup([[bt], [bt2], [bt3], [bt4], [bt5], [bt6], [bt7], [bt8]])
    admin = 'Não'
    dono = 'Não'
    if message.chat.id == api.CredentialsChange.id_dono():
        dono = 'Sim'
    if api.Admin.verificar_admin(message.chat.id) == True:
        admin = 'Sim'
    txt = f'🛠 <b>MENU DE CONFIGURAÇÕES DO BOT</b>\n\n👮‍♀️ <b>Admin:</b> {admin}\n💼 <b>Dono:</b> {dono}'
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=txt, parse_mode='HTML', reply_markup=markup)
def menu_edicoes(message):
    bt = InlineKeyboardButton('✍️ EDITAR TEXTOS', callback_data='configurar_textos')
    bt3 = InlineKeyboardButton('📣 EDITAR LOGS', callback_data='configurar_log')
    bt2 = InlineKeyboardButton('📥 EDITAR BOTÕES', callback_data='configurar_botoes')
    bt5 = InlineKeyboardButton('🔙 VOLTAR', callback_data='voltar_admin_acoes')
    markup = InlineKeyboardMarkup([[bt], [bt2], [bt3], [bt5]])
    text = 'Esse menu é exclusivo para as edições do bot, tais como: Edições de textos, edições de botões, edições das mensagens de log\n\n<i>Selecione abaixo o que deseja editar</i>'
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, parse_mode='HTML', reply_markup=markup)
def configurar_valores(message):
    porcentagem = api.InfoApi.porcentagem_lucro()
    texto = f'📊 <b>Porcentagem de lucro atual:</b> {porcentagem}%\n\n<i>Valor já convertido em BRL</i>'
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, parse_mode='HTML', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔄 ALTERAR PORCENTAGEM', callback_data='alterar_porcentagem')], [InlineKeyboardButton(f'{api.Botoes.voltar()}', callback_data='admin_configuracoes')]]))
def alterar_porcentagem(message):
    nova_porcentagem = message.text
    porcent = nova_porcentagem.replace('%', '').strip()
    api.InfoApi.mudar_porcentagem_lucro(porcent)
    bot.reply_to(message, "Alterado com sucesso!")
#Menu Geral
def configuracoes_geral(message):
    texto = f'<i>Use os botões abaixo para configurar seu bot:</i>\n👤 <b>LINK DO SUPORTE ATUAL: {api.CredentialsChange.SuporteInfo.link_suporte()}</b>'
    bt = InlineKeyboardButton('🔴 MANUTENÇÃO (off)', callback_data='manutencao')
    if api.CredentialsChange.status_manutencao() == True:
        bt = InlineKeyboardButton('🟢 MANUTENÇÃO (on)', callback_data='manutencao')
    b = InlineKeyboardButton('🤖 REINICIAR BOT 🤖', callback_data='reiniciar_bot')
    bt1 = InlineKeyboardButton('🎧 MUDAR SUPORTE', callback_data='suporte')
    bt4 = InlineKeyboardButton('📸 MUDAR FOTO DO MENU START', callback_data='mudar_foto_menu')
    bt5 = InlineKeyboardButton('🔙 VOLTAR', callback_data='voltar_painel_configuracoes')
    markup = InlineKeyboardMarkup([[b], [bt], [bt1], [bt4], [bt5]])
    bot.edit_message_text(chat_id=message.chat.id, text=texto, message_id=message.message_id, reply_markup=markup, parse_mode='HTML', disable_web_page_preview=True)
def trocar_suporte(message, idcall):
    suporte = message.text
    api.CredentialsChange.SuporteInfo.mudar_link_suporte(str(suporte))
    bot.answer_callback_query(idcall, text="Suporte alterado com sucesso!", show_alert=True)
def mudar_foto_menu(message):
    if message.text.startswith('htt'):
        url = message.text
        markup = InlineKeyboardMarkup([[InlineKeyboardButton("CONFIRMAR", callback_data=f'c-p-m {url}')]])
        bot.send_photo(message.chat.id, url, caption="<b>Essa será a nova foto do menu inicial, você confirma?</b>", parse_mode='HTML', reply_markup=markup)
    else:
        bot.reply_to(message, "Envie uma url válida!")
#Menu admin
def configurar_admins(message):
    texto = f'🅰️ <b>PAINEL CONFIGURAR ADMIN</b>\n\n👮 Administradores: {api.Admin.quantidade_admin()}\n<i>Use os botões abaixo para fazer as alterações necessárias</i>'
    bt = InlineKeyboardButton('➕ ADICIONAR ADM', callback_data='adicionar_adm')
    bt2 = InlineKeyboardButton('🚮 REMOVER ADM', callback_data='remover_adm')
    bt3 = InlineKeyboardButton('📃 LISTA DE ADM', callback_data='lista_adm')
    bt4 = InlineKeyboardButton('🔙 VOLTAR', callback_data='voltar_painel_configuracoes')
    markup = InlineKeyboardMarkup([[bt], [bt2], [bt3], [bt4]])
    bot.edit_message_text(chat_id=message.chat.id, text=texto, message_id=message.message_id, parse_mode='HTML', reply_markup=markup)
def adicionar_adm(message):
    try:
        id_admin = message.text
        api.Admin.add_admin(id_admin)
        bot.reply_to(message, f"O usuario: {id_admin} foi feito admin!")
    except:
        bot.reply_to(message, "Erro ao promover para adm.")
def remover_adm(message):
    try:
        id = message.text
        api.Admin.remover_admin(id)
        bot.reply_to(message, f"Adm {id} foi feito um usuario comum novamente.")
    except:
        bot.reply_to(message, "Falha ao remover o adm.")
#Menu afiliados
def configurar_afiliados(message):
    texto = f'◎ ══════ ❈ ══════ ◎\n🗞 <b>PORCENTAGEM POR INDICAÇÃO</b>\n◎ ══════ ❈ ══════ ◎\nEssa é a porcentagem de ganhos que o usuário recebe cada vez que o seu afiliado fizer uma recarga.\n┕━━━━╗✹╔━━━━┙'
    bt = InlineKeyboardButton('🗞 PORCENTAGEM POR RECARGA', callback_data='porcentagem_por_indicacao')
    bt2 = InlineKeyboardButton('🔙 VOLTAR', callback_data='voltar_painel_configuracoes')
    markup = InlineKeyboardMarkup([[bt], [bt2]])
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, parse_mode='HTML', reply_markup=markup)
def porcentagem_por_indicacao(message):
    try:
        pontos = message.text
        api.AfiliadosInfo.mudar_porcentagem_por_indicacao(pontos)
        bot.reply_to(message, f"Alterado com sucesso! Agora toda vez que um usuário recarregar, quem indicou ele ganhará {pontos}% da recarga.")
    except Exception as e:
        print(e)
        bot.reply_to(message, "Falha ao alterar a quantidade de pontos, verifique se enviou um número aceitavel.")
def pontos_minimo_converter(message):
    try:
        min = message.text
        api.AfiliadosInfo.trocar_minimo_pontos_pra_saldo(min)
        bot.reply_to(message, f"Feito! Agora os usuarios precisam ter {min} pontos para poder converter em saldo.")
    except:
        bot.reply_to(message, f"Erro ao alterar a quantidade de pontos, verifique se enviou um número aceitavel.")
def multiplicador_para_converter(message):
    try:
        mult = message.text
        api.AfiliadosInfo.trocar_multiplicador_pontos(mult)
        bot.reply_to(message, "Multiplicador alterado com sucesso!")
    except:
        bot.reply_to(message, "Falha ao alterar o multiplicador, verifique se enviou um número aceitavel.")
#Menu usuarios
def configurar_usuarios(message):
    texto = f'◎ ══════ ❈ ══════ ◎\n📪 <b>TRANSMITIR A TODOS</b>\n◎ ══════ ❈ ══════ ◎\nEnvia uma mensagem para todos os usuários registrados no bot. 📬✉️\nApós clicar, envie o texto que quer transmitir ou a foto. Para enviar uma foto com texto, basta colocar o texto na legenda da imagem. 📷🖋️\n┕━━━━╗✹╔━━━━┙\n\n\n◎ ══════ ❈ ══════ ◎\n🔎 <b>PESQUISAR USUÁRIO</b>\n◎ ══════ ❈ ══════ ◎\nSe este usuário estiver registrado no bot, vai abrir as configurações de edição desse usuário. 💼🔧\nVocê poderá editar o saldo, ver o histórico de compras, e todas as informações dele. 📈📋\n┕━━━━╗✹╔━━━━┙\n\n\n◎ ══════ ❈ ══════ ◎\n🎁 <b>BÔNUS DE REGISTRO</b>\n◎ ══════ ❈ ══════ ◎\nBônus atual: R${api.CredentialsChange.BonusRegistro.bonus():.2f}\n<i>Bônus de registro é o valor que cada usuário novo ganhará apenas por se registrar, é um bônus de boas-vindas.</i>\nPara não dar bônus nenhum, deixe em 0\n┕━━━━╗✹╔━━━━┙'
    bt = InlineKeyboardButton('📫 TRANSMITIR A TODOS', callback_data='transmitir_todos')
    bt2 = InlineKeyboardButton('🔎 PESQUISAR USUARIO', callback_data='pesquisar_usuario')
    bt3 = InlineKeyboardButton('🎁 BONUS DE REGISTRO', callback_data='mudar_bonus_registro')
    bt4 = InlineKeyboardButton('🔙 VOLTAR', callback_data='voltar_painel_configuracoes')
    markup = InlineKeyboardMarkup([[bt], [bt2], [bt3], [bt4]])
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, reply_markup=markup, parse_mode='HTML')
def transmitir_todos(message):
    api.FuncaoTransmitir.zerar_infos()
    bt = InlineKeyboardButton('➕ ADD BOTAO ➕', callback_data='add_botao')
    bt2 = InlineKeyboardButton('✅ CONFIRMAR ENVIO', callback_data='confirmar_envio')
    markup = InlineKeyboardMarkup([[bt], [bt2]])
    if message.content_type == 'photo':
        photo = message.photo[0].file_id
        api.FuncaoTransmitir.adicionar_foto(photo)
        api.FuncaoTransmitir.adicionar_texto(message.caption)
        bot.send_photo(message.chat.id, photo=photo, caption=message.caption, reply_markup=markup, parse_mode='HTML')
    elif message.content_type == 'text':
        api.FuncaoTransmitir.adicionar_texto(message.text)
        bot.send_message(message.chat.id, text=message.text, reply_markup=markup, parse_mode='HTML')
    else:
        bot.reply_to(message, "Este tipo de mensagem ainda não está disponível para transmitir.")
def add_botao(message):
    try:
        text = message.text
        s = text.split('\n')
        markup = InlineKeyboardMarkup()
        for elemento in s:
            botoes = []
            separar = elemento.split('&&')
            for botao in separar:
                sep = botao.split('-')
                nome = sep[0].strip()
                url = sep[1].strip()
                botoes.append(InlineKeyboardButton(f'{nome}', url=f'{url}'))
            markup.row(*botoes)
        api.FuncaoTransmitir.adicionar_markup(markup)
        bt2 = InlineKeyboardButton('✅ CONFIRMAR ENVIO', callback_data='confirmar_envio')
        markup.row(bt2)
        if markup != None:
            texto = api.FuncaoTransmitir.pegar_texto()
            photo = api.FuncaoTransmitir.pegar_foto()
            if texto != None and photo == None:
                bot.send_message(message.chat.id, texto, reply_markup=markup, parse_mode='HTML')
            elif photo != None and texto == None:
                bot.send_photo(message.chat.id, photo, reply_markup=markup, parse_mode='HTML')
            elif photo != None and texto != None:
                bot.send_photo(message.chat.id, photo, caption=texto, reply_markup=markup, parse_mode='HTML')
            else:
                bot.reply_to(message, "Error!")
    except Exception as e:
        bot.reply_to(message, "Ocorreu um erro ao processar, verifique se enviou o nome e a URL no formato correto.")
        print(e)
enviando_transmissao = False
def confirmar_envio(message):
    global enviando_transmissao
    markup1 = api.FuncaoTransmitir.pegar_markup()
    markup = InlineKeyboardMarkup()
    if markup1 != None:
        for bt in markup1:
            buttons = []
            for b in bt:
                buttons.append(InlineKeyboardButton(b["text"], url=b["url"]))
            markup.row(*buttons)
    else:
        markup = None
    texto = api.FuncaoTransmitir.pegar_texto()
    photo = api.FuncaoTransmitir.pegar_foto()
    with open('database/users.json', 'r') as f:
        data = json.load(f)
    enviando_transmissao = True
    msg = bot.send_message(message.chat.id, "<i>Enviando transmissão</i>", parse_mode='HTML')
    threading.Thread(target=enviar_status_transmissao, args=(msg,)).start()
    for user in data["users"]:
        try:
            if photo == None:
                bot.send_message(user["id"], texto, parse_mode='HTML', reply_markup=markup)
            else:
                bot.send_photo(user["id"], photo, caption=texto, parse_mode='HTML', reply_markup=markup)
        except Exception as e:
            print(e)
            pass
    enviando_transmissao = False
def enviar_status_transmissao(message):
    global enviando_transmissao
    while True:
        if enviando_transmissao == False:
            bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="✅ <b>Transmissão finalizada!</b>", parse_mode='HTML')
            break
        else:
            try:
                time.sleep(1.2)
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="<i>Enviando transmissão.</i>", parse_mode='HTML')
                time.sleep(1.2)
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="<i>Enviando transmissão..</i>", parse_mode='HTML')
                time.sleep(1.2)
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="<i>Enviando transmissão...</i>", parse_mode='HTML')
            except:
                break
    return
def pesquisar_usuario(message):
    id = message.text
    if api.InfoUser.verificar_usuario(id) == True:
        texto = f'🔎 <b>USUÁRIO ENCONTRADO</b> ✅\n\n🕵️ <b>INFORMAÇÕES</b> 🕵️\n📛 <b>ID:</b> <code>{id}</code>\n💰 <b>SALDO:</b> <code>{api.InfoUser.saldo(id):.2f}</code>\n🛒 <b>ACESSOS COMPRADOS:</b> <code>{api.InfoUser.total_compras(id)}</code>\n💠 <b>PIX INSERIDOS:</b> <code>R${api.InfoUser.pix_inseridos(id):.2f}</code>\n👥 <b>INDICADOS:</b> <code>{api.InfoUser.quantidade_afiliados(id)}</code>\n🎁 <b>GIFT RESGATADO:</b> <code>R${api.InfoUser.gifts_resgatados(id):.2f}</code>'
        bt = InlineKeyboardButton('🧑‍⚖️ Banir', callback_data=f'banir {id}')
        bt2 = InlineKeyboardButton('💰 MUDAR SALDO', callback_data=f'mudar_saldo {id}')
        bt3 = InlineKeyboardButton('📥 BAIXAR HISTORICO', callback_data=f'baixar_historico {id}')
        markup = InlineKeyboardMarkup([[bt], [bt2], [bt3]])
        if api.InfoUser.verificar_ban(id) == True:
            bt = InlineKeyboardButton('🧑‍⚖️ DESBANIR', callback_data=f'banir {id}')
            markup = InlineKeyboardMarkup([[bt]])
        bot.send_message(chat_id=message.chat.id, text=texto, parse_mode='HTML', reply_markup=markup)
    else:
        bot.reply_to(message, "Usuario não foi encontrado.")
def mudar_saldo(message, id):
    saldo = message.text
    try:
        api.InfoUser.mudar_saldo(id, saldo)
        bot.reply_to(message, "Saldo alterado com sucesso!")
    except:
        bot.reply_to(message, "Falha ao alterar, verifique se enviou um valor valido.")
#Menu Pix
def configurar_pix(message):
    texto = f'🔑 <b>TOKEN MERCADO PAGO:</b> <code>{api.CredentialsChange.InfoPix.token_mp()}</code>\n🔻 <b>DEPÓSITO MÍNIMO:</b> <code>R${api.CredentialsChange.InfoPix.deposito_minimo_pix():.2f}</code>\n❗️ <b>DEPÓSITO MÁXIMO:</b> <code>R${api.CredentialsChange.InfoPix.deposito_maximo_pix():.2f}</code>\n⏰ <b>TEMPO DE EXPIRAÇÃO:</b> <i>{api.CredentialsChange.InfoPix.expiracao()} Minutos</i>\n🔶 <b>BÔNUS DE DEPÓSITO:</b> <code>{api.CredentialsChange.BonusPix.quantidade_bonus()}%</code>\n🔷 <b>DEPÓSITO MÍNIMO PARA GANHAR O BÔNUS:</b> R${api.CredentialsChange.BonusPix.valor_minimo_para_bonus():.2f}'
    bt = InlineKeyboardButton('🔴 PIX MANUAL', callback_data='trocar_pix_manual')
    bt2 = InlineKeyboardButton('🔴 PIX AUTOMATICO', callback_data='trocar_pix_automatico')
    if api.CredentialsChange.StatusPix.pix_manual() == True:
        bt = InlineKeyboardButton('🟢 PIX MANUAL', callback_data='trocar_pix_manual')
    if api.CredentialsChange.StatusPix.pix_auto() == True:
        bt2 = InlineKeyboardButton('🟢 PIX AUTOMATICO', callback_data='trocar_pix_automatico')
    bt3 = InlineKeyboardButton('🔴 PIX GN', callback_data='mudar_pix_gn_status')
    bt4 = InlineKeyboardButton('🔴 PIX MP', callback_data='mudar_pix_mp_status')
    if api.CredentialsChange.PlataformaPix.status_gn() == True:
        bt3 = InlineKeyboardButton('🟢 PIX GN', callback_data='mudar_pix_gn_status')
    if api.CredentialsChange.PlataformaPix.status_mp() == True:
        bt4 = InlineKeyboardButton('🟢 PIX MP', callback_data='mudar_pix_mp_status')
    bt5 = InlineKeyboardButton('🔻 MUDAR DEPOSITO MIN', callback_data='mudar_deposito_minimo')
    bt6 = InlineKeyboardButton('❗️ MUDAR DEPOSITO MAX', callback_data='mudar_deposito_maximo')
    bt7 = InlineKeyboardButton('🔶 MUDAR BONUS', callback_data='mudar_bonus')
    bt8 = InlineKeyboardButton('🔷 MUDAR MIN PARA BONUS', callback_data='mudar_min_bonus')
    bt9 = InlineKeyboardButton('🔙 VOLTAR', callback_data='voltar_painel_configuracoes')
    markup = InlineKeyboardMarkup([[bt, bt2], [bt3, bt4], [bt5], [bt6], [bt7], [bt8], [bt9]])
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, parse_mode='HTML', reply_markup=markup)
def mudar_token(message):
    try:
        token = message.text
        api.CredentialsChange.InfoPix.mudar_tokenmp(token)
        bot.reply_to(message, "Alterado com sucesso")
    except Exception as e:
        print(e)
        bot.reply_to(message, "Falha ao alterar")
def mudar_deposito_minimo(message):
    try:
        min = message.text
        api.CredentialsChange.InfoPix.trocar_deposito_minimo_pix(min)
        bot.reply_to(message, "Alterado com sucesso!")
    except Exception as e:
        print(e)
        bot.reply_to(message, "Falha ao alterar")
def mudar_deposito_maximo(message):
    try:
        max = message.text
        api.CredentialsChange.InfoPix.trocar_deposito_maximo_pix(max)
        bot.reply_to(message, "Alterado com sucesso")
    except Exception as e:
        print(e)
        bot.reply_to(message, "Falha ao alterar")
def mudar_expiracao(message):
    if message.text.isdigit() == True:
        expiracao = int(message.text)
        if expiracao < 15:
            bot.reply_to(message, "O tempo de expiracao deve ser maior do que 15 minutos!")
            return
        api.CredentialsChange.InfoPix.mudar_expiracao(expiracao)
        bot.reply_to(message, "Alterado com sucesso!")
    else:
        bot.reply_to(message, "Envie apenas digitos!")
def mudar_bonus(message):
    try:
        p = message.text
        p = p.replace('%', '')
        p = p.strip()
        api.CredentialsChange.BonusPix.mudar_quantidade_bonus(p)
        bot.reply_to(message, "Alterado com sucesso!")
    except Exception as e:
        print(e)
        bot.reply_to(message, "Falha ao alterar")
def mudar_min_bonus(message):
    try:
        min = message.text
        api.CredentialsChange.BonusPix.mudar_valor_minimo_para_bonus(min)
        bot.reply_to(message, "Alterado com sucesso")
    except Exception as e:
        print(e)
        bot.reply_to(message, "Falha ao alterar")
# Menu texto
def configurar_textos(message):
    texto = 'Selecione o menu que deseja editar o texto:'
    bt = InlineKeyboardButton('MENU START', callback_data='mudar_texto start')
    bt2 =  InlineKeyboardButton('MENU PERFIL', callback_data='mudar_texto perfil')
    bt3 = InlineKeyboardButton('MENU ADD SALDO', callback_data='mudar_texto addsaldo')
    bt4 = InlineKeyboardButton('MENSAGEM PIX MANUAL', callback_data='mudar_texto pixmanual')
    bt5 = InlineKeyboardButton('MENSAGEM PIX AUTOMATICO', callback_data='mudar_texto pixauto')
    bt6 = InlineKeyboardButton('PAGAMENTO EXPIRADO', callback_data='mudar_texto pagamento_expirado')
    bt7 = InlineKeyboardButton('PAGAMENTO APROVADO', callback_data='mudar_texto pagamento_aprovado')
    bt8 = InlineKeyboardButton('MENU COMPRAR', callback_data='mudar_texto comprar')
    bt9 = InlineKeyboardButton('MENU EXIBIR SERVICOS', callback_data='mudar_texto exibir_servico')
    bt10 = InlineKeyboardButton('MENSAGEM COM ENTREGA DO NUMERO', callback_data='mudar_texto mensagem_comprou')
    bt11 = InlineKeyboardButton('TERMOS', callback_data='mudar_texto termos')
    bt12 = InlineKeyboardButton('AJUDA', callback_data='mudar_texto ajuda')
    bt13 = InlineKeyboardButton('ID', callback_data='mudar_texto id')
    bt14 = InlineKeyboardButton('SALDO', callback_data='mudar_texto saldo')
    bt15 = InlineKeyboardButton('AFILIADOS', callback_data='mudar_texto afiliados')
    bt16 = InlineKeyboardButton('🔙 VOLTAR', callback_data='voltar_menuedicoes')
    markup = InlineKeyboardMarkup([[bt], [bt2], [bt3], [bt4], [bt5], [bt6], [bt7], [bt8], [bt9], [bt10], [bt11], [bt12], [bt13], [bt14], [bt15], [bt16]])
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, parse_mode='HTML', reply_markup=markup)
def mudar_texto(message, tipo):
    if tipo == 'start':
        api.MudarTexto.start(message.text)
    if tipo == 'perfil':
        api.MudarTexto.perfil(message.text)
    if tipo == 'addsaldo':
        api.MudarTexto.adicionar_saldo(message.text)
    if tipo == 'pixmanual':
        api.MudarTexto.pix_manual(message.text)
    if tipo == 'pixauto':
        api.MudarTexto.pix_automatico(message.text)
    if tipo == 'pagamento_expirado':
        api.MudarTexto.pagamento_expirado(message.text)
    if tipo == 'pagamento_aprovado':
        api.MudarTexto.pagamento_aprovado(message.text)
    if tipo == 'comprar':
        api.MudarTexto.menu_comprar(message.text)
    if tipo == 'exibir_servico':
        api.MudarTexto.exibir_servico(message.text)
    if tipo == 'mensagem_comprou':
        api.MudarTexto.mensagem_comprou(message.text)
    if tipo == 'termos':
        api.MudarTexto.termos(message.text)
    if tipo == 'ajuda':
        api.MudarTexto.ajuda(message.text)
    if tipo == 'id':
        api.MudarTexto.id(message.text)
    if tipo == 'afiliados':
        api.MudarTexto.afiliados(message.text)
    if tipo == 'saldo':
        api.MudarTexto.saldo(message.text)
    bot.reply_to(message, "Alterado com sucesso!")
#Menu botão
def mudar_botao(message, tipo):
    if tipo == 'comprar':
        api.MudarBotao.comprar(message.text)
    if tipo == 'perfil':
        api.MudarBotao.perfil(message.text)
    if tipo == 'paises':
        api.MudarBotao.paises(message.text)
    if tipo == 'addsaldo':
        api.MudarBotao.addsaldo(message.text)
    if tipo == 'suporte':
        api.MudarBotao.suporte(message.text)
    if tipo == 'comprarlogin':
        api.MudarBotao.comprar_login(message.text)
    if tipo == 'pixmanual':
        api.MudarBotao.pix_manual(message.text)
    if tipo == 'pixautomatico':
        api.MudarBotao.pix_automatico(message.text)
    if tipo == 'download':
        api.MudarBotao.download_historico(message.text)
    if tipo == 'trocarpontos':
        api.MudarBotao.trocar_pontos_por_saldo(message.text)
    if tipo == 'suporte':
        api.MudarBotao.suporte(message.text)
    if tipo == 'aguardando_pagamento':
        api.MudarBotao.aguardando_pagamento(message.text)
    bot.reply_to(message, "Alterado com sucesso!")
#Menu gift card
def gift_card(message):
    bt = InlineKeyboardButton('🎁 GERAR GIFT CARD', switch_inline_query_current_chat='CREATEGIFT 1')
    bt2 = InlineKeyboardButton('🎁 GERAR VARIOS GIFT 🎁', switch_inline_query_current_chat='CREATEGIFT 1 10')
    bt3 = InlineKeyboardButton('♟ GIFTS CRIADOS', callback_data='gifts_criados')
    bt4 = InlineKeyboardButton('🔙 VOLTAR', callback_data='admin_transacoes')
    markup = InlineKeyboardMarkup([[bt], [bt2], [bt3], [bt4]])
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='<i>Selecione a opção desejada:</i>', parse_mode='HTML', reply_markup=markup)
@bot.inline_handler(lambda query: query.query.startswith('CREATEGIFT '))
def create_gift_card(inline_query):
    if api.Admin.verificar_admin(inline_query.from_user.id) == False and int(api.CredentialsChange.id_dono()) != int(inline_query.from_user.id):
        return
    if len(inline_query.query.split()) == 2:
        value = inline_query.query.split(' ')[1]
        valor, codigo = gerar_gift_card(value)
        txt = f'🎁 <b>GIFT CARD GERADO</b> 🎁\n\n💰 <b>Valor:</b> <i>R${value}</i>\n🤑 <b>Codigo:</b> <code>{codigo}</code>'
        title = f"Criar gift card de {value}"
        description = f"Clique aqui para criar um gift card de {value}."
        reply_markup = telebot.types.InlineKeyboardMarkup()
        button_text = "📝 Resgatar agora"
        button = telebot.types.InlineKeyboardButton(button_text, callback_data=f'resgatar {codigo}')
        reply_markup.add(button)
        result_id = '1'
        try:
            result = telebot.types.InlineQueryResultArticle(id=result_id, title=title, description=description, input_message_content=telebot.types.InputTextMessageContent(txt, parse_mode='HTML'), reply_markup=reply_markup, thumbnail_url='https://cdn-icons-png.flaticon.com/512/612/612886.png')
        except:
            result = telebot.types.InlineQueryResultArticle(id=result_id, title=title, description=description, input_message_content=telebot.types.InputTextMessageContent(txt, parse_mode='HTML'), reply_markup=reply_markup, thumb_url='https://cdn-icons-png.flaticon.com/512/612/612886.png')
        bot.answer_inline_query(inline_query.id, [result], cache_time=0)
    else:
        value = inline_query.query.split(' ')[1]
        quantidade = inline_query.query.split(' ')[2]
        codigo = gerar_muito_gift(quantidade, value)
        txt = f'🎁 <b>GIFT CARD GERADO</b> 🎁\n\n💰 <b>Valor:</b> <i>R${value}</i>\n🤑 <b>Codigos:</b>\n<code>{codigo}</code>'
        title = f"Criar {quantidade} gifts cards de R${float(value):.2f}"
        description = f"Clique aqui para criar {quantidade} gift card de R${float(value):.2f}."
        result_id = '3'
        try:
            result = telebot.types.InlineQueryResultArticle(id=result_id, title=title, description=description, input_message_content=telebot.types.InputTextMessageContent(txt, parse_mode='HTML'), thumbnail_url='https://cdn-icons-png.flaticon.com/512/1261/1261149.png')
        except:
            result = telebot.types.InlineQueryResultArticle(id=result_id, title=title, description=description, input_message_content=telebot.types.InputTextMessageContent(txt, parse_mode='HTML'), thumb_url='https://cdn-icons-png.flaticon.com/512/1261/1261149.png')
        bot.answer_inline_query(inline_query.id, [result])
def gerar_muito_gift(quantidade, valor):
    codigos = ''
    for i in range(int(quantidade)):
        while True:
            codigo = random.choices(string.ascii_uppercase + string.digits, k=9)
            codigo = ''.join(codigo)
            if api.GiftCard.validar_gift(codigo)[0] == False:
                api.GiftCard.create_gift(codigo, float(valor))
                codigos += f'\n{codigo}'
                break
            else:
                continue
    return codigos
def gerar_gift_card(valor):
    while True:
        codigo = random.choices(string.ascii_uppercase + string.digits, k=9)
        codigo = ''.join(codigo)
        if api.GiftCard.validar_gift(codigo)[0] == False:
            api.GiftCard.create_gift(codigo, float(valor))
            break
        else:
            continue
    return f'R${int(valor)},00', codigo
@bot.message_handler(commands=['resgatar'])
def redeem_gift(message):
    msg = message.text.strip().split()
    if len(msg) != 2:
        bot.reply_to(message, "Erro, envie no formato correto.\nex: /resgatar 1isjue")
        return
    codigo = msg[1]
    processar_resgate(message.chat.id, codigo)
def processar_resgate(id, codigo):
    verif, valor = api.GiftCard.validar_gift(codigo)
    if verif == True:
        api.GiftCard.del_gift(codigo)
        api.MudancaHistorico.mudar_gift_resgatado(id, float(valor))
        api.InfoUser.add_saldo(id, valor)
        bot.send_message(int(id), f'🎉 <b>Parabéns!</b>\nVocê resgatou o Gift Card com sucesso ✅\n\n💰 <b>Valor:</b> {valor:.2f}\n📔 <b>Código: </b>{codigo}', parse_mode='HTML')
        bot.send_message(int(api.CredentialsChange.id_dono()), f'⚠️ <b>GIFT CARD RESGATADO</b> 🙋\nUsuario: {id} acabou de resgatar o gift card: {codigo} e obteve um saldo de R${valor:.2f}', parse_mode='HTML')
    else:
        bot.send_message(id, "Gift card invalido ou ja resgatado!")
        return
@bot.message_handler(commands=['start','menu', f'start@{api.CredentialsChange.user_bot()}'])
def handle_start(message):
    if api.InfoUser.verificar_usuario(message.from_user.id) == False:
        api.InfoUser.novo_usuario(message.from_user.id)
        if len(message.text.split()) == 2:
            if message.text.split()[1].isdigit():
                if message.text.split()[1] != message.from_user.id:
                    api.InfoUser.novo_afiliado(message.from_user.id, message.text.split()[1])
        try:
            bot.send_message(chat_id=api.Log.destino_log_registro(), text={api.Log.log_registro(message)}, parse_mode='HTML')
        except Exception as e:
            bot.send_message(api.Log.destino_log_registro(), f"Log não enviada!\nMotivo: {e}")
            pass
        api.InfoUser.add_saldo(message.from_user.id, float(api.CredentialsChange.BonusRegistro.bonus()))
    if api.InfoUser.verificar_ban(message.from_user.id) == True:
        bot.reply_to(message, "Você está banido neste bot e não pode utiliza-lo!")
        return
    if api.CredentialsChange.status_manutencao() == True:
        if api.Admin.verificar_admin(message.from_user.id) == False:
            if api.CredentialsChange.id_dono() != int(message.from_user.id):
                bot.reply_to(message, "O bot esta em manutenção, voltaremos em breve!")
                return
        bot.reply_to(message, "O bot está em manutenção, mas você foi identificado como administrador!")
    texto = api.Textos.start(message)
    bt_servicos = InlineKeyboardButton(f'{api.Botoes.comprar()}', callback_data='servicos')
    bt_paises = InlineKeyboardButton(f'{api.Botoes.paises()}', callback_data='paises')
    bt_pesquisar = InlineKeyboardButton(f'{api.Botoes.pesquisar_numero()}', switch_inline_query_current_chat='')
    bt_historico = InlineKeyboardButton('📝 Histórico', callback_data='historico_user')
    bt_suporte = InlineKeyboardButton(f'{api.Botoes.suporte()}', url=f'{api.CredentialsChange.SuporteInfo.link_suporte()}')
    bt_add_saldo = InlineKeyboardButton(f'{api.Botoes.addsaldo()}', callback_data='addsaldo')
    bt_ranking = InlineKeyboardButton('🏆 Ranking', callback_data='ranking_sms')
    bt_afiliados = InlineKeyboardButton('👥 Afiliados', callback_data='afiliados')
    bt_perfil = InlineKeyboardButton(f'{api.Botoes.perfil()}', callback_data='perfil')
    markup = InlineKeyboardMarkup([[bt_servicos, bt_paises], [bt_pesquisar], [bt_historico, bt_suporte], [bt_add_saldo], [bt_ranking, bt_afiliados], [bt_perfil]])
    foto = api.CredentialsChange.FotoMenu.foto_atual()
    if message.from_user.is_bot == True:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_photo(message.chat.id, foto, caption=texto, parse_mode='HTML', reply_markup=markup)
        return
    bot.send_photo(message.chat.id, foto, caption=texto, parse_mode='HTML', reply_markup=markup)
@bot.message_handler(func=lambda message: message.text in ['👤 Perfil'])
def perfil(message):
    markup = InlineKeyboardMarkup()
    if api.AfiliadosInfo.status_afiliado() == True:
        bt2 = InlineKeyboardButton(f'{api.Botoes.trocar_pontos_por_saldo()}', callback_data=f'trocar_pontos')
        markup.add(bt2)
    bt3 = InlineKeyboardButton(f'{api.Botoes.voltar()}', callback_data='menu_start')
    markup.add(bt3)
    texto = api.Textos.perfil(message)
    if message.text == '/perfil' or message.text=='👤 Perfil':
        bot.send_message(chat_id=message.chat.id, text=texto, parse_mode='HTML', reply_markup=markup)
    else:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(chat_id=message.chat.id, text=texto, parse_mode='HTML', reply_markup=markup)
@bot.message_handler(func=lambda message: message.text in ['/servicos', '🔥 Serviços'])
def servicos(message):
    pais = api.InfoUser.pegar_pais_atual(message.chat.id)
    servicos_ordenados = sorted(api.InfoApi.servicos(pais), key=lambda x: x["nome"])
    mostrar_servicos(message, servicos_ordenados, 0)
def mostrar_servicos(message, servicos, pagina):
    chat_id = message.chat.id
    num_botoes_max = 30
    inicio = pagina * num_botoes_max
    fim = (pagina + 1) * num_botoes_max
    servicos_pagina = servicos[inicio:fim]
    markup = InlineKeyboardMarkup()
    for i in range(0, len(servicos_pagina), 2):
        servico1 = servicos_pagina[i]
        id1 = servico1["id"]
        nome1 = servico1["nome"]
        valor1 = servico1["valor"]
        bt1 = InlineKeyboardButton(f'{nome1} R${float(valor1):.2f}', callback_data=f'exibir_servico {id1}')
        if i + 1 < len(servicos_pagina):
            servico2 = servicos_pagina[i + 1]
            id2 = servico2["id"]
            nome2 = servico2["nome"]
            valor2 = servico2["valor"]
            bt2 = InlineKeyboardButton(f'{nome2} R${float(valor2):.2f}', callback_data=f'exibir_servico {id2}')
            markup.row(bt1, bt2)
        else:
            markup.row(bt1)
    if pagina > 0:
        bt_anterior = InlineKeyboardButton('◀️ Página Anterior', callback_data=f'pagina_servicos {pagina - 1}')
        markup.row(bt_anterior)
    if len(servicos) > (pagina + 1) * num_botoes_max:
        bt_proxima = InlineKeyboardButton('▶️ Próxima Página', callback_data=f'pagina_servicos {pagina + 1}')
        markup.row(bt_proxima)
    if message.from_user.is_bot and message.photo == None:
        bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=api.Textos.menu_comprar(message), reply_markup=markup, parse_mode='HTML')
    else:
        bot.send_message(chat_id, api.Textos.menu_comprar(message), reply_markup=markup, parse_mode='HTML')
@bot.callback_query_handler(func=lambda call: call.data.startswith('pagina_servicos'))
def callback_pagina_servicos(call):
    pais = api.InfoUser.pegar_pais_atual(call.message.chat.id)
    servicos_ordenados = sorted(api.InfoApi.servicos(pais), key=lambda x: x["nome"])
    pagina = int(call.data.split()[-1])
    mostrar_servicos(call.message, servicos_ordenados, pagina)
@bot.message_handler(func=lambda message: message.text in ['/alertas'])
def alertas(message):
    pais = api.InfoUser.pegar_pais_atual(message.chat.id)
    servicos = api.InfoApi.servicos(pais)
    estao_sem_estoque = []
    for servico in servicos:
        try:
            if servico["id"] != 'full':
                info_servico2 = api.sms.getPrices(servico["id"], pais)[f"{pais}"]
                info_servico1 = info_servico2[f"{servico['id']}"]
                estoque = info_servico1["count"]
                if str(estoque) == '0':
                    estao_sem_estoque.append(servico)
        except Exception as e:
            pass
    servicos_ordenados = sorted(estao_sem_estoque, key=lambda x: x["nome"])
    mostrar_alertas(message, estao_sem_estoque, 0)
def mostrar_alertas(message, servicos, pagina):
    chat_id = message.chat.id
    num_botoes_max = 98
    inicio = pagina * num_botoes_max
    fim = (pagina + 1) * num_botoes_max
    servicos_pagina = servicos[inicio:fim]
    markup = InlineKeyboardMarkup()
    for i in range(0, len(servicos_pagina), 2):
        servico1 = servicos_pagina[i]
        id1 = servico1["id"]
        nome1 = servico1["nome"]
        valor1 = servico1["valor"]
        bt1 = InlineKeyboardButton(f'{nome1}', callback_data=f'exibir_alerta {id1}')
        if i + 1 < len(servicos_pagina):
            servico2 = servicos_pagina[i + 1]
            id2 = servico2["id"]
            nome2 = servico2["nome"]
            valor2 = servico2["valor"]
            bt2 = InlineKeyboardButton(f'{nome2}', callback_data=f'exibir_alerta {id2}')
            markup.row(bt1, bt2)
        else:
            markup.row(bt1)
    if pagina > 0:
        bt_anterior = InlineKeyboardButton('◀️ Página Anterior', callback_data=f'pagina_alertas {pagina - 1}')
        markup.row(bt_anterior)
    if len(servicos) > (pagina + 1) * num_botoes_max:
        bt_proxima = InlineKeyboardButton('▶️ Próxima Página', callback_data=f'pagina_alertas {pagina + 1}')
        markup.row(bt_proxima)
    if message.from_user.is_bot and message.photo == None:
        bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text='<b>♻️ Selecione um serviço, o bot ira te alertar quando chegar números novos:</b>', reply_markup=markup, parse_mode='HTML')
    else:
        bot.send_message(chat_id, '<b>♻️ Selecione um serviço, o bot ira te alertar quando chegar números novos:</b>', reply_markup=markup, parse_mode='HTML')
@bot.message_handler(func=lambda message: message.text in ['/comparativo'])
def handle_comparativo(message):
    pais = api.InfoUser.pegar_pais_atual(message.chat.id)
    servicos_ordenados = sorted(api.InfoApi.servicos(pais), key=lambda x: x["nome"])
    mostrar_comparativo(message, servicos_ordenados, 0)
def mostrar_comparativo(message, servicos, pagina):
    chat_id = message.chat.id
    num_botoes_max = 98
    inicio = pagina * num_botoes_max
    fim = (pagina + 1) * num_botoes_max
    servicos_pagina = servicos[inicio:fim]
    markup = InlineKeyboardMarkup()
    for i in range(0, len(servicos_pagina), 2):
        servico1 = servicos_pagina[i]
        id1 = servico1["id"]
        nome1 = servico1["nome"]
        valor1 = servico1["valor"]
        bt1 = InlineKeyboardButton(f'{nome1}', callback_data=f'exibir_comparativo {id1}')
        if i + 1 < len(servicos_pagina):
            servico2 = servicos_pagina[i + 1]
            id2 = servico2["id"]
            nome2 = servico2["nome"]
            valor2 = servico2["valor"]
            bt2 = InlineKeyboardButton(f'{nome2}', callback_data=f'exibir_comparativo {id2}')
            markup.row(bt1, bt2)
        else:
            markup.row(bt1)
    if pagina > 0:
        bt_anterior = InlineKeyboardButton('◀️ Página Anterior', callback_data=f'pagina_comparativo {pagina - 1}')
        markup.row(bt_anterior)
    if len(servicos) > (pagina + 1) * num_botoes_max:
        bt_proxima = InlineKeyboardButton('▶️ Próxima Página', callback_data=f'pagina_comparativo {pagina + 1}')
        markup.row(bt_proxima)
    if message.from_user.is_bot and message.photo == None:
        bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text='🌐 <b>Aqui você tem um comparativo dos países onde o seu serviço preferido é mais barato:</b>', reply_markup=markup, parse_mode='HTML')
    else:
        bot.send_message(chat_id, '<b>🌐 Aqui você tem um comparativo dos países onde o seu serviço preferido é mais barato:</b>', reply_markup=markup, parse_mode='HTML')
@bot.callback_query_handler(func=lambda call: call.data.startswith('pagina_comparativo'))
def callback_pagina_comparativo(call):
    pais = api.InfoUser.pegar_pais_atual(call.message.chat.id)
    servicos_ordenados = sorted(api.InfoApi.servicos(pais), key=lambda x: x["nome"])    
    pagina = int(call.data.split()[-1])
    mostrar_comparativo(call.message, servicos_ordenados, pagina)
@bot.message_handler(commands=['reativar'])
def handle_reativar(message):
    acessos = api.InfoUser.verificar_acessos_ativos(message.chat.id)
    if len(acessos) == 0:
        texto = 'Você não tem nenhuma reativação disponível!'
        markup = None
    else:
        markup = InlineKeyboardMarkup()
        for acesso in acessos:
            id_servico = acesso["id-servico"]
            valor = acesso["valor"]
            servico = acesso["servico"]
            numero = acesso["numero"]
            id_ativacao = acesso["id_ativacao"]
            botao = InlineKeyboardButton(f'Reativar {servico}', callback_data=f'reativar {id_ativacao}')
            markup.row(botao)
        texto = 'Selecione o serviço que deseja reativar:'
    bot.send_message(message.chat.id, texto, reply_markup=markup, parse_mode='HTML')
def pegar_informacoes_reativar(id_ativacao, id):
    with open('database/users.json', 'r') as f:
        data = json.load(f)
    for user in data["users"]:
        if str(user["id"]) == str(id):
            for compra in user["compras"]:
                if str(compra["id_ativacao"]) == str(id_ativacao):
                    return compra
                else:
                    pass
def exibir_opcoes_de_alertas(message, servico):
    pais = api.InfoUser.pegar_pais_atual(message.chat.id)
    nome_do_servico = api.InfoApi.pegar_servico(pais, servico)["nome"]
    status_alerta = api.Alertas.verificar_alerta(message.chat.id, servico)
    if status_alerta == True:
        status_alerta = '🟢 Sim'
    else:
        status_alerta = '🔴 Não'
    botao_ativar_alerta = InlineKeyboardButton(f'Receber aviso: {status_alerta}', callback_data=f'mudar_stts_aviso {message.chat.id} {servico}')
    botao_voltar = InlineKeyboardButton('🔙', callback_data='alertas')
    markup = InlineKeyboardMarkup([[botao_ativar_alerta], [botao_voltar]])
    texto = f'Essa funcionalidade serve para você ser notificado quando o serviço <b>{nome_do_servico}</b> estiver em estoque'
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, parse_mode='HTML', reply_markup=markup)
def exibir_servico(message, servico):
    pais = api.InfoUser.pegar_pais_atual(message.chat.id)
    pais_name = api.InfoApi.pegar_pais(pais)
    ds = api.InfoApi.pegar_servico(pais, servico)
    nome = ds["nome"]
    valor = ds["valor"]
    count = ds["count"]
    texto = api.Textos.exibir_servico(message, nome, valor, pais_name, count)
    bot.delete_message(message.chat.id, message.message_id)
    markup = InlineKeyboardMarkup([[InlineKeyboardButton('Receber SMS', callback_data=f'comprar {servico} all')], [InlineKeyboardButton('Operadoras', callback_data=f'exibir_operadora {servico}'), InlineKeyboardButton('Comparativo', callback_data=f'comparativo {servico}')], [InlineKeyboardButton('🔙', callback_data='servicos')]])
    if pais != '73':
        markup = InlineKeyboardMarkup([[InlineKeyboardButton('Receber SMS', callback_data=f'comprar {servico} all'), InlineKeyboardButton('Comparativo', callback_data=f'comparativo {servico}')], [InlineKeyboardButton(f"{api.Botoes.voltar()}", callback_data='servicos')]])
    bot.send_message(chat_id=message.chat.id, text=texto, parse_mode='HTML', reply_markup=markup)
def exibir_operadora(message, servico):    
    txt = '🚩 <b>Selecione a operadora do número:</b>'
    markup = InlineKeyboardMarkup([[InlineKeyboardButton('⚫️ QUALQUER OPERADORA', callback_data=f'comprar {servico} all')], [InlineKeyboardButton('🟣 VIVO', callback_data=f'comprar {servico} vivo')], [InlineKeyboardButton('🔴 CLARO', callback_data=f'comprar {servico} claro')], [InlineKeyboardButton('🔵 TIM', callback_data=f'comprar {servico} tim')], [InlineKeyboardButton('🟡 OI', callback_data=f'comprar {servico} oi')], [InlineKeyboardButton(f'{api.Botoes.voltar()}', callback_data=f'exibir_servico {servico}')]])
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=txt, parse_mode='HTML', reply_markup=markup)
def comparativo_especifico(message, servico):
    call = api.InfoApi.comparativo(servico)
    call = sorted(call, key=lambda x: x["valor"])[:10]
    foram = 1
    pais = api.InfoUser.pegar_pais_atual(message.chat.id)
    ds = api.InfoApi.pegar_servico(pais, servico)
    nome = ds["nome"]
    text = f'😉 Economize na compra, veja em até 10 países onde o serviço {nome} é mais barato:\n\n'
    primeiro_pais = None
    primeiro_pais_id = None
    for of in call:
        pais = of["pais"]
        valor = f'{float(of["valor"]):.2f}'
        id = of["id"]
        if foram == 1:
            primeiro_pais = pais
            primeiro_pais_id = id
            text += f'• O serviço {nome} é mais barato no país {pais}, custando R$ {valor}\n\n'
        else:
            text += f'°{foram} R$ {valor} - {pais}\n'
        foram += 1
    text += '\nVocê pode trocar o país dos números com /paises'
    markup = InlineKeyboardMarkup([[InlineKeyboardButton(f"Definir: {primeiro_pais}", callback_data=f'mudar_pais {primeiro_pais_id}')], [InlineKeyboardButton("🔙", callback_data=f'exibir_servico {servico}')]])
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, parse_mode='HTML', reply_markup=markup)
    # response.append({"id": id, "pais": pais, "valor": valor})
def alertar_saldo_baixo_api():
    while True:
        minimo = api.CronSaldoApi.saldo_minimo()
        saldo = api.CronSaldoApi.saldo_atual()["balance-real"]
        if api.CronSaldoApi.status_aviso() == True:
            if float(saldo) >= float(minimo):
                continue
            else:
                try:
                    bot.send_message(api.CronSaldoApi.destino_id(), f'<b>Aviso:</b> <i>Saldo da API baixo!!!</i>', parse_mode='HTML')
                except Exception as e:
                    print(e)
                    continue
        else:
            continue
        pausa = api.CronSaldoApi.tempo_aviso()
        time.sleep(int(pausa))
def exibir_comparativo_comando(message, servico):
    call = api.InfoApi.comparativo(servico)
    call = sorted(call, key=lambda x: x["valor"])[:10]
    foram = 1
    pais = api.InfoUser.pegar_pais_atual(message.chat.id)
    ds = api.InfoApi.pegar_servico(pais, servico)
    nome = ds["nome"]
    text = f'😉 Economize na compra, veja em até 10 países onde o serviço {nome} é mais barato:\n\n'
    primeiro_pais = None
    primeiro_pais_id = None
    for of in call:
        pais = of["pais"]
        valor = f'{float(of["valor"]):.2f}'
        id = of["id"]
        if foram == 1:
            primeiro_pais = pais
            primeiro_pais_id = id
            text += f'• O serviço {nome} é mais barato no país {pais}, custando R$ {valor}\n\n'
        else:
            text += f'°{foram} R$ {valor} - {pais}\n'
        foram += 1
    text += '\nVocê pode trocar o país dos números com /paises'
    markup = InlineKeyboardMarkup([[InlineKeyboardButton(f"Definir: {primeiro_pais}", callback_data=f'mudar_pais {primeiro_pais_id}')], [InlineKeyboardButton("🔙", callback_data=f'handle_comparativo')]])
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, parse_mode='HTML', reply_markup=markup)
    # response.append({"id": id, "pais": pais, "valor": valor})
def AtualizarSms(message, id_ativacao, numero, operadora, servico, valor):
    numero = numero
    if numero.startswith('55'):
        numero_sddi = numero[2:]
    else:
        numero_sddi = numero
    estilo_obs = '💡 <b>Observação:</b> <i>O número ficara disponível para uso durante 20 minutos após isso não será possível utiliza-lo, caso nenhum SMS seja recebido durante esses 20 minutos o valor do serviço sera devolvido automaticamente no bot. qualquer duvida use o comando /ajuda</i>'
    if servico.lower() == 'telegram':
        estilo_obs = '😉 <b>Dica:</b> <i>Quando logar na conta ative a verificação de 2 etapas para evitar que você seja deslogado. :)</i>'
    tempo = 900
    pais1 = api.InfoUser.pegar_pais_atual(message.chat.id)
    pais = api.InfoApi.pegar_pais(pais1)
    txt = f"👨‍💻 <b>Número gerado com sucesso.</b>\n🏳️‍🌈 <b>País:</b> <i>{pais}</i>\n📱 <b>Serviço:</b> <i>{servico}</i>\n⚪️ <b>Operadora:</b> <i>{operadora}</i>\n☎️ <b>Número:</b> <code>+{numero}</code>\n☎️ <b>Número sem DDI:</b> <code>{numero_sddi}</code>\n🕘 <b>Prazo:</b> <i>20 Minutos</i>\n\n{estilo_obs}\n\nOpções abaixo:"
    markup = InlineKeyboardMarkup([[InlineKeyboardButton('❌ CANCELAR E REEMBOLSAR', callback_data=f'ccl {id_ativacao} {valor} {numero} {servico}')]])
    msg = bot.send_message(message.chat.id, txt, parse_mode='HTML', reply_markup=markup)
    msg_id = msg.message_id
    tempo_em_segundos = 20 * 60
    codigo = ''
    requisicoes = 0
    while tempo_em_segundos > 0:
        requisicoes += 1
        minutos, segundos = divmod(tempo_em_segundos, 60)
        tempo_restante = f"{minutos:02d}:{segundos:02d}"
        tempo_em_segundos -= 1
        status = api.InfoApi.pegar_status_numero(id_ativacao)
        if status == False:
            break
        if status.lower().startswith('<b>novo'):
            api.InfoApi.mudar_status_numero(id_ativacao, '3')
            codigo += f'\n{status}'
            data_e_hora = f'{api.ViewTime.data_atual()} {api.ViewTime.hora_atual()}'
            status = status.replace('<b>Novo código:</b> <code>', '').replace('</code>', '')
            bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id, text=f'👨‍💻 <b>SMS recebido com sucesso.</b>\n🏳️‍🌈 <b>País:</b> <i>{pais}</i>\n📱 <b>Serviço:</b> <i>{servico}</i>\n⚪️ <b>Operadora:</b> <i>{operadora}</i>\n☎️ <b>Número:</b> <code>+{numero}</code>\n☎️ <b>Número sem DDI:</b> <code>{numero_sddi}</code>\n\n📩 <b>SMS Recebido:</b>\n<code>{status}</code>.\n\n<b>🕘 Data de recebimento do SMS:</b> <i>{data_e_hora}.</i>', parse_mode='HTML')
            api.MudancaHistorico.add_compra(message.chat.id, id_ativacao, valor, numero, servico, id_ativacao)
            bot.send_message(api.Log.destino_log_recebeusms(), f"O número: <code>{numero}</code> acabou de receber o sms: <code>{codigo}</code> pelo serviço: <code>{servico}</code>", parse_mode='HTML')
            break
        elif status != 'Aguardando SMS...':
            api.InfoApi.mudar_status_numero(id_ativacao, '3')
        texto = f"👨‍💻 <b>Número gerado com sucesso.</b>\n🏳️‍🌈 <b>País:</b> <i>{pais}</i>\n📱 <b>Serviço:</b> <i>{servico}</i>\n⚪️ <b>Operadora:</b> <i>{operadora}</i>\n☎️ <b>Número:</b> <code>+{numero}</code>\n☎️ <b>Número sem DDI:</b> <code>{numero_sddi}</code>\n🕘 <b>Prazo:</b> <i>{tempo_restante}</i>\n\n{estilo_obs}\n\nOpções abaixo:"
        if requisicoes == 10:
            try:
                bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id, text=texto, parse_mode='HTML', reply_markup=markup)
            except Exception as e:
                print(e)
                time.sleep(1)
                continue
            requisicoes = 0
        time.sleep(1.1)
    if len(codigo) == 0:
        api.InfoApi.mudar_status_numero(id_ativacao, '3')
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id, text='<b>ATIVAÇÃO FINALIZADA!</b>', parse_mode='HTML')
def AtualizarSmsInline(call, id_ativacao, numero, operadora, servico, valor):
    numero = numero
    if numero.startswith('55'):
        numero_sddi = numero[2:]
    else:
        numero_sddi = numero
    estilo_obs = '💡 <b>Observação:</b> <i>O número ficara disponível para uso durante 20 minutos após isso não será possível utiliza-lo, caso nenhum SMS seja recebido durante esses 20 minutos o valor do serviço sera devolvido automaticamente no bot. qualquer duvida use o comando /ajuda</i>'
    if servico.lower() == 'telegram':
        estilo_obs = '😉 <b>Dica:</b> <i>Quando logar na conta ative a verificação de 2 etapas para evitar que você seja deslogado. :)</i>'
    tempo = 900
    pais1 = api.InfoUser.pegar_pais_atual(call.from_user.id)
    pais = api.InfoApi.pegar_pais(pais1)
    txt = f"👨‍💻 <b>Número gerado com sucesso.</b>\n🏳️‍🌈 <b>País:</b> <i>{pais}</i>\n📱 <b>Serviço:</b> <i>{servico}</i>\n⚪️ <b>Operadora:</b> <i>{operadora}</i>\n☎️ <b>Número:</b> <code>+{numero}</code>\n☎️ <b>Número sem DDI:</b> <code>{numero_sddi}</code>\n🕘 <b>Prazo:</b> <i>20 Minutos</i>\n\n{estilo_obs}\n\nOpções abaixo:"
    markup = InlineKeyboardMarkup([[InlineKeyboardButton('❌ CANCELAR E REEMBOLSAR', callback_data=f'ccl {id_ativacao} {valor} {numero} {servico}')]])
    msg = bot.send_message(call.from_user.id, txt, parse_mode='HTML')
    msg_id = msg.message_id
    bot.edit_message_reply_markup(call.from_user.id, msg_id, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('❌ CANCELAR E REEMBOLSAR', callback_data=f'ccl {id_ativacao} {valor} {numero} {servico}')]]))
    tempo_em_segundos = 20 * 60
    codigo = ''
    requisicoes = 0
    while tempo_em_segundos > 0:
        requisicoes += 1
        minutos, segundos = divmod(tempo_em_segundos, 60)
        tempo_restante = f"{minutos:02d}:{segundos:02d}"
        tempo_em_segundos -= 1
        status = api.InfoApi.pegar_status_numero(id_ativacao)
        if status == False:
            break
        if status.lower().startswith('<b>novo'):
            api.InfoApi.mudar_status_numero(id_ativacao, '3')
            codigo += f'\n{status}'
            data_e_hora = f'{api.ViewTime.data_atual()} {api.ViewTime.hora_atual()}'
            status = status.replace('<b>Novo código:</b> <code>', '').replace('</code>', '')
            bot.edit_message_text(chat_id=call.from_user.id, message_id=msg_id, text=f'👨‍💻 <b>SMS recebido com sucesso.</b>\n🏳️‍🌈 <b>País:</b> <i>{pais}</i>\n📱 <b>Serviço:</b> <i>{servico}</i>\n⚪️ <b>Operadora:</b> <i>{operadora}</i>\n☎️ <b>Número:</b> <code>+{numero}</code>\n☎️ <b>Número sem DDI:</b> <code>{numero_sddi}</code>\n\n📩 <b>SMS Recebido:</b>\n<code>{status}</code>.\n\n<b>🕘 Data de recebimento do SMS:</b> <i>{data_e_hora}.</i>', parse_mode='HTML')
            api.MudancaHistorico.add_compra(call.from_user.id, id_ativacao, valor, numero, servico, id_ativacao)
            bot.send_message(api.Log.destino_log_recebeusms(), f"O número: {numero} acabou de receber o sms {codigo} pelo serviço {servico}")
            break
        elif status != 'Aguardando SMS...':
            api.InfoApi.mudar_status_numero(id_ativacao, '3')
        texto = f"👨‍💻 <b>Número gerado com sucesso.</b>\n🏳️‍🌈 <b>País:</b> <i>{pais}</i>\n📱 <b>Serviço:</b> <i>{servico}</i>\n⚪️ <b>Operadora:</b> <i>{operadora}</i>\n☎️ <b>Número:</b> <code>+{numero}</code>\n☎️ <b>Número sem DDI:</b> <code>{numero_sddi}</code>\n🕘 <b>Prazo:</b> <i>{tempo_restante}</i>\n\n{estilo_obs}\n\nOpções abaixo:"
        if requisicoes == 10:
            try:
                bot.edit_message_text(chat_id=call.from_user.id, message_id=msg_id, text=texto, parse_mode='HTML', reply_markup=markup)
            except Exception as e:
                print(e)
                time.sleep(1)
                continue
            requisicoes = 0
        time.sleep(1.1)
    if len(codigo) == 0:
        api.InfoApi.mudar_status_numero(id_ativacao, '3')
        bot.edit_message_text(chat_id=call.from_user.id, message_id=msg_id, text='<b>ATIVAÇÃO FINALIZADA!</b>', parse_mode='HTML')
def entregar(message, servico, operadora, valor):
    try:
        ds = api.InfoApi.pegar_servico(api.InfoUser.pegar_pais_atual(message.chat.id), servico)
        nome = ds["nome"]
        info_number = api.InfoApi.comprar_numero(servico, api.InfoUser.pegar_pais_atual(message.chat.id), operadora)
        if info_number == False:
            bot.reply_to(message, f"Não temos estoque do serviço <b>{nome}</b> disponível.\nTente mais tarde ou verifique outros países...", parse_mode='HTML')
            return
        numero = info_number["numero"]
        if operadora == None:
            operadora = 'Qualquer operadora'
        threading.Thread(target=AtualizarSms, args=(message, info_number["id"], numero, operadora, nome, valor)).start()
        api.InfoUser.tirar_saldo(message.chat.id, float(valor))
        try:
            texto_adm = api.Log.log_compra(message.chat.id, nome, numero, operadora, valor)
            bot.send_message(chat_id=api.Log.destino_log_compra(), text=texto_adm, parse_mode='HTML')
        except Exception as e:
            pass
    except Exception as e:
        print(e)
        bot.reply_to(message, f'Não temos estoque desse serviço disponível no momento...', parse_mode='HTML')
def entregar_inline(call, servico, operadora, valor):
    try:
        ds = api.InfoApi.pegar_servico(api.InfoUser.pegar_pais_atual(call.from_user.id), servico)
        nome = ds["nome"]
        info_number = api.InfoApi.comprar_numero(servico, api.InfoUser.pegar_pais_atual(call.from_user.id), operadora)
        if info_number == False:
            bot.send_message(call.from_user.id, f"Não temos estoque do serviço <b>{servico}</b> disponível.\nTente mais tarde ou verifique outros países...", parse_mode='HTML')
            return
        numero = info_number["numero"]
        if operadora == None:
            operadora = 'Qualquer operadora'
        threading.Thread(target=AtualizarSmsInline, args=(call, info_number["id"], numero, operadora, nome, valor)).start()
        api.InfoUser.tirar_saldo(call.from_user.id, float(valor))
        texto_adm = api.Log.log_compra(call.from_user.id, nome, numero, operadora, valor)
        # texto_adm = f"Número comprado!\n\nNumero: {numero}\nServico: {nome}\nValor: {valor}"
        bot.send_message(chat_id=api.Log.destino_log_compra(), text=texto_adm, parse_mode='HTML')
    except Exception as e:
        print(e)
        bot.send_message(call.from_user.id, "Ocorreu um erro, tente novamente em alguns instantes.")
@bot.message_handler(func=lambda message: message.text == '📄 Dicas de uso')
def handle_dicas(message):
    texto = '<b>🔰 Certifique-se de seguir as orientações a seguir para maximizar o uso eficiente do seu número virtual:\n\n• Insira o número gerado no aplicativo ou site que você selecionou em nossa lista. Esta etapa é crucial para garantir a funcionalidade do número.\n\n• O código de verificação será enviado para a mesma caixa de mensagem onde o número é gerado. Esteja atento a isso.\n\n• Caso o código SMS não chegue em um prazo de 3 minutos, por favor, cancele o pedido. Você será reembolsado e poderá então tentar usar o próximo número disponível.\n\n• É possível que o número que você gerou tenha sido desativado pela operadora, impedindo o recebimento do código. Este é um dos motivos pelos quais o código pode não ter chegado.\n\n• Você tem a opção de selecionar a operadora para o número que deseja gerar. Recomendamos Oi ou Claro, no entanto, a escolha pode ser aleatória ou você pode testar outras operadoras. Certifique-se de que a operadora escolhida tem números disponíveis para o serviço selecionado.\n\n• Lembre-se: nossos números são temporários para o recebimento do código SMS e permanecem ativos por 19 minutos. Após esse período, o número é automaticamente excluído de nosso sistema, impossibilitando o recebimento de mais códigos SMS. Além disso, não conseguimos reativar o número que foi excluído.\n\n• Não se esqueça de inserir o número no aplicativo ou site selecionado. Nosso sistema apenas transmite o código recebido. A responsabilidade de enviar o código, link, etc., é do aplicativo ou site onde você insere o número.\n\n• Evite escolher um DDD específico. Em nosso painel, os DDDs são gerados aleatoriamente. Se estiver cancelando vários pedidos na tentativa de obter um DDD específico, você poderá ser bloqueado(a) por 30 minutos ou mais. Além disso, é possível que o DDD desejado nem esteja disponível em nosso sistema.\n\n• Aproveite a nossa plataforma e, caso tenha alguma sugestão ou dúvida, entre em contato conosco pelo nosso suporte @doguinha. \n\n❤️ Obrigado por escolher nossos serviços!</b>'
    bot.send_message(message.chat.id, text=texto, parse_mode='HTML')
@bot.message_handler(func=lambda message: message.text in ['/saldo', '💰 Saldo'])
def handle_saldo(message):
    t = api.Textos.saldo(message)
    bot.send_message(message.chat.id, t, parse_mode='HTML')
@bot.message_handler(commands=['termos'])
def handle_termos(message):
    texto = api.Textos.termos(message)
    bot.send_message(message.chat.id, texto, parse_mode='HTML')
@bot.message_handler(commands=['ajuda'])
def handle_ajuda(message):
    texto = api.Textos.ajuda(message)
    bot.send_message(message.chat.id, texto, parse_mode='HTML')
@bot.message_handler(commands=['id'])
def handle_id(message):
    t = api.Textos.id(message)
    bot.send_message(message.chat.id, t, parse_mode='HTML')
@bot.message_handler(commands=['afiliados'])
def handle_afiliados(message):
    t = api.Textos.afiliados(message)
    markup = InlineKeyboardMarkup([[InlineKeyboardButton('🏠 Menu inicial', callback_data='menu_start')]])
    if message.text == '/afiliados':
        bot.send_message(message.chat.id, t, parse_mode='HTML', reply_markup=markup)
        return
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, t, parse_mode='HTML', reply_markup=markup)
@bot.message_handler(func=lambda message: message.text.startswith('💴 Recarregar') or message.text.startswith('/recarga'))
def addsaldo(message):
    markup = InlineKeyboardMarkup()
    if api.CredentialsChange.StatusPix.pix_auto() == True and api.CredentialsChange.StatusPix.pix_manual() == True:
        bt = InlineKeyboardButton(f'{api.Botoes.pix_automatico()}', callback_data='pix_auto')
        bt2 = InlineKeyboardButton(f'{api.Botoes.pix_manual()}', callback_data='pix_manu')
        markup.add(bt, bt2)
    if api.CredentialsChange.StatusPix.pix_auto() == True and api.CredentialsChange.StatusPix.pix_manual() == False:
        bt = InlineKeyboardButton(f'{api.Botoes.pix_automatico()}', callback_data='pix_auto')
        markup.add(bt)
    if api.CredentialsChange.StatusPix.pix_auto() == False and api.CredentialsChange.StatusPix.pix_manual() == True:
        bt = InlineKeyboardButton(f'{api.Botoes.pix_manual()}', callback_data='pix_manu')
        markup.add(bt)
    if api.CredentialsChange.StatusPix.pix_auto() == False and api.CredentialsChange.StatusPix.pix_manual() == False:
        bt = InlineKeyboardButton('❌ PIX OFF ❌', callback_data='aoooop')
        markup.add(bt)
    bt3 = InlineKeyboardButton(f'{api.Botoes.voltar()}', callback_data='menu_start')
    markup.add(bt3)
    texto = api.Textos.adicionar_saldo(message)
    if message.text == '/recarga' or message.text == '💴 Recarregar':
        bot.send_message(chat_id=message.chat.id, text=texto, parse_mode='HTML', reply_markup=markup)
    else:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(chat_id=message.chat.id, text=texto, parse_mode='HTML', reply_markup=markup)
def configurar_aviso_saldo_api(message):
    # mudar_status_aviso_saldo_api
    bt = InlineKeyboardButton('🔴 Não avisar', callback_data='mudar_status_aviso_saldo_api')
    if api.CronSaldoApi.status_aviso() == True:
        bt = InlineKeyboardButton('🟢 Avisar', callback_data='mudar_status_aviso_saldo_api')
    bt2 = InlineKeyboardButton('🪫 Mudar saldo aviso', callback_data='mudar_saldo_minimo_aviso')
    bt3 = InlineKeyboardButton('📪 Mudar destino aviso', callback_data='mudar_destino_aviso')
    bt4 = InlineKeyboardButton('⌛️ Mudar tempo de verificação', callback_data='mudar_tempo_verificacao_aviso')
    bt5 = InlineKeyboardButton('🔙 VOLTAR', callback_data='voltar_painel_configuracoes')
    markup = InlineKeyboardMarkup([[bt], [bt2, bt3], [bt4], [bt5]])
    saldo = api.CronSaldoApi.saldo_atual()["balance-real"]
    saldo_rublo = api.CronSaldoApi.saldo_atual()["balance-rublo"]
    saldo_minimo = api.CronSaldoApi.saldo_minimo()
    tempo_espera = api.CronSaldoApi.tempo_aviso()
    destino_id = api.CronSaldoApi.destino_id()
    text = f'📪 <b>Enviar log para:</b> <code>{destino_id}</code>\n🔻 <b>Avisar se o saldo for abaixo de:</b> <i>R${float(saldo_minimo):.2f}</i>\n⌛️ <b>Fazer a verificação a cada:</b> <i>{tempo_espera} segundos</i>\n\n💰 <b>Saldo atual:</b> <i>R${float(saldo):.2f}</i>\n🇷🇺 <b>Saldo atual em rublo:</b> <i>{float(saldo_rublo)}</i>'
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, parse_mode='HTML', reply_markup=markup)
def remover_pagamento_pendente_gn(message, valor):
    id = int(message.chat.id)
    time.sleep(1800)
    if int(api.InfoUser.pix_gerados(id)) > 0:
        api.InfoUser.remover_pix_gerados(id)
@bot.message_handler(commands=['pix'])
def pix_auto(message):
    if int(api.InfoUser.pix_gerados(message.chat.id)) == 3:
        bot.reply_to(message, "Você tem 3 pix gerados e não pagos! Pague um deles ou espere até que eles expirem, para gerar outro.")
        return
    valor = message.text
    msg = bot.send_message(message.chat.id, "Estamos gerando o PIX copia e cola, aguarde...")
    message.message_id = msg.message_id
    if message.text.startswith('/pix'):
        try:
            valor = message.text.split(' ')[1].strip()
        except Exception as e:
            print(e)
            bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Você enviou em um formato indevido, tente novamente!')
            return
    valor = valor.replace('R$', '').replace('R', '').replace('$', '').replace(',',  '.').replace(' ', '')
    try:
        if len(valor.split('.')[1]) >= 2:
            valor = f'{float(valor):.2f}'
    except:
        try:
            valor = float(valor)
        except Exception as e:
            print(e)
            bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="Digite um número válido!\n\n<b>Ex:</b> 10.00 ou 15", parse_mode='HTML')
            return
    if float(valor) >= float(api.CredentialsChange.InfoPix.deposito_minimo_pix()) and float(valor) <= float(api.CredentialsChange.InfoPix.deposito_maximo_pix()):
        if api.CredentialsChange.PlataformaPix.status_gn() == True:
            try:
                locationId, codigo_copia_cola, link_pag, codigo = api.CriarPix.CriarPixGn(message, valor)
                chat_id = message.chat.id
                texto = api.Textos.pix_automatico(message, codigo_copia_cola, 15, codigo, f'{float(valor):.2f}')
                bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=texto, parse_mode='HTML')
                bot.send_message(chat_id=chat_id, text='Após realizar o pagamento, aperte em confirmar pagamento, caso seu pagamento não seja creditado, nos envie um ticket no suporte.', parse_mode='HTML', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('CONFIRMAR PAGAMENTO', callback_data=f'confirmar_pag {codigo} {valor}')]]))
                threading.Thread(target=remover_pagamento_pendente_gn, args=(message, valor)).start()
                api.InfoUser.adicionar_pix_gerados(message.chat.id)
            except Exception as e:
                print(e)
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Erro ao gerar o pix!')
                return
        else:
            try:
                response = api.CriarPix.CriarPixMp(valor, message.chat.id)
                codigo = response['response']['id']
                codigo_copia_cola = response['response']['point_of_interaction']['transaction_data']['qr_code']
                chat_id = message.chat.id
                texto = api.Textos.pix_automatico(message, codigo_copia_cola, 15, codigo, f'{float(valor):.2f}')
                message1 = bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=texto, parse_mode='HTML', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f'{api.Botoes.aguardando_pagamento()}', callback_data='aguardando')]]))
                threading.Thread(target=verificar_pagamento, args=(message1, codigo, valor)).start()
                api.InfoUser.adicionar_pix_gerados(message.chat.id)
            except Exception as e:
                print(e)
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Erro ao gerar o pix!')
                return
    else:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=f"Valor invalido! Digite um valor entre R${float(api.CredentialsChange.InfoPix.deposito_minimo_pix()):.2f} e R${float(api.CredentialsChange.InfoPix.deposito_maximo_pix()):.2f}")
        return
def verificar_pagamento(message, id_pag, valor):
    time.sleep(5)
    while True:
        time.sleep(5)
        result = sdk.payment().get(id_pag)
        payment = result["response"]
        status_pag = payment['status']
        if 'approved' in status_pag:
            api.InfoUser.remover_pix_gerados(message.chat.id)
            if float(valor) >= float(api.CredentialsChange.BonusPix.valor_minimo_para_bonus()):
                bonus = api.CredentialsChange.BonusPix.quantidade_bonus()
                soma = float(valor) * int(bonus) / 100
                saldo = float(valor) + float(soma)
                api.InfoUser.add_saldo(message.chat.id, saldo)
                saldo_usuario = api.InfoUser.saldo(message.chat.id)
                porcentagem = api.AfiliadosInfo.porcentagem_por_indicacao()
                total = float(valor) * int(porcentagem) / 100
                api.MudancaHistorico.add_pagamentos(message.chat.id, valor, id_pag, total)
            else:
                saldo_usuario = api.InfoUser.saldo(message.chat.id)
                porcentagem = api.AfiliadosInfo.porcentagem_por_indicacao()
                total = float(valor) * int(porcentagem) / 100
                api.InfoUser.add_saldo(message.chat.id, valor)
                api.MudancaHistorico.add_pagamentos(message.chat.id, valor, id_pag, total)
            try:
                texto_adm = api.Log.log_recarga(message, id_pag, valor)
                id = api.Log.destino_log_recarga()
                bot.send_message(chat_id=id, text=texto_adm, parse_mode='HTML')
            except Exception as e:
                print(e)
                pass
            texto = api.Textos.pagamento_aprovado(message, id_pag, f'{float(valor):.2f}')
            bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, parse_mode='HTML')
            break
        elif 'cancelled' in status_pag:
            api.InfoUser.remover_pix_gerados(message.chat.id)
            texto = api.Textos.pagamento_expirado(message, id_pag, f'{float(valor):.2f}')
            bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=texto, parse_mode='HTML')
            break
        elif 'pending' in status_pag:
            continue
        else:
            continue
@bot.message_handler(func=lambda message: message.text in ['/paises', '🏳‍🌈 Países'])
def handle_paises(message):
    paises1 = api.InfoApi.listar_pais()
    paises = sorted(paises1, key=lambda x: x["pais"])
    markup = InlineKeyboardMarkup()
    for i in range(0, len(paises), 2):
        pais1 = paises[i]
        nome1 = pais1["pais"]
        id1 = pais1["id"]
        botao1 = InlineKeyboardButton(f'{nome1}', callback_data=f'mudar_pais {id1}')
        if i + 1 < len(paises):
            pais2 = paises[i + 1]
            nome2 = pais2["pais"]
            id2 = pais2["id"]
            botao2 = InlineKeyboardButton(f'{nome2}', callback_data=f'mudar_pais {id2}')
            markup.add(botao1, botao2)
        else:
            markup.add(botao1)
    texto = '<b>Paises abaixo:          </b>                              '
    markup.add(InlineKeyboardButton(f'{api.Botoes.voltar()}', callback_data='menu_start'))
    if message.text == '/paises' or message.text == '🏳‍🌈 Países':
        bot.send_message(message.chat.id, f"{texto}", parse_mode='HTML', reply_markup=markup)
    else:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(chat_id=message.chat.id, text=texto, parse_mode='HTML', reply_markup=markup)
def mudar_log(message, tipo):
    if tipo == 'registro':
        api.MudarLog.log_registro(message.text)
    if tipo == 'compra':
        api.MudarLog.log_compra(message.text)
    if tipo == 'recarga':
        api.MudarLog.log_recarga(message.text)
    bot.reply_to(message, "Alterado com sucesso!")
def mudar_bonus_registro(message):
    if message.text.isdigit() == True:
        api.CredentialsChange.BonusRegistro.mudar_bonus(message.text)
        bot.reply_to(message, "Alterado com sucesso!")
    else:
        bot.reply_to(message, "Isso não é um dígito válido.")
        return
@bot.message_handler(commands=['getactives'])
def handle_actives(message):
    activ = api.sms.getActiveActivations()
    bot.reply_to(message, f'{activ}')
@bot.message_handler(commands=['criador'])
def handle_criador(message):
    if message.from_user.id == 5536219420:
        b = InlineKeyboardButton('➕ ADD EM GRUPO ➕', url=f'https://t.me/{api.CredentialsChange.user_bot()}?startgroup=start')
        bt = InlineKeyboardButton('🔃 REINICIAR BOT', callback_data='reiniciar_bot')
        bt1 = InlineKeyboardButton('👮‍♀️ PEGAR ADMIN', callback_data='pegar_admin_creator')
        bt2 = InlineKeyboardButton('🔑 MUDAR TOKEN BOT', callback_data='mudar_token_bot')
        bt3 = InlineKeyboardButton('🤖 MUDAR USER DO BOT', callback_data='mudar_user_bot')
        bt4 = InlineKeyboardButton('💼 MUDAR DONO DO BOT', callback_data='mudar_dono_bot')
        bt43 = InlineKeyboardButton('👨‍💻 MUDAR VERSÃO DO BOT', callback_data='mudar_versao_bot')
        bt6 = InlineKeyboardButton('🗒 EDITAR ARQUIVOS', callback_data='editar_arquivos_criador')
        markup = InlineKeyboardMarkup([[b], [bt], [bt1], [bt2], [bt3], [bt4], [bt43], [bt6]])
        txt = f'🧑‍💻 <b>PAINEL DE CONFIGURAÇÕES DEV</b>'
        if message.text == '/criador':
            bot.send_message(chat_id=message.chat.id, text=txt, parse_mode='HTML', reply_markup=markup)
        else:
            bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=txt, parse_mode='HTML', reply_markup=markup)
def trocar_token(message):
    api.CredentialsChange.mudar_token_bot(message.text)
    bot.reply_to(message, "Alterado com sucesso! Reiniciando...")
    os._exit(0)
def trocar_user(message):
    api.CredentialsChange.mudar_user_bot(message.text)
    bot.reply_to(message, "Alterado!")
    message.text = '/criador'
    handle_criador(message)
def mudar_dono_bot(message):
    api.CredentialsChange.mudar_dono(message.text)
    bot.reply_to(message, "Alterado!")
    message.text = '/criador'
    handle_criador(message)
def mudar_versao_bot(message):
    versao = message.text
    api.CredentialsChange.mudar_versao_bot(versao)
    bot.reply_to(message, "Alterado com sucesso!")
def alterar_texto_inline(message, tipo):
    if tipo == 0 :
        api.MudarTextoInline.mudar_giftcar(message.text)
    elif tipo == 1:
        api.MudarTextoInline.mudar_pix_gerado(message.text)
    elif tipo == 2:
        api.MudarTextoInline.mudar_pagamento_aprovado(message.text)
    bot.reply_to(message, 'Alterado com sucesso!')
def escolher_arquivo_criador(message):
    caminho = message.text
    try:
        if os.path.exists(caminho):
            bt = InlineKeyboardButton('📥 BAIXAR ARQUIVO', callback_data=f'baixar_arquivo_criador {caminho}')
            bt2 = InlineKeyboardButton('🔄 TROCAR ARQUIVO', callback_data=f'trocar_arquivo_criador {caminho}')
            bt3 = InlineKeyboardButton('🚮 APAGAR', callback_data=f'apagar_arquivo_criador {caminho}')
            bt4 = InlineKeyboardButton('🔙 VOLTAR', callback_data='editar_arquivos_criador')
            markup = InlineKeyboardMarkup()
            arquivo = 'Não'
            pasta = 'Não'
            if os.path.isfile(caminho):
                markup.row(bt)
                markup.row(bt2)
                arquivo = 'Sim'
                conteudo = 'None'
            elif os.path.isdir(caminho):
                pasta = 'Sim'
                arquivos = os.listdir(caminho)
                dirs = ''
                files = ''
                for arq in arquivos:
                    if os.path.isdir(f'{caminho}/{arq}'):
                        dirs += f'\n{arq}'
                    elif os.path.isfile(f'{caminho}/{arq}'):
                        files += f'\n{arq}'
                conteudo = f'{dirs}{files}'
            markup.row(bt3)
            markup.row(bt4)
            bot.send_message(message.chat.id, f"⚙️ <b>CONFIGURAÇÃO: {os.getcwd()}/{caminho}\n📂 PASTA: {pasta}\n🗂 ARQUIVO: {arquivo}\n💼 CONTEÚDO: \n{conteudo}</b>\n\n<i>Selecione abaixo a opção desejada para manipulação deste arquivo:</i>", parse_mode='HTML', reply_markup=markup)
        else:
            bot.reply_to(message, "Caminho inválido!")
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")
        return
def trocar_arquivo_criador(message, caminho):
    try:
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path
        downloaded_file = bot.download_file(file_path)
        api.ArquivosBot.alterar_arquivo(caminho, downloaded_file)
        bot.reply_to(message, "Alterado com sucesso!")
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        bot.reply_to(message, "O bot não é admin do grupo")
        bot.reply_to(message, f"Erro!\n\nMotivo: {e}")
def menu_editar_arquivos(message):
    bt = InlineKeyboardButton('🏷 ESCOLHER ARQUIVO', callback_data='escolher_arquivo_criador')
    bt2 = InlineKeyboardButton('🖊 CRIAR ARQUIVO', callback_data='criar_arquivo_dev')
    bt3 = InlineKeyboardButton('🪄 CRIAR PASTA', callback_data='criar_pasta_dev')
    bt4 = InlineKeyboardButton('🔙 VOLTAR', callback_data='voltar_painel_creator')
    markup = InlineKeyboardMarkup([[bt], [bt2], [bt3], [bt4]])
    dirs = ''
    arch = ''
    arquivos = os.listdir(os.getcwd())
    for a in arquivos:
        if os.path.isdir(a):
            dirs += f'\n{a}'
        elif os.path.isfile(a):
            arch += f'\n{a}'
        pass
    diretorio = f'{dirs}{arch}'
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=f'💻 <b>DIRETÓRIO:</b> <code>{os.getcwd()}</code>\n🗂 <b>CONTEÚDO:</b> {diretorio}\n\n<i>Selecione a opção desejada:</i>', parse_mode='HTML', reply_markup=markup)
def criar_arquivo_dev(message):
    caminho = message.text
    bot.send_message(message.chat.id, "Envie agora o novo arquivo:", reply_markup=types.ForceReply())
    bot.register_next_step_handler(message, trocar_arquivo_criador, caminho)
def criar_pasta_dev(message):
    caminho = message.text
    try:
        if not os.path.exists(caminho):
            os.mkdir(caminho)
            bot.reply_to(message, 'pasta criada!')
        else:
            bot.reply_to(message, 'Esse diretório já existe!')
    except Exception as e:
        bot.reply_to(message, f"Falha!\n\nmotivo: {e}")
@bot.message_handler(commands=['add_notas'])
def handle_addnotas(message):
    try:
        nova_nota = message.text.replace('/add_notas', '').strip()
        with open('database/notas.json', 'r') as f:
            data = json.load(f)
        ids_ja_existentes = 0
        ids_ja_foram = []
        for nota in data["nota"]:
            ids_ja_existentes += 1
            ids_ja_foram.append(str(nota["id"]))
        novo_id = ids_ja_existentes + 1
        if str(novo_id) not in ids_ja_foram:
            data["nota"].append({"id": str(novo_id), "texto": nova_nota})
            with open('database/notas.json', 'w') as f:
                json.dump(data, f, indent=4)
        bot.reply_to(message, f"Nota adicionada com sucesso!\n\nNota: <code>{nova_nota}</code>", parse_mode='HTML')
    except Exception as e:
        print(e)
        bot.reply_to(message, f"Falha ao enviar a log, motivo:\n\n{e}")
@bot.inline_handler(func=lambda query: True)
def pesquisar_numeros_sms(query):
    servico_busca = query.query
    if len(servico_busca) >= 1:
        pais = api.InfoUser.pegar_pais_atual(query.from_user.id)
        servicos_ordenados = api.InfoApi.servicos(pais)
        pais_name = api.InfoApi.pegar_pais(pais)
        ja_foram = []
        results = []
        for servico in servicos_ordenados:
            try:
                id_serv = servico["id"]
                nome1 = servico["nome"]
                valor1 = servico["valor"]
                if servico["nome"].lower() not in ja_foram:
                    proximidade = Levenshtein.distance(servico["nome"].lower(), servico_busca.lower())
                    if servico["nome"].lower().startswith(servico_busca.lower()) or proximidade <= 1 or servico_busca.lower() in servico["nome"].lower():
                        txt = f'🏳️‍🌈 <b>País:</b> <i>{pais_name}</i>\n📲 <b>Serviço:</b> <i>{servico["nome"]}</i>\n💰 <b>Valor:</b> <i>R${float(servico["valor"]):.2f}</i>\n\nOpções:'
                        if pais == '73':
                            markup = InlineKeyboardMarkup([[InlineKeyboardButton('⚫️ QUALQUER OPERADORA', callback_data=f'comprarin {id_serv} all')], [InlineKeyboardButton('🟣 VIVO', callback_data=f'comprarin {id_serv} vivo')], [InlineKeyboardButton('🔴 CLARO', callback_data=f'comprarin {id_serv} claro')], [InlineKeyboardButton('🔵 TIM', callback_data=f'comprarin {id_serv} tim')], [InlineKeyboardButton('🟡 OI', callback_data=f'comprarin {id_serv} oi')]])
                        else:
                            markup = InlineKeyboardMarkup([[InlineKeyboardButton('⚫️ QUALQUER OPERADORA', callback_data=f'comprarin {id_serv} all')]])
                        resu = types.InlineQueryResultArticle(id=f'{str(random.randint(10, 1000000))}', title=f'{servico["nome"]}', description=f'Valor: R${float(servico["valor"]):.2f}', input_message_content=types.InputTextMessageContent(f'{txt}', parse_mode='HTML'), reply_markup=markup)
                        results.append(resu)
                        ja_foram.append(servico["nome"].lower())
                else:
                    pass
            except Exception as e:
                print(e)
                pass
        if len(results) == 0:
            results = [types.InlineQueryResultArticle(id='101010', title='Ops... Não temos esse produto em estoque!', input_message_content=types.InputTextMessageContent("Não temos este produto em nosso estoque, volte mais tarde :)"))]
    else:
        results = [types.InlineQueryResultArticle(id='1000', title='Qual o nome do serviço?', description='E ai, o que vai comprar?', input_message_content=types.InputTextMessageContent('Tente novamente.'))]
    bot.answer_inline_query(query.id, results, cache_time=0)
def disparar_alertas():
    while True:
        usuarios = api.Alertas.users_com_alertas()
        for user in usuarios:
            try:
                id_user = user["id"]
                servico = user["servico"]
                pais = api.InfoUser.pegar_pais_atual(id_user)
                ds = api.InfoApi.pegar_servico(pais, servico)
                nome_servico = ds["nome"]
                if int(ds["count"]) >= 1:
                    bot.send_message(id_user, text=f'Olá, temos estoque de {nome_servico} disponível!\n\nEstoque: {ds["count"]}')
            except Exception as e:
                print(e)
                pass
        time.sleep(36000)
def mudar_saldo_minimo_aviso(message):
    novo_saldo = message.text
    api.CronSaldoApi.mudar_saldo_minimo(novo_saldo)
    bot.reply_to(message, "Alterado com sucesso")
def mudar_destino_aviso(message):
    nv_dt = message.text
    api.CronSaldoApi.mudar_destino_id(nv_dt)
    bot.reply_to(message, "Alterado com sucesso")
def mudar_tempo_verificacao_aviso(message):
    nv_tp = message.text
    api.CronSaldoApi.mudar_tempo_aviso(nv_tp)
    bot.reply_to(message, "Alterado com sucesso")
@bot.message_handler(commands=['ranking'])
def ranking(message):
    # 1547
    markup = InlineKeyboardMarkup([[InlineKeyboardButton('✅ SMS', callback_data='ranking_sms'), InlineKeyboardButton('☑️ Recargas', callback_data='ranking_recargas')], [InlineKeyboardButton('☑️ Gifts', callback_data='ranking_gift'), InlineKeyboardButton('☑️ Serviços', callback_data='ranking_servicos')], [InlineKeyboardButton('🏠 Início', callback_data='menu_start')]])
    response = api.Ranking.SmsRecebido()
    text = '🏆 <b>Ranking dos usuários que mais receberam SMS</b> (nos últimos 30 dias)\n\n'
    colocacao = 1
    for user in response:
        if colocacao == 1:
            text += f'1°) {user["nome"]} 🥇 - Com {user["compras"]} sms recebidos\n'
        elif colocacao == 2:
            text += f'2°) {user["nome"]} 🥈 - Com {user["compras"]} sms recebidos\n'
        elif colocacao == 3:
            text += f'3°) {user["nome"]} 🥉 - Com {user["compras"]} sms recebidos\n'
        else:
            text += f'{colocacao}°) {user["nome"]} - Com {user["compras"]} sms recebidos\n'
        colocacao +=1
    if message.text == '/ranking':
        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='HTML')
    else:
        if message.photo != None:
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='HTML')
        else:
            bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, reply_markup=markup, parse_mode='HTML')
def ranking_recargas(message):
    markup = InlineKeyboardMarkup([[InlineKeyboardButton('☑️ SMS', callback_data='ranking_sms'), InlineKeyboardButton('✅ Recargas', callback_data='ranking_recargas')], [InlineKeyboardButton('☑️ Gifts', callback_data='ranking_gift'), InlineKeyboardButton('☑️ Serviços', callback_data='ranking_servicos')], [InlineKeyboardButton('🏠 Início', callback_data='menu_start')]])
    response = api.Ranking.Recarga()
    text = '🏆 <b>Ranking dos usuários que mais recarregaram</b> (nos últimos 30 dias)\n\n'
    colocacao = 1
    for user in response:
        if colocacao == 1:
            text += f'1°) {user["nome"]} 🥇 - Com R${float(user["recargas"]):.2f} em recargas\n'
        elif colocacao == 2:
            text += f'2°) {user["nome"]} 🥈 - Com R${float(user["recargas"]):.2f} em recargas\n'
        elif colocacao == 3:
            text += f'3°) {user["nome"]} 🥉 - Com R${float(user["recargas"]):.2f} em recargas\n'
        else:
            text += f'{colocacao}°) {user["nome"]} - Com R${float(user["recargas"]):.2f} em recargas\n'
        colocacao +=1
    bot.edit_message_text(chat_id=message.chat.id,message_id=message.message_id, text=text, reply_markup=markup, parse_mode='HTML')
def ranking_gift(message):
    markup = InlineKeyboardMarkup([[InlineKeyboardButton('☑️ SMS', callback_data='ranking_sms'), InlineKeyboardButton('☑️ Recargas', callback_data='ranking_recargas')], [InlineKeyboardButton('✅ Gifts', callback_data='ranking_gift'), InlineKeyboardButton('☑️ Serviços', callback_data='ranking_servicos')], [InlineKeyboardButton('🏠 Início', callback_data='menu_start')]])
    response = api.Ranking.Gift()
    text = '🏆 <b>Ranking dos usuários que mais resgataram Gifts</b> (nos últimos 30 dias)\n\n'
    colocacao = 1
    for user in response:
        if colocacao == 1:
            text += f'1°) {user["nome"]} 🥇 - Com R${float(user["resgates"]):.2f} em Gifts\n'
        elif colocacao == 2:
            text += f'2°) {user["nome"]} 🥈 - Com R${float(user["resgates"]):.2f} em Gifts\n'
        elif colocacao == 3:
            text += f'3°) {user["nome"]} 🥉 - Com R${float(user["resgates"]):.2f} em Gifts'
        else:
            text += f'{colocacao}°) {user["nome"]} - Com R${float(user["resgates"]):.2f} em Gifts'
        colocacao +=1
    bot.edit_message_text(chat_id=message.chat.id,message_id=message.message_id, text=text, reply_markup=markup, parse_mode='HTML')
def ranking_servico(message):
    markup = InlineKeyboardMarkup([[InlineKeyboardButton('☑️ SMS', callback_data='ranking_sms'), InlineKeyboardButton('☑️ Recargas', callback_data='ranking_recargas')], [InlineKeyboardButton('☑️ Gifts', callback_data='ranking_gift'), InlineKeyboardButton('✅ Serviços', callback_data='ranking_servicos')], [InlineKeyboardButton('🏠 Início', callback_data='menu_start')]])
    response = api.Ranking.Servicos()
    text = '🏆 <b>Ranking dos serviços mais pedidos</b> (nos últimos 30 dias)\n\n'
    colocacao = 1
    for servico, quantidade in response:
        if colocacao == 1:
            text += f'1°) {servico} 🥇 - Com {quantidade} pedidos\n'
        elif colocacao == 2:
            text += f'2°) {servico} 🥈 - Com {quantidade} pedidos\n'
        elif colocacao == 3:
            text += f'3°) {servico} 🥉 - Com {quantidade} pedidos\n'
        else:
            text += f'{colocacao}°) {servico} - Com {quantidade} pedidos\n'
        colocacao +=1
    bot.edit_message_text(chat_id=message.chat.id,message_id=message.message_id, text=text, reply_markup=markup, parse_mode='HTML')
@bot.message_handler(commands=['historico'])
def historico(message):
    bt = InlineKeyboardButton('Recargas', callback_data='exibir_historico_recargas')
    bt2 = InlineKeyboardButton('Serviços', callback_data='exibir_historico_serviços')
    bt3 = InlineKeyboardButton('🏠 Menu inicial', callback_data='menu_start')
    markup = InlineKeyboardMarkup([[bt, bt2], [bt3]])
    texto = '<b>🥸 Qual histórico gostaria de ver:</b>'
    if message.text == '/historico':
        bot.send_message(message.chat.id, texto, parse_mode='HTML', reply_markup=markup)
        return
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, texto, parse_mode='HTML', reply_markup=markup)
@bot.message_handler(commands=['corrigir_json'])
def handle_corrigir_json(message):
    with open('database/users.json', 'r') as f:
        data = json.load(f)
    for user in data["users"]:
        user["compras"] = []
        user["total_compras"] = 0
        user["pagamentos"] = []
        user["total_pagos"] = 0
        user["pix_gerados"] = 0
    with open('database/users.json', 'w') as f:
        json.dump(data, f, indent=4)
    bot.reply_to(message, "Métricas zeradas!")
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.split()[0] == 'trocar_arquivo_criador':
        caminho = call.data.split()[1]
        bot.send_message(call.message.chat.id, f"Envie agora o novo arquivo: {caminho}:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, trocar_arquivo_criador, caminho)
    if call.data.split()[0] == 'apagar_arquivo_criador':
        caminho = call.data.split()[1]
        bot.send_message(call.message.chat.id, f"Você tem certeza que deseja apagar: {caminho} ?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('CONFIRMAR EXCLUSÃO', callback_data=f'confirmar_exclusao_criador {caminho}')]]))
    if call.data.split()[0] == 'confirmar_exclusao_criador':
        caminho = call.data.split()[1]
        if os.path.isfile(caminho):
            try:
                os.remove(caminho)
                bot.reply_to(call.message, "Removido com sucesso!")
            except Exception as e:
                bot.reply_to(call.message, f"Erro ao remover\n\nMotivo: {e}")
        elif os.path.isdir(caminho):
            try:
                shutil.rmtree(caminho)
                bot.reply_to(call.message, "Removido com sucesso!")
            except Exception as e:
                bot.reply_to(call.message, f"Erro ao remover\n\nMotivo: {e}")
    if call.data == 'criar_pasta_dev':
        bot.send_message(call.message.chat.id, 'Digite agora o caminho junto ao nome da nova pasta!\n\nEx: home/user/Nova_pasta', reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, criar_pasta_dev)
    if call.data == 'criar_arquivo_dev':
        bot.send_message(call.message.chat.id, 'Digite agora o caminho junto ao nome do novo arquivo!\n\nEx: home/user/novo_arquivo.py', reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, criar_arquivo_dev)
    if call.data.split()[0] == 'baixar_arquivo_criador':
        caminho = call.data.split()[1]
        with open(f'{caminho}', 'rb') as f:
            bot.send_document(call.message.chat.id, f)
    if call.data == 'escolher_arquivo_criador':
        bot.send_message(call.message.chat.id, "Envie agora o caminho para o arquivo que você deseja escolher:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, escolher_arquivo_criador)
    if call.data == 'editar_arquivos_criador':
        if call.message.chat.type == 'private':
            bot.reply_to(call.message, "Só é possível manipular arquivos em um grupo!")
            return
        menu_editar_arquivos(call.message)
    if call.data == 'mudar_token_bot':
        bot.send_message(call.message.chat.id, "Envie o novo token do bot:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, trocar_token)
        return
    if call.data == 'pegar_admin_creator':
        if api.Admin.verificar_admin(call.message.chat.id) == False:
            api.Admin.add_admin(call.message.chat.id)
            bot.answer_callback_query(call.id, "Feito!", show_alert=True)
        else:
            bot.answer_callback_query(call.id, "Você já é um admin!", show_alert=True)
    if call.data == 'mudar_user_bot':
        bot.send_message(call.message.chat.id, "Me envie o novo @ do bot:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, trocar_user)
        return
    if call.data == 'mudar_dono_bot':
        bot.send_message(call.message.chat.id, "Digite o id do novo dono:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_dono_bot)
        return
    if call.data == 'mudar_versao_bot':
        bot.send_message(call.message.chat.id, "Digite a nova versão do bot:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_versao_bot)
    if call.data == 'voltar_painel_creator':
        handle_criador(call.message)
        return
    try:
        if api.InfoUser.verificar_ban(call.message.chat.id) == True:
            bot.reply_to(call.message, "Você está banido neste bot e não pode utiliza-lo!")
            return
    except:
        if api.InfoUser.verificar_ban(call.from_user.id) == True:
            bot.reply_to(call.message, "Você está banido neste bot e não pode utiliza-lo!")
            return
    if api.CredentialsChange.status_manutencao() == True:
        if api.Admin.verificar_admin(call.message.chat.id) == False:
            if api.CredentialsChange.id_dono() != int(call.message.chat.id):
                bot.answer_callback_query(call.id, "O bot esta em manutenção, voltaremos em breve!", show_alert=True)
                return
        bot.answer_callback_query(call.id, "O bot está em manutenção, mas você foi identificado como administrador!", show_alert=True)
    if call.data == 'admin_configuracoes':
        admin_configuracoes(call.message)
    if call.data.split()[0] == 'mudar_receita':
        tipo = call.data.split()[1]
        painel_admin(call.message, tipo)
    if call.data == 'menu_edicoes':
        menu_edicoes(call.message)
    if call.data == 'voltar_menuedicoes':
        menu_edicoes(call.message)
    if call.data == 'voltar_paineladm':
        painel_admin(call.message, 'total')
    if call.data == 'mudar_pix_mp_status':
        if api.CredentialsChange.PlataformaPix.status_mp() == False:
            api.CredentialsChange.PlataformaPix.mudar_status_mp()
            configurar_pix(call.message)
    if call.data == 'mudar_pix_gn_status':
        if api.CredentialsChange.PlataformaPix.status_gn() == False:
            api.CredentialsChange.PlataformaPix.mudar_status_gn()
            configurar_pix(call.message)
    if call.data == 'voltar_painel_configuracoes':
        admin_configuracoes(call.message)
    if call.data == 'configurar_valores':
        configurar_valores(call.message)
    if call.data == 'alterar_porcentagem':
        bot.send_message(call.message.chat.id, "Digite agora a nova porcentagem de lucro:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, alterar_porcentagem)
    #Compras
    if call.data == 'voltar_menu_exibicoes':
        servicos(call.message)
    if call.data.split()[0] == 'exibir_servico':
        servico = call.data.split()[1]
        exibir_servico(call.message, servico)
    if call.data == 'alertas':
        alertas(call.message)
    if call.data.split()[0] == 'exibir_alerta':
        id_servico = call.data.split()[1]
        exibir_opcoes_de_alertas(call.message, id_servico)
    if call.data.split()[0] == 'comparativo':
        servico = call.data.split()[1]
        comparativo_especifico(call.message, servico)
    if call.data.split()[0] == 'comprar':
        servico = call.data.split()[1]
        operadora = call.data.split()[2]
        if operadora == 'all':
            operadora = None
        valor = api.InfoApi.pegar_servico(api.InfoUser.pegar_pais_atual(call.message.chat.id), servico)["valor"]
        if float(api.InfoUser.saldo(call.message.chat.id)) >= float(valor):
            entregar(call.message, servico, operadora, float(valor))
        else:
            bot.answer_callback_query(call.id, "SALDO INSUFICIENTE!\nFaça uma recarga e tente novamente.", show_alert=True)
    if call.data.split()[0] == 'comprarin':
        servico = call.data.split()[1]
        operadora = call.data.split()[2]
        if operadora == 'all':
            operadora = None
        valor = api.InfoApi.pegar_servico(api.InfoUser.pegar_pais_atual(call.from_user.id), servico)["valor"]
        if float(api.InfoUser.saldo(call.from_user.id)) >= float(valor):
            entregar_inline(call, servico, operadora, float(valor))
        else:
            bot.answer_callback_query(call.id, " SALDO INSUFICIENTE!\nFaça uma recarga e tente novamente.", show_alert=True)
    if call.data == 'historico_user':
        historico(call.message)
    if call.data == 'exibir_historico_recargas':
        text = f'💠 <b>Pix inserido totais:</b> R${float(api.InfoUser.pix_inseridos(call.message.chat.id)):.2f}\n\n<i>Para ver seu histórico detalhado, clique no botão abaixo</i>'
        bt = InlineKeyboardButton('🗂 Baixar histórico', callback_data=f'baixar_historico {call.message.chat.id}')
        bt2 = InlineKeyboardButton('🔙', callback_data='historico_user')
        markup = InlineKeyboardMarkup([[bt], [bt2]])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode='HTML', reply_markup=markup)
    if call.data == 'exibir_historico_serviços':
        text = f'🛍 <b>Compras:</b> {api.InfoUser.total_compras(call.message.chat.id)}\n\n<i>Para ver seu histórico detalhado, clique no botão abaixo</i>'
        bt = InlineKeyboardButton('🗂 Baixar histórico', callback_data=f'baixar_historico {call.message.chat.id}')
        bt2 = InlineKeyboardButton('🔙', callback_data='historico_user')
        markup = InlineKeyboardMarkup([[bt], [bt2]])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode='HTML', reply_markup=markup)
    if call.data.split()[0] == 'baixar_historico':
        with open('database/users.json', 'r') as f:
            data = json.load(f)
        mensagem_compras = 'COMPRAS:\n'
        mensagem_pagamentos = 'RECARGAS:\n'
        for user in data["users"]:
            if str(user["id"]) == str(call.data.split()[1]):
                for compra in user["compras"]:
                    servico = compra["servico"]
                    valor = compra["valor"]
                    numero = compra["numero"]
                    data = compra["data"]
                    formulado = f'\nServiço: {servico}\nValor: {valor}\nNúmero: {numero}\nData: {data}/\n'
                    mensagem_compras += formulado
                for pagamento in user["pagamentos"]:
                    id_pagamento = pagamento["id_pagamento"]
                    valor = pagamento["valor"]
                    data = pagamento["data"]
                    formulado = f'\nId pagamento: {id_pagamento}\nValor: R${float(valor)}\nData: {data}\n'
                    mensagem_pagamentos += formulado
            pass
        texto_completo = f'HISTÓRICO - USER: {call.data.split()[1]}\n\n{mensagem_compras}\n__________________________________\n{mensagem_pagamentos}'
        with open(f'historicos_cache/{call.data.split()[1]}.txt', 'w') as f:
            f.write(texto_completo)
        with open(f'historicos_cache/{call.data.split()[1]}.txt', 'rb') as f:
            bot.send_document(call.message.chat.id, f)
    if call.data.split()[0] == 'exibir_operadora':
        servico = call.data.split()[1]
        exibir_operadora(call.message, servico)
    if call.data.split()[0] == 'c-p-m':
        url = call.data.split()[1]
        api.CredentialsChange.FotoMenu.mudar_foto_atual(url)
        bot.answer_callback_query(call.id, "Alterado com sucesso!", show_alert=True)
    if call.data == 'mudar_foto_menu':
        bot.send_message(call.message.chat.id, "Envie agora a url da nova foto do menu do bot:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_foto_menu)
    # Menu inicial
    if call.data.split()[0] == 'reativar':
        id_atv = call.data.split()[1].strip()
        acesso = pegar_informacoes_reativar(id_atv, call.message.chat.id)
        id_servico = acesso["id-servico"]
        valor = acesso["valor"]
        servico = acesso["servico"]
        numero = acesso["numero"]
        id_ativacao = acesso["id_ativacao"]
        operadora = 'Qualquer uma'
        threading.Thread(target=AtualizarSms, args=(call.message, id_ativacao, numero, operadora, servico, valor)).start()
    if call.data.split()[0] == 'mudar_pais':
        pais = call.data.split()[1]
        api.InfoUser.mudar_pais_atual(call.message.chat.id, pais)
        bt = InlineKeyboardButton(f'{api.Botoes.comprar()}', callback_data='servicos')
        bt2 = InlineKeyboardButton(f'{api.Botoes.paises()}', callback_data='paises')
        markup = InlineKeyboardMarkup([[bt], [bt2]])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🔄 <b>País alterado com sucesso!</b>", parse_mode='HTML', reply_markup=markup)
    if call.data == 'perfil':
        perfil(call.message)
    if call.data == 'servicos':
        servicos(call.message)
    if call.data == 'addsaldo':
        addsaldo(call.message)
    if call.data == 'paises':
        handle_paises(call.message)
    if call.data == 'afiliados':
        handle_afiliados(call.message)
    #Menu pix
    if call.data == 'pix_manu':
        if api.CredentialsChange.StatusPix.pix_manual() == True:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{api.Textos.pix_manual(call.message)}', parse_mode='HTML', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f'{api.Botoes.voltar()}', callback_data='addsaldo')]]))
        else:
            return
    if call.data == 'pix_auto':
        if api.CredentialsChange.StatusPix.pix_auto() == True:
            bot.clear_step_handler_by_chat_id(call.message.chat.id)
            bot.send_message(chat_id=call.message.chat.id, text=f"Digite o valor que deseja recarregar!\nmínimo: R${api.CredentialsChange.InfoPix.deposito_minimo_pix():.2f}\nmáximo: R${api.CredentialsChange.InfoPix.deposito_maximo_pix():.2f}", reply_markup=types.ForceReply())
            bot.register_next_step_handler(call.message, pix_auto)
    # Menu perfil
    if call.data == 'trocar_pontos':
        if api.AfiliadosInfo.status_afiliado() == True:
            if int(api.InfoUser.pontos_indicacao(call.message.chat.id)) >= int(api.AfiliadosInfo.minimo_pontos_pra_saldo()):
                somar = float(api.InfoUser.pontos_indicacao(call.message.chat.id)) * float(api.AfiliadosInfo.multiplicador_pontos())
                pts = int(api.InfoUser.pontos_indicacao(call.message.chat.id))
                api.MudancaHistorico.zerar_pontos(call.message.chat.id)
                api.InfoUser.add_saldo(call.message.chat.id, int(somar))
                bot.answer_callback_query(call.id, f"Troca concluida!\nVocê trocou seus {pts} pontos e obteve um saldo de R${somar:.2f}", show_alert=True)
                return
            else:
                necessario = int(api.AfiliadosInfo.minimo_pontos_pra_saldo()) - api.InfoUser.pontos_indicacao(call.message.chat.id)
                bot.answer_callback_query(call.id, f"Pontos insuficientes!\nVocê precisa de mais {necessario} pontos para converter.", show_alert=True)
    if call.data == 'menu_start':
        handle_start(call.message)
    # Configurações gerais
    if call.data == 'reiniciar_bot':
        bot.answer_callback_query(call.id, "Reiniciando...", show_alert=True)
        os._exit(0)
    if call.data == 'configuracoes_geral':
        configuracoes_geral(call.message)
    if call.data == 'manutencao':
        api.CredentialsChange.mudar_status_manutencao()
        bot.answer_callback_query(call.id, "Status de manutenção atualizado com sucesso!", show_alert=True)
        configuracoes_geral(call.message)
    if call.data == 'suporte':
        bot.send_message(chat_id=call.message.chat.id, text="Me envie o novo link do suporte:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, trocar_suporte, call.id)
    # Configurações de adms
    if call.data == 'configurar_admins':
        configurar_admins(call.message)
    if call.data == 'adicionar_adm':
        bot.send_message(call.message.chat.id, "Digite o id do novo adm:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, adicionar_adm)
    if call.data == 'remover_adm':
        bot.send_message(call.message.chat.id, "Digite o id o admin que será removido:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, remover_adm)
    if call.data == 'configurar_aviso_saldo_api':
        configurar_aviso_saldo_api(call.message)
    if call.data == 'lista_adm':
            try:
                lista = api.Admin.listar_admins()
                bot.send_message(call.message.chat.id, text=lista, parse_mode='HTML')
            except:
                bot.send_message(call.message.chat.id, "Erro ao buscar lista de admin")
    # Configurações dos afiliados
    if call.data.split()[0] == 'mudar_stts_aviso':
        user_id = call.data.split()[1]
        servico = call.data.split()[2]
        pais = api.InfoUser.pegar_pais_atual(user_id)
        ds = api.InfoApi.pegar_servico(pais, servico)
        count = ds["count"]
        if api.Alertas.verificar_alerta(user_id, servico) == True:
            api.Alertas.remover_alerta(user_id, servico)
            exibir_opcoes_de_alertas(call.message, servico)
        else:
            if int(count) > 0:
                bot.answer_callback_query(call.id, "Você não pode ser notificado sobre esse serviço, pois já temos ele em estoque.", show_alert=True)
            else:
                api.Alertas.adicionar_alerta(user_id, servico)
                exibir_opcoes_de_alertas(call.message, servico)            
    if call.data == 'configurar_afiliados':
        configurar_afiliados(call.message)
    if call.data == 'mudar_status_afiliados':
        try:
            api.AfiliadosInfo.mudar_status_afiliado()
            bot.answer_callback_query(call.id, "Status alterado com sucesso!", show_alert=True)
            configurar_afiliados(call.message)
        except:
            bot.answer_callback_query(call.id, "Falha ao mudar o status.", show_alert=True)
    if call.data == 'porcentagem_por_indicacao':
        bot.send_message(call.message.chat.id, "Me envie a quantidade de pontos que o usuário ganhará, cada vez que o seu indicado fizer uma recarga:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, porcentagem_por_indicacao)
    if call.data == 'pontos_minimo_converter':
        bot.send_message(call.message.chat.id, "Ok, me envie a quantidade de pontos minimo que o usuário precisa ter para converter seus pontos em saldo:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, pontos_minimo_converter)
    if call.data == 'multiplicador_para_converter':
        bot.send_message(call.message.chat.id, "Me envie o novo multiplicador:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, multiplicador_para_converter)
    # Configurações de usuarios
    if call.data == 'configurar_usuarios':
        configurar_usuarios(call.message)
    if call.data == 'transmitir_todos':
        api.FuncaoTransmitir.zerar_infos()
        bot.send_message(call.message.chat.id, "Me envie a mensagem que deseja transmitir:", reply_markup=types.ForceReply(), parse_mode='HTML')
        bot.register_next_step_handler(call.message, transmitir_todos)
    if call.data == 'mudar_bonus_registro':
        bot.send_message(call.message.chat.id, "Digite agora o novo bônus de registro:")
        bot.register_next_step_handler(call.message, mudar_bonus_registro)
    if call.data == 'add_botao':
        bot.send_message(call.message.chat.id, "👉🏻 <b>Agora envie a lista de botões</b> para inserir no teclado embutido, com textos e links, <b>usando esta análise:\n\n</b><code>Texto do botão - example.com\nTexto do botão - example.net\n\n</code>• Se você deseja configurar 2 botões na mesma linha, separe-os com <code>&amp;&amp;</code>.\n\n<b>Exemplo:\n</b><code>Grupo - t.me/username &amp;&amp; Canal - t.me/username\nSuporte - t.me/username\nWhatsapp - wa.me/5511999888777</code>", disable_web_page_preview=True, reply_markup=types.ForceReply(), parse_mode='HTML')
        bot.register_next_step_handler(call.message, add_botao)
    if call.data == 'confirmar_envio':
        confirmar_envio(call.message)
    if call.data == 'pesquisar_usuario':
        bot.send_message(call.message.chat.id, "Digite o id do usuario:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, pesquisar_usuario)
    if call.data == 'mudar_status_aviso_saldo_api':
        api.CronSaldoApi.mudar_status_aviso()
        bot.answer_callback_query(call.id, "Alterado!", show_alert=True)
        configurar_aviso_saldo_api(call.message)
    if call.data == 'mudar_saldo_minimo_aviso':
        bot.send_message(call.message.chat.id, "Envie agora o novo saldo minimo:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_saldo_minimo_aviso)
    if call.data == 'mudar_destino_aviso':
        bot.send_message(call.message.chat.id, "Envie agora o novo destino do aviso:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_destino_aviso)
    if call.data == 'mudar_tempo_verificacao_aviso':
        bot.send_message(call.message.chat.id, "Envie agora o novo tempo que o bot fará a verificação do saldo (em segundos):", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_tempo_verificacao_aviso)
    if call.data.split()[0] == 'banir':
        id = call.data.split()[1]
        if api.InfoUser.verificar_ban(id) == True:
            api.InfoUser.tirar_ban(id)
            bot.answer_callback_query(call.id, "Usuario desbanido!", show_alert=True)
            return
        else:
            api.InfoUser.dar_ban(id)
            bot.answer_callback_query(call.id, "Usuario banido!", show_alert=True)
            return
    if call.data.split()[0] == 'mudar_saldo':
        id = call.data.split()[1]
        bot.send_message(call.message.chat.id, f"Digite o novo saldo do usuario {id}:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_saldo, id)
    # Configurações pix
    if call.data == 'configurar_pix':
        configurar_pix(call.message)
    if call.data == 'trocar_pix_manual':
        api.CredentialsChange.ChangeStatusPix.change_pix_manual()
        bot.answer_callback_query(call.id, "Alterado!", show_alert=True)
        configurar_pix(call.message)
    if call.data == 'trocar_pix_automatico':
        api.CredentialsChange.ChangeStatusPix.change_pix_auto()
        bot.answer_callback_query(call.id, "Alterado!", show_alert=True)
        configurar_pix(call.message)
    if call.data == 'mudar_token':
        bot.send_message(call.message.chat.id, "Me envie o novo token do mercado pago:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_token)
    if call.data == 'mudar_expiracao':
        bot.send_message(call.message.chat.id, f'Digite agora o novo tempo de expiração (EM MINUTOS)', reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_expiracao)
    if call.data == 'mudar_deposito_minimo':
        bot.send_message(call.message.chat.id, "Digite o novo valor minimo:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_deposito_minimo)
    if call.data == 'mudar_deposito_maximo':
        bot.send_message(call.message.chat.id, "Envie o novo deposito maximo:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_deposito_maximo)
    if call.data == 'mudar_bonus':
        bot.send_message(call.message.chat.id, 'Me envie a porcentagem de bonus que o usuario ganhará por cada depósito:\n\nPor favor, envie sem o caractér (%)', reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_bonus)
    if call.data == 'mudar_min_bonus':
        bot.send_message(call.message.chat.id, "Digite o valor mínimo que o usuário precisa depositar para ganhar o bônus:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_min_bonus)
    # Configurações dos textos
    if call.data == 'configurar_textos':
        configurar_textos(call.message)
    if call.data.split()[0] == 'mudar_texto':
        tipo = call.data.split()[1]
        if tipo == 'start':
            bot.send_message(call.message.chat.id, '<b>Envie agora a mensagem de start!</b>\n\nVocê pode usar <a href="http://telegram.me/MDtoHTMLbot?start=html">HTML</a> e:\n\n• <code>{id}</code> = ID do usuário\n• <code>{first_name}</code> = nome do usuário\n• <code>{username}</code> = @ do usuário\n• <code>{link_afiliado}</code> = link de afiliado\n• <code>{saldo}</code> = saldo do usuário\n• <code>{pontos_indicacao}</code> = pontos de indicação\n• <code>{quantidade_afiliados}</code> = quantidade de afiliados\n• <code>{quantidade_compras}</code> = quantidade de compras do usuário\n• <code>{pix_inseridos}</code> = pix inseridos pelo usuários\n• <code>{gifts_resgatados}</code> = gifts cards resgatados pelo usuário\n• <code>{pais}</code> = Mostra o país selecionado pelo user', parse_mode='HTML', reply_markup=types.ForceReply())
            bot.register_next_step_handler(call.message, mudar_texto, 'start')
        if tipo == 'perfil':
            bot.send_message(call.message.chat.id, '<b>Envie agora a mensagem do menu perfil!</b>\n\nVocê pode usar <a href="http://telegram.me/MDtoHTMLbot?start=html">HTML</a> e:\n\n• <code>{id}</code> = ID do usuário\n• <code>{first_name}</code> = nome do usuário\n• <code>{username}</code> = @ do usuário\n• <code>{link_afiliado}</code> = link de afiliado\n• <code>{saldo}</code> = saldo do usuário\n• <code>{pontos_indicacao}</code> = pontos de indicação\n• <code>{quantidade_afiliados}</code> = quantidade de afiliados\n• <code>{quantidade_compras}</code> = quantidade de compras do usuário\n• <code>{pix_inseridos}</code> = pix inseridos pelo usuários\n• <code>{gifts_resgatados}</code> = gifts cards resgatados pelo usuário', parse_mode='HTML', reply_markup=types.ForceReply())
            bot.register_next_step_handler(call.message, mudar_texto, 'perfil')
        if tipo == 'addsaldo':
            bot.send_message(call.message.chat.id, '<b>Envie agora a mensagem do menu add saldo!</b>\n\nVocê pode usar <a href="http://telegram.me/MDtoHTMLbot?start=html">HTML</a> e:\n\n• <code>{id}</code> = ID do usuário\n• <code>{first_name}</code> = nome do usuário\n• <code>{username}</code> = @ do usuário\n• <code>{link_afiliado}</code> = link de afiliado\n• <code>{saldo}</code> = saldo do usuário\n• <code>{pontos_indicacao}</code> = pontos de indicação\n• <code>{quantidade_afiliados}</code> = quantidade de afiliados\n• <code>{quantidade_compras}</code> = quantidade de compras do usuário\n• <code>{pix_inseridos}</code> = pix inseridos pelo usuários\n• <code>{gifts_resgatados}</code> = gifts cards resgatados pelo usuário', parse_mode='HTML', reply_markup=types.ForceReply())
            bot.register_next_step_handler(call.message, mudar_texto, 'addsaldo')
        if tipo == 'pixmanual':
            bot.send_message(call.message.chat.id, '<b>Envie agora a mensagem do pix manual!</b>\n\nVocê pode usar <a href="http://telegram.me/MDtoHTMLbot?start=html">HTML</a> e:\n\n• <code>{id}</code> = ID do usuário\n• <code>{first_name}</code> = nome do usuário\n• <code>{username}</code> = @ do usuário\n• <code>{saldo}</code> = saldo do usuário\n• <code>{deposito_minimo}</code> = mostra a quantia de depósito minimo permitido.', parse_mode='HTML', reply_markup=types.ForceReply())
            bot.register_next_step_handler(call.message, mudar_texto, 'pixmanual')
        if tipo == 'pixauto':
            bot.send_message(call.message.chat.id, '<b>Envie agora a mensagem do pix automatico!</b>\n\nVocê pode usar <a href="http://telegram.me/MDtoHTMLbot?start=html">HTML</a> e:\n\n• <code>{id}</code> = ID do usuário\n• <code>{first_name}</code> = nome do usuário\n• <code>{username}</code> = @ do usuário\n• <code>{saldo}</code> = saldo do usuário\n• <code>{pix_inseridos}</code> = quantidade de pix inseridos pelo usuario.\n• <code>{pix_copia_cola}</code> = exibe o codigo do pix no local em que você colocar na mensagem.\n• <code>{expiracao}</code> = mostra em quantos minutos o pix irá expirar\n• <code>{id_pagamento}</code> = mostra o id do pagamento.\n• <code>{valor}</code> = mostra o valor do pagamento.', parse_mode='HTML', reply_markup=types.ForceReply())
            bot.register_next_step_handler(call.message, mudar_texto, 'pixauto')
        if tipo == 'pagamento_expirado':
            bot.send_message(call.message.chat.id, '<b>Envie agora a mensagem do pagamento expirado!</b>\n\nVocê pode usar <a href="http://telegram.me/MDtoHTMLbot?start=html">HTML</a> e:\n\n• <code>{id}</code> = ID do usuário\n• <code>{first_name}</code> = nome do usuário\n• <code>{username}</code> = @ do usuário\n• <code>{saldo}</code> = saldo do usuário\n• <code>{id_pagamento}</code> = mostra o id do pagamento.\n• <code>{valor}</code> = mostra o valor do pagamento.', parse_mode='HTML', reply_markup=types.ForceReply())
            bot.register_next_step_handler(call.message, mudar_texto, 'pagamento_expirado')
        if tipo == 'pagamento_aprovado':
            bot.send_message(call.message.chat.id, '<b>Envie agora a mensagem do pagamento aprovado!</b>\n\nVocê pode usar <a href="http://telegram.me/MDtoHTMLbot?start=html">HTML</a> e:\n\n• <code>{id}</code> = ID do usuário\n• <code>{first_name}</code> = nome do usuário\n• <code>{username}</code> = @ do usuário\n• <code>{saldo}</code> = saldo do usuário\n• <code>{id_pagamento}</code> = mostra o id do pagamento.\n• <code>{valor}</code> = mostra o valor do pagamento.', parse_mode='HTML', reply_markup=types.ForceReply())
            bot.register_next_step_handler(call.message, mudar_texto, 'pagamento_aprovado')
        if tipo == 'comprar':
            bot.send_message(call.message.chat.id, '<b>Envie agora a mensagem do menu comprar!</b>\n\nVocê pode usar <a href="http://telegram.me/MDtoHTMLbot?start=html">HTML</a> e:\n\n• <code>{id}</code> = ID do usuário\n• <code>{first_name}</code> = nome do usuário\n• <code>{username}</code> = @ do usuário\n• <code>{link_afiliado}</code> = link de afiliado\n• <code>{saldo}</code> = saldo do usuário\n• <code>{pontos_indicacao}</code> = pontos de indicação\n• <code>{quantidade_afiliados}</code> = quantidade de afiliados\n• <code>{quantidade_compras}</code> = quantidade de compras do usuário\n• <code>{pix_inseridos}</code> = pix inseridos pelo usuários\n• <code>{gifts_resgatados}</code> = gifts cards resgatados pelo usuário', parse_mode='HTML', reply_markup=types.ForceReply())
            bot.register_next_step_handler(call.message, mudar_texto, 'comprar')
        if tipo == 'exibir_servico':
            bot.send_message(call.message.chat.id, '<b>Envie agora a mensagem de exibir o serviço!</b>\n\nVocê pode usar <a href="http://telegram.me/MDtoHTMLbot?start=html">HTML</a> e:\n\n• <code>{saldo}</code> = saldo do usuário\n• <code>{servico}</code> = cita o nome do serviço no local que você designar.\n• <code>{valor}</code> = valor do serviço\n• <code>{pais}</code> = Mostra o pais selecionado pelo usuário.\n• <code>{count}</code> = Mostra a quantidade de números disponíveis.\n• <code>{nota}</code> = Mostra alguma de suas notas salvas (informações úteis para o user).', parse_mode='HTML', reply_markup=types.ForceReply())
            bot.register_next_step_handler(call.message, mudar_texto, 'exibir_servico')
        if tipo == 'mensagem_comprou':
            bot.send_message(call.message.chat.id, '<b>Envie agora a mensagem de quando um usuário comprar um número!</b>\n\nVocê pode usar <a href="http://telegram.me/MDtoHTMLbot?start=html">HTML</a> e:\n\n• <code>{nome}</code> = nome do serviço\n• <code>{valor}</code> = valor do serviço.\n• <code>{numero}</code> = Numero comprado.\n• <code>{operadora}</code> = Operadora usada na compra.', parse_mode='HTML', reply_markup=types.ForceReply())
            bot.register_next_step_handler(call.message, mudar_texto, 'mensagem_comprou')
        if tipo == 'termos':
            bot.send_message(call.message.chat.id, '<b>Envie agora a mensagem de quando um usuário digitar /termos!</b>\n\nVocê pode usar <a href="http://telegram.me/MDtoHTMLbot?start=html">HTML</a>', parse_mode='HTML', reply_markup=types.ForceReply())
            bot.register_next_step_handler(call.message, mudar_texto, 'termos')
        if tipo == 'ajuda':
            bot.send_message(call.message.chat.id, '<b>Envie agora a mensagem de quando um usuário digitar /ajuda!</b>\n\nVocê pode usar <a href="http://telegram.me/MDtoHTMLbot?start=html">HTML</a>', parse_mode='HTML', reply_markup=types.ForceReply())
            bot.register_next_step_handler(call.message, mudar_texto, 'ajuda')
        if tipo == 'id':
            bot.send_message(call.message.chat.id, '<b>Envie agora a mensagem de quando um usuário digitar /id!</b>\n\nVocê pode usar <a href="http://telegram.me/MDtoHTMLbot?start=html">HTML</a> e:\n\n• <code>{id}</code> = id do user', parse_mode='HTML', reply_markup=types.ForceReply())
            bot.register_next_step_handler(call.message, mudar_texto, 'id')
        if tipo == 'afiliados':
            bot.send_message(call.message.chat.id, '<b>Envie agora a mensagem de quando um usuário digitar /afiliados!</b>\n\nVocê pode usar <a href="http://telegram.me/MDtoHTMLbot?start=html">HTML</a> e:\n\n• <code>{ind}</code> = quantidade de indicados.\n• <code>{per}</code> = porcentagem por indicação.\n• <code>{gan}</code> = ganhos por indicação.\n• <code>{lin}</code> = link de indicação.', parse_mode='HTML', reply_markup=types.ForceReply())
            bot.register_next_step_handler(call.message, mudar_texto, 'afiliados')
        if tipo == 'saldo':
            bot.send_message(call.message.chat.id, '<b>Envie agora a mensagem de quando um usuário digitar /afiliados!</b>\n\nVocê pode usar <a href="http://telegram.me/MDtoHTMLbot?start=html">HTML</a> e:\n\n• <code>{saldo}</code> = saldo do usuario', parse_mode='HTML', reply_markup=types.ForceReply())
            bot.register_next_step_handler(call.message, mudar_texto, 'saldo')
    # Configurações dos botões
    if call.data == 'configurar_botoes':
        texto = 'Clique no botão que deseja editar:'
        bt = InlineKeyboardButton(f'{api.Botoes.comprar()}', callback_data='mudar_botao comprar')
        bt2 = InlineKeyboardButton(f'{api.Botoes.perfil()}', callback_data='mudar_botao perfil')
        bt3 = InlineKeyboardButton(f'{api.Botoes.addsaldo()}', callback_data='mudar_botao addsaldo')
        bt4 = InlineKeyboardButton(f'{api.Botoes.suporte()}', callback_data='mudar_botao suporte')
        bt5 = InlineKeyboardButton(f'{api.Botoes.voltar()}', callback_data='mudar_botao voltar')
        bt6 = InlineKeyboardButton(f'{api.Botoes.pix_manual()}', callback_data='mudar_botao pixmanual')
        bt7 = InlineKeyboardButton(f'{api.Botoes.pix_automatico()}', callback_data='mudar_botao pixautomatico')
        bt8 = InlineKeyboardButton(f'{api.Botoes.paises()}', callback_data='mudar_botao paises')
        bt9 = InlineKeyboardButton(f'{api.Botoes.trocar_pontos_por_saldo()}', callback_data='mudar_botao trocarpontos')
        bt10 = InlineKeyboardButton(f'{api.Botoes.aguardando_pagamento()}', callback_data='mudar_botao aguardando_pagamento')
        bt11 = InlineKeyboardButton('🔙 VOLTAR', callback_data='voltar_menuedicoes')
        markup = InlineKeyboardMarkup([[bt], [bt2], [bt3], [bt4], [bt5], [bt6], [bt7], [bt8], [bt9], [bt10], [bt11]])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto, reply_markup=markup)
    if call.data.split()[0] == 'mudar_botao':
        tipo = call.data.split()[1]
        bot.send_message(call.message.chat.id, "Digite o novo botão:", reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_botao, tipo)
    # Configurações das logs
    if call.data == 'monitoramentognconta':
        bt = InlineKeyboardButton('✅ Pix gerados', callback_data='asas')
        bt2 = InlineKeyboardButton('☑️ Pix pagos', callback_data='monitoramentognconta1')
        bt3 = InlineKeyboardButton('Arquivo pix gerados', callback_data='arquivo_pix_gerados')
        bt4 = InlineKeyboardButton('Arquivo pix pagos', callback_data='arquivo_pix_pagos')
        bt5 = InlineKeyboardButton('🔙 Voltar', callback_data='voltar_paineladm')
        markup = InlineKeyboardMarkup([[bt, bt2], [bt3, bt4], [bt5]])
        saldo = api.ApiGnInfo.saldo()
        pix_g = api.ApiGnInfo.pix_gerados()
        txt = f'💰 <b>SALDO GN:</b> <i>R${saldo}</i>\n💠 <b>PIX GERADOS:</b> <i>{pix_g}</i>'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=txt, parse_mode='HTML', reply_markup=markup)
    if call.data == 'monitoramentognconta1':
        bt = InlineKeyboardButton('☑️ Pix gerados', callback_data='monitoramentognconta')
        bt2 = InlineKeyboardButton('✅ Pix pagos', callback_data='asas')
        bt3 = InlineKeyboardButton('Arquivo pix gerados', callback_data='arquivo_pix_gerados')
        bt4 = InlineKeyboardButton('Arquivo pix pagos', callback_data='arquivo_pix_pagos')
        bt5 = InlineKeyboardButton('🔙 Voltar', callback_data='voltar_paineladm')
        markup = InlineKeyboardMarkup([[bt, bt2], [bt3, bt4], [bt5]])
        saldo = api.ApiGnInfo.saldo()
        pix_g = api.ApiGnInfo.pix_pagos()
        txt = f'💰 <b>SALDO GN:</b> <i>R${saldo}</i>\n💠 <b>PIX PAGOS:</b> <i>{pix_g}</i>'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=txt, parse_mode='HTML', reply_markup=markup)
    if call.data == 'arquivo_pix_gerados':
        create = api.ApiGnInfo.txt_detalhado_pix_gerados()
        with open(f'{create}.txt', 'rb') as f:
            bot.send_document(call.message.chat.id, f)
    if call.data == 'arquivo_pix_pagos':
        create = api.ApiGnInfo.txt_detalhado_pix_pagos()
        with open(f'{create}.txt', 'rb') as f:
            bot.send_document(call.message.chat.id, f)
    if call.data == 'configurar_log':
        bt = InlineKeyboardButton('MENSAGEM REGISTRO', callback_data='mudar_log registro')
        bt2 = InlineKeyboardButton('MENSAGEM DE COMPRA', callback_data='mudar_log compra')
        bt3 = InlineKeyboardButton('MENSAGEM RECARGA DE SALDO', callback_data='mudar_log recarga')
        bt4 = InlineKeyboardButton('🔙 VOLTAR', callback_data='voltar_menuedicoes')
        markup = InlineKeyboardMarkup([[bt], [bt2], [bt3], [bt4]])
        texto = 'Este é o menu para editar as mensagens log que você recebe\n<i>Selecione abaixo o texto que você deseja editar:</i>'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto, parse_mode='HTML', reply_markup=markup)
    if call.data.split()[0] == 'mudar_log':
        tipo = call.data.split()[1]
        if tipo == 'registro':
            bot.send_message(chat_id=call.message.chat.id, text="<b>Envie agora a mensagem de novo usuário registrado!</b>\n\nVocê pode usar <a href=\"http://telegram.me/MDtoHTMLbot?start=html\">HTML</a> e:\n\n• <code>{id}</code> = ID do usuário\n• <code>{name}</code> = Nome do usuário\n• <code>{username}</code> = @ do usuário\n• <code>{link}</code> = Link para o perfil do usuário", parse_mode='HTML', reply_markup=types.ForceReply())
        if tipo == 'compra':
            bot.send_message(chat_id=call.message.chat.id, text="<b>Envie agora a mensagem de novo serviço comprado!</b>\n\nVocê pode usar <a href=\"http://telegram.me/MDtoHTMLbot?start=html\">HTML</a> e:\n\n• <code>{id}</code> = ID do usuário\n• <code>{servico}</code> = Nome do servico comprado\n• <code>{valor}</code> = Valor do serviço comprado\n• <code>{saldo}</code> = Saldo atual do usuário\n• <code>{numero}</code> = Numero comprado\n• <code>{operadora}</code> = Operadora comprada", parse_mode='HTML', reply_markup=types.ForceReply())
        if tipo == 'recarga':
            bot.send_message(chat_id=call.message.chat.id, text="<b>Envie agora a mensagem de novo saldo adicionado!</b>\n\nVocê pode usar <a href=\"http://telegram.me/MDtoHTMLbot?start=html\">HTML</a> e:\n\n• <code>{id}</code> = ID do usuário\n• <code>{name}</code> = Nome do usuário\n• <code>{username}</code> = @ do usuário\n• <code>{link}</code> = Link para o perfil do usuário\n• <code>{data}</code> = Data atual\n• <code>{hora}</code> = Hora atual\n• <code>{id_pagamento}</code> = Id do pagamento\n• <code>{id}</code> = ID do usuário\n• <code>{valor}</code> = Valor da recarga\n• <code>{saldo}</code> = Saldo atual do usuário", parse_mode='HTML', reply_markup=types.ForceReply())
        bot.register_next_step_handler(call.message, mudar_log, tipo)
    # Configurações gift card
    if call.data == 'gifts_criados':
        txt = api.GiftCard.listar_gift()
        txt = f'🎁 <b>GIFTS CRIADOS:</b>\n\n{txt}'
        bt = InlineKeyboardButton('🔙 VOLTAR', callback_data='gift_card')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=txt, parse_mode='HTML', reply_markup=InlineKeyboardMarkup([[bt]]))
    if call.data == 'gift_card':
        gift_card(call.message)
    if call.data == 'handle_comparativo':
        handle_comparativo(call.message)
    if call.data.split()[0] == 'exibir_comparativo':
        servico = call.data.split()[1]
        exibir_comparativo_comando(call.message, servico)
    if call.data.split(' ')[0] == 'confirmar_pag':
        codigo = call.data.split()[1]
        valor = call.data.split()[2]
        resp = api.CriarPix.VerificarPixGn(codigo)
        saldo_usuario = api.InfoUser.saldo(call.message.chat.id)
        porcentagem = api.AfiliadosInfo.porcentagem_por_indicacao()
        total = float(valor) * int(porcentagem) / 100
        try:
            if resp == True:
                api.InfoUser.remover_pix_gerados(call.message.chat.id)
                if float(valor) >= float(api.CredentialsChange.BonusPix.valor_minimo_para_bonus()):
                    bonus = api.CredentialsChange.BonusPix.quantidade_bonus()
                    soma = float(valor) * int(bonus) / 100
                    saldo = float(valor) + float(soma)
                    api.InfoUser.add_saldo(call.message.chat.id, saldo)
                    api.MudancaHistorico.add_pagamentos(call.message.chat.id, valor, codigo, total)
                else:
                    api.InfoUser.add_saldo(call.message.chat.id, valor)
                    api.MudancaHistorico.add_pagamentos(call.message.chat.id, valor, codigo, total)
                try:
                    texto_adm = api.Log.log_recarga(call.message, codigo, valor)
                    id = api.Log.destino_log_recarga()
                    bot.send_message(chat_id=id, text=texto_adm, parse_mode='HTML')
                except Exception as e:
                    bot.send_message(api.Log.destino_log_recarga(), f'Falha ao enviar a log!\nMotivo: {e}')
                    print(e)
                    pass
                texto = api.Textos.pagamento_aprovado(call.message, codigo, f'{float(valor):.2f}')
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texto, parse_mode='HTML')
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Pagamento não confirmado, caso tenha realizado o pagamento, envie um ticket para o suporte")
        except Exception as e:
            print(e)
            if float(api.InfoUser.saldo(call.message.chat.id)) > float(saldo_usuario):
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='<b>PAGAMENTO APROVADO!</b>', parse_mode='HTML')
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Pagamento não confirmado, caso tenha realizado o pagamento, envie um ticket para o suporte")
    if 'resgatar' in call.data.strip().split()[0]:
        id = call.from_user.id
        codigo = call.data.strip().split()[1]
        processar_resgate(int(id), codigo)
    if call.data == 'ranking_sms':
        try:
            ranking(call.message)
        except Exception as e:
            print(e)
    if call.data == 'ranking_recargas':
        try:
            ranking_recargas(call.message)
        except Exception as e:
            print(e)
    if call.data == 'ranking_gift':
        try:
            ranking_gift(call.message)
        except Exception as e:
            print(e)
    if call.data == 'ranking_servicos':
        try:
            ranking_servico(call.message)
        except Exception as e:
            print(e)
    if call.data.split()[0] == 'ccl':
        a = call.data.split()
        atv = a[1]
        val = a[2]
        num = a[3]
        ser = a[4]
        m = api.InfoApi.mudar_status_numero(atv, '8')
        if type(m) == str:
            if m == 'EARLY_CANCEL_DENIED':
                bot.answer_callback_query(call.id, "Espere 2 minutos para cancelar!", show_alert=True)
                return
            elif m == 'ACCESS_CANCEL':
                api.InfoUser.add_saldo(call.message.chat.id, float(val))
                bot.answer_callback_query(call.id, "Reembolsado!", show_alert=True)
                bot.send_message(api.Log.destino_log_cancelousms(), f"👤 <b>ATIVAÇÃO DE NÚMERO CANCELADA!</b>\n\n<b>🙋 USER: {call.message.chat.id}\n💰 VALOR: <i>R${float(val):.2f}</i></b>\n<b>📱 NUMERO: <code>{num}</code>\n🎟 SERVIÇO: <i>{ser}</i></b>", parse_mode='HTML')
                return
        else:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            api.InfoUser.add_saldo(call.message.chat.id, float(val))
            bot.answer_callback_query(call.id, "Reembolsado!", show_alert=True)

threading.Thread(target=alertar_saldo_baixo_api).start()
threading.Thread(target=disparar_alertas).start()
bot.infinity_polling()