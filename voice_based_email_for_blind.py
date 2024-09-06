import speech_recognition as sr
import smtplib
import imaplib
import email
from gtts import gTTS
import pyglet
import os
import time

def play_tts_message(message, filename):
    tts = gTTS(text=message, lang='en')
    tts.save(filename)
    music = pyglet.media.load(filename, streaming=False)
    music.play()
    time.sleep(music.duration)
    os.remove(filename)

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        print("Processing...")

    try:
        text = recognizer.recognize_google(audio).lower()
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def main():
    # Project name announcement
    play_tts_message("Project: Voice based Email for blind", "name.mp3")

    # Login info
    login = os.getlogin()
    print(f"You are logging from : {login}")

    # Choices announcement
    play_tts_message("Option 1. Compose a mail.", "hello.mp3")
    print("Option 1. Compose a mail.")
    play_tts_message("Option 2. Check your inbox", "second.mp3")
    print("Option 2. Check your inbox")

    # User choice
    text = recognize_speech()

    if text:
        if any(option in text for option in ['1', 'a', 'one']):
            # Compose and send email
            play_tts_message("Please dictate your message.", "message.mp3")
            msg = recognize_speech()

            if msg:
                try:
                    # Send the email
                    mail = smtplib.SMTP('smtp.gmail.com', 587)
                    mail.ehlo()
                    mail.starttls()
                    mail.login('anjalishaw965@gmail.com', 'bhpaudtchdhfpwbl')  # Replace with your email and password
                    mail.sendmail('anjalishaw965@gmail.com', 'ashawcloud@gmail.com', msg)  # Replace with recipient email
                    mail.close()

                    print("Congrats! Your mail has been sent.")
                    play_tts_message("Congrats! Your mail has been sent.", "send.mp3")
                except Exception as e:
                    print(f"Failed to send email: {e}")
            else:
                print("Failed to recognize email message.")
                
        elif any(option in text for option in ['2', 'b', 'two']):
            # Check inbox
            try:
                mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
                mail.login('anjalishaw965@gmail.com', 'bhpaudtchdhfpwbl')  # Replace with your email and password
                mail.select('Inbox')

                # Total number of mails
                status, data = mail.search(None, 'ALL')
                email_ids = data[0].split()
                num_emails = len(email_ids)
                print(f"Number of mails in your inbox: {num_emails}")
                play_tts_message(f"Total mails are: {num_emails}", "total.mp3")

                # Check unseen emails
                status, data = mail.search(None, 'UNSEEN')
                unseen_ids = data[0].split()
                num_unseen = len(unseen_ids)
                print(f"Number of unseen mails: {num_unseen}")
                play_tts_message(f"Your unseen mails: {num_unseen}", "unseen.mp3")

                # Fetch the most recent email
                if email_ids:
                    latest_email_id = email_ids[-1]
                    status, data = mail.fetch(latest_email_id, '(RFC822)')
                    raw_email = data[0][1].decode("utf-8")
                    email_message = email.message_from_string(raw_email)
                    from_ = email_message['From']
                    subject = email_message['Subject']
                    print(f"From: {from_}")
                    print(f"Subject: {subject}")
                    play_tts_message(f"From: {from_}. Subject: {subject}", "mail.mp3")

                    # Email body
                    if email_message.is_multipart():
                        for part in email_message.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode("utf-8")
                                break
                    else:
                        body = email_message.get_payload(decode=True).decode("utf-8")

                    print(f"Body: {body}")
                    play_tts_message(f"Body: {body}", "body.mp3")

                mail.close()
                mail.logout()
            except Exception as e:
                print(f"Failed to check inbox: {e}")
        else:
            print("Invalid choice. Please try again.")
            play_tts_message("Invalid choice. Please try again.", "invalid_choice.mp3")

if __name__ == "__main__":
    main()
