from instagrapi import Client
import json
import time
import os
import random

def seconds_to_time(seconds):
    minutes = seconds // 60
    seconds %= 60
    return f'{minutes:02}:{seconds:02}'


# Initialize the client and log in
cl = Client()
cl.login("powlowbot", "panchos")

media=None
text = ""

posted = []


try:
    with open("posted.txt","r") as file:
        posted = json.loads(file.read())
except:
    pass


# Get a list of direct threads

# Define the username of the specific user you're interested in
target_username = "forbenaj"

# Find the thread associated with the specific user
target_thread = None



while True:
    try:
        threads = cl.direct_threads()
        for thread in threads:
            for user in thread.users:
                if user.username == target_username:
                    target_thread = thread
                    break
            if target_thread:
                break
        if target_thread:
            # Get the messages in the thread
            messages = target_thread.messages
            for message in messages:
                if message.item_type == "clip":
                    media = message.clip
                    print("Is reel!")
                    if media.pk not in posted:
                        print("Not posted yet! Posting...")
                        downloaded_video = cl.video_download(media.pk)
                        cl.clip_upload(downloaded_video,"wowee")
                        cl.direct_send("Posted! Yipee!!", thread_ids=[target_thread.id])
                        posted.append(media.pk)
            with open("posted.txt","w") as file:
                json.dump(posted,file)
            print("saved")
            waitTime = random.randint(2,30)
            for i in range(1,waitTime):
                text = f"Seconds till next post: {seconds_to_time(waitTime-i)}"
                print(text, end='\r', flush=True)
                time.sleep(1)  # Wait for 1 second
        else:
            print("Thread with the specified user not found.")
    except Exception as e:
        with open("log.txt", "w") as log:
            log.write(str(e))
        os.system('shutdown /s /f /t 300')
        cl.direct_send("Bro PC about to shutdown", thread_ids=[target_thread.id])
        

'''from instagrapi import Client




cl = Client()
cl.login("powlowbot", "panchos")


my_messages = cl.direct_thread_by_participants([3588598670])



while True:
    text = input("Insert msg n°: ")
    print(my_messages[int(text)])
'''