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
cl = Client(request_timeout=7)


cl.load_settings("session.json")

print("Logging in...")
cl.login("powlowbot", "panchos")


#cl.dump_settings("session.json")


media=None
caption = ""
posted = []
running = True

with open("posted.txt","r") as file:
    posted = json.loads(file.read())





print("Getting messages...")


target_user = {"name": "forbenaj", "id": 3588598670}
target_thread = None


print("Alrighty, starting this!")

while running:
    try:
        # Get the thread by user
        threads = cl.direct_threads()
        for thread in threads:
            for user in thread.users:
                if user.username == target_user["name"]:
                    target_thread = thread
                    break
            if target_thread:
                break

        # Get the messages in the thread
        messages = target_thread.messages

        # Iterate through messages and check if you received a new reel
        for i in range(len(messages)):
            message = messages[i]

            if message.item_type == "clip":
                media = message.clip

                if i > 0 and messages[i-1].item_type == "text" and messages[i-1].user_id == target_user["id"]:
                    caption = messages[i-1].text
                else:
                    caption = "wowee"

                # If reel is not posted, download it and post it
                if media.pk not in posted:
                    print("Found new message! Posting...")

                    downloaded_video = cl.video_download(media.pk)
                    try:
                        print("this would post...")
                        #cl.clip_upload(downloaded_video,caption)
                    except Exception as e:
                        print(e)

                    # Send a message to user when the video is posted
                    print("Posted. Sending response...")
                    cl.direct_send("Posted!! Yipee!!", thread_ids=[target_thread.id])
                    
                    posted.append(media.pk)

        with open("posted.txt","w") as file:
            json.dump(posted,file)
        waitTime = random.randint(2,30)

        for i in range(1,waitTime):
            text = f"Time till next check: {seconds_to_time(waitTime-i)}"
            print(text, end='\r', flush=True)
            time.sleep(1)  # Wait for 1 second

    except Exception as e:
        with open("log.txt", "w") as log:
            log.write(str(e))
        print(e)
        os.system('shutdown /s /f /t 300')
        cl.direct_send(f"Bro PC about to shutdown, this was the error:\n{e}", thread_ids=[target_thread.id])

    
