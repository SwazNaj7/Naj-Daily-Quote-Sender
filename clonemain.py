import requests
import random
import json
import datetime
import os
from email.message import EmailMessage
import ssl
import smtplib
import textwrap
import time
import customtkinter
import re

email_sender = ''  # Where the email comes from
email_password = ""  # The email the quote is sent to

# These lines format today's date into Month-DD-YYYY
current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%b %d, %Y")


def show_error_popup():
    error_popup = customtkinter.CTkToplevel(app)
    error_popup.title("Error")
    error_popup.geometry("300x100")

    error_message = customtkinter.CTkLabel(
        error_popup, text="Email is not valid, please enter gmail")
    error_message.pack(padx=20, pady=10)

# Function used to send the email with data from the quotes API


def send_email(quote, author, category):
    email = email_entry.get()

    gmail_pattern = re.match(r"^\w+@gmail\.com$", email)

    if gmail_pattern:
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email
        em['Subject'] = 'Daily Quote from Naj'

        # Wrap text so long quotes will not look offset
        wrapped_quote = textwrap.fill(quote, width=100)
        body = f'''
        Good day, {email.split('@')[0]}!

        Here is Today's Quote for {formatted_time}:

        {wrapped_quote}

        Author: {author}
        Category: {category.title()}

        Sent using Python Script made by Naj
        '''
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            try:
                # Login to the quote sending email
                smtp.login(email_sender, email_password)
                # Send email
                smtp.send_message(em)
                print("Email Sent!!")
                button_function()
            except Exception as e:
                print("Error sending email: ", str(e))
                show_error_popup()
# Function used to get the quote from the API


def get_random_quote():
    # Used to track program execution time
    start_time = time.time()
    try:
        # From the api link, we format the category so that we can select a random quote from that category
        api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(
            random.choice(selected_categories))
        # Using the requests library we then get the info from the API using an API key
        response = requests.get(
            api_url, headers={'X-Api-Key': 'dEA4YsCa+3liPOnKEaE9mQ==feMmoc3sFdjz8wWd'})

        # If the request was successful, we load the json file
        if response.status_code == 200:
            # Parse the json to a python dict
            data = json.loads(response.text)

            # Extract needed items from the parsed json file
            for item in data:
                send_email(item['quote'], item['author'], item['category'])

        else:
            print("Error while getting quote")
    # Use exception as e to catch the exact error message that occured
    except Exception as e:
        print("Something went wrong, please try again", str(e))
    finally:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Program execution time: {elapsed_time:.2f} seconds")

#Function used to schedule the email to send at 8 AM daily
def schedule_daily_email():
    while True:
        current_time = datetime.datetime.now().time()
        
        #Creates time and sets it to 9:00
        scheduled_time = datetime.time(9, 0, 0)
        
        #Subtracts the current time from the scheduled time
        time_until_next_email = datetime.datetime.combine(datetime.date.today(), scheduled_time) - datetime.datetime.combine(datetime.date.today(), current_time)
        
        if time_until_next_email.total_seconds() < 0:
            time_until_next_email += datetime.timedelta(days=1)
            
        time.sleep(time_until_next_email.total_seconds())
        
        get_random_quote()

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("600x400")
app.title("Naj Daily Quotes")
app.iconbitmap(r'C:\\Users\\Naj\Documents\Desktop Folders\\Coding Projects\\Naj - Python Stuff\\Personal Projects\\Naj - Daily Quote Generator\\GUI Icon\\email_icon.ico')


def switch_event():
    selected_value = switch_var.get()
    for category, check_var in checkox_categories.items():
        check_var.set(selected_value)
    update_selected_categories()


def update_selected_categories():
    for category, check_var in checkox_categories.items():
        if check_var.get() == "on":
            if category not in selected_categories:
                selected_categories.append(category)

        else:
            if category in selected_categories:
                selected_categories.remove(category)


def button_function():
    email_get = email_entry.get()

    message = f"Quotes being sent to {email_get}, press enter to close!!"

    new_window = customtkinter.CTkToplevel(app)
    new_window.title("Quotes Sent")
    new_window.focus()

    message_label = customtkinter.CTkLabel(new_window, text=message)
    message_label.pack(padx=20, pady=10)

    new_window.bind('<Return>', lambda event=None: close_and_focus(new_window))


def close_and_focus(new_window):
    new_window.focus_force()
    app.destroy()


def optionmenu_callback(choice):
    print("optionmenu dropdown clicked: ", choice)


def checkbox_event():
    update_selected_categories()
    if len(selected_categories) <= 1:
        print("Category selected, current value:", selected_categories)
    else:
        print("Categories selected, current value:", selected_categories)


switch_var = customtkinter.StringVar(value="off")
switch = customtkinter.CTkSwitch(
    app, text="Select All", command=switch_event, variable=switch_var, onvalue="on", offvalue="off")
switch.pack(side="right", padx=20, pady=10)

main_header = customtkinter.CTkLabel(
    app, text="Daily Quotes from Naj", fg_color="transparent", font=('Arial', 30, 'bold'))
main_header.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)

scrollable_frame = customtkinter.CTkScrollableFrame(
    master=app, width=300, height=100)
scrollable_frame.place(x=145, y=140)

categories = [
    'age', 'alone', 'amazing', 'anger', 'architecture', 'art', 'attitude',
    'beauty', 'best', 'birthday', 'business', 'car', 'change', 'communications',
    'computers', 'cool', 'courage', 'dad', 'dating', 'death', 'design', 'dreams',
    'education', 'environmental', 'equality', 'experience', 'failure', 'faith',
    'family', 'famous', 'fear', 'fitness', 'food', 'forgiveness', 'freedom',
    'friendship', 'funny', 'future', 'god', 'good', 'government', 'graduation',
    'great', 'happiness', 'health', 'history', 'home', 'hope', 'humor', 'imagination',
    'inspirational', 'intelligence', 'jealousy', 'knowledge', 'leadership', 'learning',
    'legal', 'life', 'love', 'marriage', 'medical', 'men', 'mom', 'money', 'morning',
    'movies', 'success']

checkox_categories = {}
for category in categories:
    check_var = customtkinter.StringVar(value="off")
    checkox_categories[category] = check_var
    checkbox = customtkinter.CTkCheckBox(master=scrollable_frame, text=category,
                                        command=checkbox_event, variable=check_var, onvalue="on", offvalue="off")
    checkbox.pack(padx=20, pady=10)

selected_categories = []

email_entry = customtkinter.CTkEntry(
    master=app, placeholder_text="Email - (@gmail.com)", width=200, height=30)
email_entry.place(relx=0.5, rely=0.26, anchor=customtkinter.CENTER)

button = customtkinter.CTkButton(
    app, text="Send Quotes!", command=get_random_quote)
button.place(relx=0.5, rely=0.93, anchor=customtkinter.CENTER)

if __name__ == "__main__":
    app.mainloop()
