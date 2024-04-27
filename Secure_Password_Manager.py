import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from cryptography.fernet import Fernet
import json

# Load or generate encryption key
try:
    with open('key.key', 'rb') as file:
        key = file.read()
except FileNotFoundError:
    key = Fernet.generate_key()
    with open('key.key', 'wb') as file:
        file.write(key)

cipher_suite = Fernet(key)

# Load passwords from file (if exists)
try:
    with open('passwords.json', 'rb') as file:
        encrypted_data = file.read()
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        passwords = json.loads(decrypted_data.decode('utf-8'))
except (FileNotFoundError, json.JSONDecodeError):
    passwords = {}

def save_passwords():
    encrypted_data = cipher_suite.encrypt(json.dumps(passwords).encode('utf-8'))
    with open('passwords.json', 'wb') as file:
        file.write(encrypted_data)

def add_password():
    global website_entry, username_email_entry, password_entry, username_entry
    website = website_entry.get()
    username_email = username_email_entry.get()
    password = password_entry.get()
    username = username_entry.get()
    if username not in passwords:
        passwords[username] = {}
    passwords[username][website] = {'username_email': username_email, 'password': password}
    save_passwords()  # Save passwords to JSON file
    messagebox.showinfo("Success", "Password added successfully!")
    add_window.destroy()

def retrieve_password():
    global website_retrieve_entry, username_retrieve_entry
    website = website_retrieve_entry.get()
    username = username_retrieve_entry.get()
    if username in passwords and website in passwords[username]:
        messagebox.showinfo("Password", f"Password: {passwords[username][website]['password']}")
    else:
        messagebox.showinfo("Error", "Password not found!")
    retrieve_window.destroy()

def update_password():
    global website_update_entry, username_update_entry, new_password_entry
    website = website_update_entry.get()
    username = username_update_entry.get()
    new_password = new_password_entry.get()
    if username in passwords and website in passwords[username]:
        passwords[username][website]['password'] = new_password
        save_passwords()  # Save passwords to JSON file
        messagebox.showinfo("Success", "Password updated successfully!")
    else:
        messagebox.showinfo("Error", "Password not found!")
    update_window.destroy()

def delete_password():
    global website_delete_entry, username_delete_entry
    website = website_delete_entry.get()
    username = username_delete_entry.get()
    if username in passwords and website in passwords[username]:
        del passwords[username][website]
        save_passwords()  # Save passwords to JSON file
        messagebox.showinfo("Success", "Password deleted successfully!")
    else:
        messagebox.showinfo("Error", "Password not found!")
    delete_window.destroy()

# Home window
def home_window():
    root = tk.Tk()
    root.title("Secure Password Manager")

    def add_window_func():
        global add_window, website_entry, username_email_entry, password_entry, username_entry
        add_window = tk.Toplevel(root)
        add_window.title("Add Password")

        website_label = tk.Label(add_window, text="Website:")
        website_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        website_entry = tk.Entry(add_window)
        website_entry.grid(row=0, column=1, padx=10, pady=5)

        username_email_label = tk.Label(add_window, text="Username/Email:")
        username_email_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        username_email_entry = tk.Entry(add_window)
        username_email_entry.grid(row=1, column=1, padx=10, pady=5)

        password_label = tk.Label(add_window, text="Password:")
        password_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        password_entry = tk.Entry(add_window, show="*")
        password_entry.grid(row=2, column=1, padx=10, pady=5)

        username_label = tk.Label(add_window, text="Username:")
        username_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        username_entry = tk.Entry(add_window)
        username_entry.grid(row=3, column=1, padx=10, pady=5)

        add_button = tk.Button(add_window, text="Add Password", command=add_password)
        add_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W+tk.E)

    def retrieve_window_func():
        global retrieve_window, website_retrieve_entry, username_retrieve_entry
        retrieve_window = tk.Toplevel(root)
        retrieve_window.title("Retrieve Password")

        website_label = tk.Label(retrieve_window, text="Website:")
        website_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        website_retrieve_entry = tk.Entry(retrieve_window)
        website_retrieve_entry.grid(row=0, column=1, padx=10, pady=5)

        username_label = tk.Label(retrieve_window, text="Username:")
        username_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        username_retrieve_entry = tk.Entry(retrieve_window)
        username_retrieve_entry.grid(row=1, column=1, padx=10, pady=5)

        retrieve_button = tk.Button(retrieve_window, text="Retrieve Password", command=retrieve_password)
        retrieve_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W+tk.E)

    def update_window_func():
        global update_window, website_update_entry, username_update_entry, new_password_entry
        update_window = tk.Toplevel(root)
        update_window.title("Update Password")

        website_label = tk.Label(update_window, text="Website:")
        website_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        website_update_entry = tk.Entry(update_window)
        website_update_entry.grid(row=0, column=1, padx=10, pady=5)

        username_label = tk.Label(update_window, text="Username:")
        username_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        username_update_entry = tk.Entry(update_window)
        username_update_entry.grid(row=1, column=1, padx=10, pady=5)

        new_password_label = tk.Label(update_window, text="New Password:")
        new_password_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        new_password_entry = tk.Entry(update_window, show="*")
        new_password_entry.grid(row=2, column=1, padx=10, pady=5)

        update_button = tk.Button(update_window, text="Update Password", command=update_password)
        update_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W+tk.E)

    def delete_window_func():
        global delete_window, website_delete_entry, username_delete_entry
        delete_window = tk.Toplevel(root)
        delete_window.title("Delete Password")

        website_label = tk.Label(delete_window, text="Website:")
        website_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        website_delete_entry = tk.Entry(delete_window)
        website_delete_entry.grid(row=0, column=1, padx=10, pady=5)

        username_label = tk.Label(delete_window, text="Username:")
        username_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        username_delete_entry = tk.Entry(delete_window)
        username_delete_entry.grid(row=1, column=1, padx=10, pady=5)

        delete_button = tk.Button(delete_window, text="Delete Password", command=delete_password)
        delete_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W+tk.E)

    add_button = tk.Button(root, text="Add Password", command=add_window_func)
    add_button.grid(row=0, column=0, padx=10, pady=5)

    retrieve_button = tk.Button(root, text="Retrieve Password", command=retrieve_window_func)
    retrieve_button.grid(row=0, column=1, padx=10, pady=5)

    update_button = tk.Button(root, text="Update Password", command=update_window_func)
    update_button.grid(row=0, column=2, padx=10, pady=5)

    delete_button = tk.Button(root, text="Delete Password", command=delete_window_func)
    delete_button.grid(row=0, column=3, padx=10, pady=5)

    root.mainloop()

# Start the program
home_window()
