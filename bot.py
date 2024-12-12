from instagrapi import Client
import json
import time
import os
import random
import argparse

def seconds_to_time(seconds):
    minutes = seconds // 60
    seconds %= 60
    return f'{minutes:02}:{seconds:02}'


def connect(username, password, request_timeout=7):
    cl = Client(request_timeout=request_timeout)

    if os.path.exists("session.json"):
        cl.load_settings("session.json")
        print("Loaded session from file")
    else:
        print("No session file found, creating new one")
        if username is None or password is None:
            raise ValueError("Username and password are required")
        cl.login(username, password)
        cl.dump_settings("session.json")

    return cl

def reconnect(username, password, request_timeout=7):
    cl = Client(request_timeout=request_timeout)
    if username is None or password is None:
        raise ValueError("Username and password are required")
    cl.login(username, password)
    cl.dump_settings("session.json")
    return cl


def get_user_thread(cl, target_user):
    threads = cl.direct_threads()
    for thread in threads:
        for user in thread.users:
            if user.username == target_user["name"]:
                return thread
            

def post_reel(cl, downloaded_video, caption):
    try:
        return cl.clip_upload(downloaded_video, caption)
    except Exception as e:
        print(e)
        return None


def send_message(cl, message, thread_id):
    try:
        print(f"Sending message: {message}")
        return cl.direct_send(message, thread_ids=[thread_id])
    except Exception as e:
        print(e)
        return None
    

def get_caption(messages, i, info_messages, target_user):
    ''' Devuelve una descripción para el reel
        Si el mensaje inmediatamente después del reel es un texto, se usa ese
        Sino, usa una descripción aleatoria
    '''
    if i > 0: # Si el reel no es el último mensaje (tiene mensaje siguiente)
        next_message = messages[i - 1] # Agarra el mensaje siguiente

        is_text = next_message.item_type == "text" # Comprobar si el siguiente es un mensaje de texto
        is_from_target_user = next_message.user_id == target_user["id"] # Comprobar si el siguiente es del usuario target

        if is_text and is_from_target_user:
            caption = next_message.text # Se usa el mensaje como caption
        else:
            caption = random.choice(info_messages["caption"]) # Sino, descripción aleatoria
    else:
        caption = random.choice(info_messages["caption"]) # Lo mismo si el reel es el último mensaje

    return caption


def wait_random_time(min, max):
    wait_time = random.randint(min, max)
    for i in range(1, wait_time):
        text = f"Time till next check: {seconds_to_time(wait_time - i)}"
        #print(text, end='\r', flush=True)
        print(text)
        time.sleep(1)  # Wait for 1 second


def run_bot(cl, target_user, username, password):
    posted_reels = json.loads(open("posted_reels.json").read()) # La lista de los reels ya publicados
    info_messages = json.loads(open("info_messages.json").read()) # Diccionario de mensajes aleatorios

    print("Alrighty, starting this!")

    while True:
        try:
            # Obtener la "thread" y los mensajes del usuario
            target_thread = get_user_thread(cl, target_user)
            messages = target_thread.messages

            # Leer todos los mensajes y verificar si recibiste un nuevo reel
            print("\nReading messages...\n")
            print(f"Number of messages: {len(messages)}")
            for i in range(len(messages)):
                message = messages[i]

                if message.item_type == "clip": # Si es un reel
                    print(f"Message {i} is a reel!")
                    media = message.clip # Extraer el video

                    caption = get_caption(messages, i, info_messages, target_user) # Obtener la descripción que va a ir en el reel


                    if media.pk not in posted_reels: # Si el reel no ha sido publicado
                        print(f"Not posted yet!")
                        print(f"Downloading video...")
                        downloaded_video = cl.video_download(media.pk) # Descargar el reel
                        
                        print(f"Posting video {downloaded_video}...")
                        video = post_reel(cl, downloaded_video, caption) # Publicar el reel

                        if video: # Si fue publicado correctamente
                            # Enviar un mensaje al usuario
                            message_text = random.choice(info_messages["success"])

                            message = send_message(cl, message_text, target_thread.id)

                            print(f"Video posted!")
                            print(f"Caption: {caption}")
                            posted_reels.append(media.pk)
                        else:
                            print("Video couldn't be posted")
                    else:
                        print("Video already posted\n")

            json.dump(posted_reels, open("posted_reels.json", "w")) # Guardar la lista de reels publicados

            wait_random_time(2, 30) # Espera 2 a 30 segundos para hacer una nueva comprobación


        # Si algo sale mal, se escribe en un log así nomás y se envía un mensaje al usuario
        except Exception as e:
            with open("log.txt", "w") as log:
                log.write(str(e)) # Guarda que esto reescribe el archivo de log
            print(f"Error: {e}")
            error_text = random.choice(info_messages["error"])
            #cl.direct_send(f"{error_text}", thread_ids=[target_thread.id])
            if str(e) == "login_required":
                print("Trying to login again...")
                wait_random_time(2, 7)
                cl = reconnect(username, password)
            else:
                break


def main():
    # Toma los argumentos de consola
    argparser = argparse.ArgumentParser(description="IG Bot")
    argparser.add_argument("--username", type=str, default="_arbot", help="Username")
    argparser.add_argument("--password", type=str, default="panchos", help="Password")
    argparser.add_argument("--target-user", type=str, default="forbenaj", help="Target user") # El usuario que va a enviarle mensajes al bot
    argparser.add_argument("--target-id", type=int, default=3588598670, help="Target thread") # Su id (capaz no haga falta ponerlo, voy a buscar la forma)
    args = argparser.parse_args()
    # Ej: python bot.py --username _arbot --password mypassword --target-user forbenaj

    # Crea el cliente e inicia sesión
    print("Trying to connect...")
    cl = connect(args.username, args.password)

    # Ejecuta el bot
    target_user = {"name": args.target_user, "id": args.target_id}
    run_bot(cl, target_user, args.username, args.password)


if __name__ == "__main__":
    main()