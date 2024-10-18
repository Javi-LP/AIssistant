from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import tiktoken
import dbManager

db_cursor = dbManager.connect_db()
# Inicializamos el modelo para contaje de tokens
enc = tiktoken.get_encoding("o200k_base")
assert enc.decode(enc.encode("hello world")) == "hello world"
enc = tiktoken.encoding_for_model("gpt-3.5-turbo")


# Función que será llamada cuando se use el comando /start
def start(update, context):
    context.user_data['authenticate'] = False
    context.user_data['usedTokens'] = 0
    context.user_data['maxTokens'] = 0
    context.user_data['code'] = None

    context.bot.send_message(chat_id=update.effective_chat.id, text="Hola! Soy el asistente IA de MINOMBRE. \nPara mayor"
                                                                    "fluidez a la hora de interactuar con su curriculum,"
                                                                    "él mismo ha pensado que sería buena idea delegar"
                                                                    " esta tarea. \nEmpezaré hablandole un poco"
                                                                    "sobre mi. Soy un modelo de lenguaje con generación"
                                                                    "aumentada por recuperación. He sido provista de"
                                                                    "un gran contexto sobre la vida tanto laboral como "
                                                                    "personal de mi creador. Por lo tanto, ofreceré "
                                                                    "respuestas de manera precisa a cualquier pregunta"
                                                                    " que se me formule sobre el curriculum vitae de mi"
                                                                    " creador.")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Escribe el codigo de usuario: ")


def echo(update, context):
    received_message = update.message.text
    authenticate = context.user_data.get('authenticate', False)

    if authenticate:
        url = "http://127.0.0.1:8000/ask/"
        payload = {"question": received_message}
        response = requests.post(url, json=payload)
        tokens = enc.encode(received_message)
        context.user_data['usedTokens'] += len(tokens)

        if response.status_code == 200:
            data = response.json()  # Obtener los datos en formato JSON
            tokens = enc.encode(data['answer']['result'])
            context.user_data['usedTokens'] += len(tokens)
            print(data)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"{data['answer']['result']}\n\n "
                                                                            f"({context.user_data['usedTokens']}/{context.user_data['maxTokens']}) Tokens usados")
            # Guardamos la interaccion del usuario
            dbManager.save_interaction(db_cursor, context.user_data['code'], str(received_message),
                                       str(data['answer']['result']))
            # Actualizamos los tokens utilizados
            dbManager.update_code(db_cursor, context.user_data['code'], context.user_data['usedTokens'])

            result = dbManager.check_code(db_cursor, context.user_data['code'])
            context.user_data['authenticate'] = result["auth"]
            context.user_data['usedTokens'] = result["usedTokens"]
            context.user_data['maxTokens'] = result["maxTokens"]
            context.user_data['code'] = result["code"]

        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="El servicio esta ocupado. Intentelo mas tarde")

    else:
        if not isinstance(received_message, str):
            context.bot.send_message(chat_id=update.effective_chat.id, text="El código no tiene el formato deseado")
        else:
            result = dbManager.check_code(db_cursor, received_message)
            context.user_data['authenticate'] = result["auth"]
            context.user_data['usedTokens'] = result["usedTokens"]
            context.user_data['maxTokens'] = result["maxTokens"]
            context.user_data['code'] = result["code"]

            if context.user_data['authenticate'] and context.user_data['usedTokens'] < context.user_data['maxTokens']:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=f"Autorizado. Le quedan {context.user_data['maxTokens'] - context.user_data['usedTokens']} Tokens.")
            elif not context.user_data['authenticate'] and context.user_data['usedTokens'] >= context.user_data['maxTokens']:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="Ha gastado todos sus tokens. Pongase en contacto con Javier")
            else:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="El codigo es incorrecto. Pruebe otra vez.")


# Función principal para iniciar el bot
def main():
    # Coloca aquí el Token que te dio el BotFather
    TOKEN = "BOT TOKEN"

    # Crea el updater y el dispatcher
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Añade un manejador de comando para el comando /start
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # Añade un manejador para cualquier mensaje de texto
    echo_handler = MessageHandler(Filters.text & ~Filters.command, echo)
    dispatcher.add_handler(echo_handler)

    # Inicia el bot
    updater.start_polling()

    # Mantén el bot corriendo hasta que se detenga manualmente
    updater.idle()


if __name__ == '__main__':
    main()
