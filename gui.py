from tkinter import *
from tkinter import messagebox, Tk, Label, Entry, Button, StringVar
from PIL import Image, ImageTk
import pyperclip
import requests

API_URL = "http://127.0.0.1:5000/api/shorten"

def shorten_url():
    long_url = url_entry.get()
    response = requests.post(API_URL, json={'url': long_url})

    if response.status_code == 200:
        short_url = response.json()['short_url']
        result.set(f"Shortened URL: {short_url}")
    else:
        messagebox.showerror("Error", "An error occurred while shortening the URL.")

def copy_to_clipboard():
    clipboard_text = result.get()
    if clipboard_text:
        pyperclip.copy(clipboard_text)
        messagebox.showinfo("Copied", "Shortened URL copied to clipboard.")
    else:
        messagebox.showerror("Error", "No shortened URL to copy.")

def closing():
    root.destroy()

def resize_image(event):
    global bg_image_resized, bg_label
    image = Image.open("static/images/shrek2.jpeg")
    image = image.resize((event.width, event.height), Image.LANCZOS)
    bg_image_resized = ImageTk.PhotoImage(image)
    bg_label.config(image=bg_image_resized)

root = Tk()
root.title("URL Shortener")
root.geometry("800x600")
root.wm_iconbitmap("static/images/Shrek.ico")

bg_image = Image.open("static/images/shrek2.jpeg")
bg_image_resized = ImageTk.PhotoImage(bg_image)
bg_label = Label(root, image=bg_image_resized)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

root.bind('<Configure>', resize_image)

frame = Frame(root, padx=20, pady=20, bg='#13D8E8')
frame.place(relx=0.5, rely=0.5, anchor='center')

Label(frame, text="Enter your URL:").grid(row=0, column=0)

url_entry = Entry(frame, width=50)
url_entry.grid(row=0, column=1)

result = StringVar()
output_label = Label(frame, textvariable=result, bg='#13D8E8')
output_label.grid(row=1, column=1)

Button(frame, text="Shorten", command=shorten_url).grid(row=2, column=1, pady=10)
Button(frame, text="Copy", command=copy_to_clipboard).grid(row=3, column=1, pady=10)

root.protocol("WM_DELETE_WINDOW", closing)
root.mainloop()
