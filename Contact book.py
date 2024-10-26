import tkinter as tk
from tkinter import messagebox
import csv
import os

# File where contacts are stored
CONTACTS_FILE = 'ContactBook.csv'

# Function to add a contact to the CSV file
def add_contact():
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    email = entry_email.get()
    country_name = entry_country_name.get()
    phone = entry_phone.get()
    address = entry_address.get()

    if not first_name or not last_name or not email or not phone or not address or not country_name:
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    with open(CONTACTS_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([first_name, last_name, email, country_name, phone, address])
        messagebox.showinfo("Contact Added", "Contact successfully added!")
        clear_form()


# Function to search for a contact
def search_contact():
    global found_contact
    search_name = entry_search.get()
    if not search_name:
        messagebox.showwarning("Input Error", "Please enter a name to search.")
        return

    found = False
    with open(CONTACTS_FILE, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if f"{row[0]} {row[1]}" == search_name:
                contact_details.config(state='normal')
                contact_details.delete(1.0, tk.END)
                contact_details.insert(tk.END, f"Name: {row[0]} {row[1]}\n")
                contact_details.insert(tk.END, f"Email: {row[2]}\n")
                contact_details.insert(tk.END, f"Country: {row[3]}\n")
                contact_details.insert(tk.END, f"Phone: {row[4]}\n")
                contact_details.insert(tk.END, f"Address: {row[5]}\n")
                contact_details.config(state='disabled')
                btn_update.config(state='normal')  # Enable update button
                found_contact = row  # Store the found contact for updating
                found = True
                break

    if not found:
        messagebox.showinfo("Not Found", "No contact found with that name.")
        btn_update.config(state='disabled')


# Function to open the update contact window
def update_contact_window():
    update_window = tk.Toplevel(root)
    update_window.title("Update Contact")
    update_window.geometry("450x550")
    update_window.configure(bg="black")

    # Title
    title_label = tk.Label(update_window, text="Update Contact",
                           font=("Helvetica", 18, "bold"), fg="white", bg="black")
    title_label.grid(row=0, column=1, columnspan=1, pady=20)

    # Pre-fill the fields with the current contact details
    tk.Label(update_window, text="First Name", fg="white", bg="black", font=('calibri', 12)).grid(row=1, column=0,
                                                                                                  padx=15, pady=10)
    entry_update_first = tk.Entry(update_window, width=45)
    entry_update_first.grid(row=1, column=1, padx=10, pady=8)
    entry_update_first.insert(0, found_contact[0])

    tk.Label(update_window, text="Last Name", fg="white", bg="black", font=('calibri', 12)).grid(row=2, column=0,
                                                                                                 padx=10, pady=10)
    entry_update_last = tk.Entry(update_window, width=45)
    entry_update_last.grid(row=2, column=1, padx=10, pady=5)
    entry_update_last.insert(0, found_contact[1])

    tk.Label(update_window, text="Email", fg="white", bg="black", font=('calibri', 12)).grid(row=3, column=0, padx=10,
                                                                                             pady=10)
    entry_update_email = tk.Entry(update_window, width=45)
    entry_update_email.grid(row=3, column=1, padx=10, pady=5)
    entry_update_email.insert(0, found_contact[2])

    tk.Label(update_window, text="Country Name", fg="white", bg="black", font=('calibri', 12)).grid(row=4, column=0,
                                                                                                    padx=10, pady=10)
    entry_update_country = tk.Entry(update_window, width=45)
    entry_update_country.grid(row=4, column=1, padx=10, pady=5)
    entry_update_country.insert(0, found_contact[3])

    tk.Label(update_window, text="Phone", fg="white", bg="black", font=('calibri', 12)).grid(row=5, column=0, padx=10,
                                                                                             pady=10)
    entry_update_phone = tk.Entry(update_window, width=45)
    entry_update_phone.grid(row=5, column=1, padx=10, pady=5)
    entry_update_phone.insert(0, found_contact[4])

    tk.Label(update_window, text="Address", fg="white", bg="black", font=('calibri', 12)).grid(row=6, column=0, padx=10,
                                                                                               pady=10)
    entry_update_address = tk.Entry(update_window, width=45)
    entry_update_address.grid(row=6, column=1, padx=10, pady=5)
    entry_update_address.insert(0, found_contact[5])

    # Function to save updated contact details
    def save_updated_contact():
        first_name = entry_update_first.get()
        last_name = entry_update_last.get()
        email = entry_update_email.get()
        country_name = entry_update_country.get()
        phone = entry_update_phone.get()
        address = entry_update_address.get()

        if not first_name or not last_name or not email or not phone or not address or not country_name:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        updated_contacts = []
        with open(CONTACTS_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row == found_contact:
                    updated_contacts.append([first_name, last_name, email, country_name, phone, address])
                else:
                    updated_contacts.append(row)

        with open(CONTACTS_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(updated_contacts)

        messagebox.showinfo("Update", "Contact successfully updated!")
        update_window.destroy()  # Close the update window after saving

    # Save button for the update window
    tk.Button(update_window, text="Save", command=save_updated_contact, bg="gray", fg="black", width=10, font=('calibri',
    10)).grid(row=7,column=1,columnspan=1,pady=15)


# Function to clear input fields and contact details
def clear_form():
    entry_first_name.delete(0, tk.END)
    entry_last_name.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_country_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_search.delete(0, tk.END)
    contact_details.config(state='normal')
    contact_details.delete(1.0, tk.END)
    contact_details.config(state='disabled')
    btn_update.config(state='disabled')


# Initialize main window
root = tk.Tk()
root.title("Contact Book")
root.geometry("510x660")
root.configure(bg="black")

# Title
title_label = tk.Label(root, text="Contact Book",
                       font=("Helvetica", 22, "bold"), fg="white", bg="black")
title_label.grid(row=0, column=1, columnspan=1, pady=20)

# Input fields and labels
tk.Label(root, text="First Name", fg="white", bg="black", font=('calibri', 12)).grid(row=1, column=0, padx=15, pady=5)
entry_first_name = tk.Entry(root, width=50)
entry_first_name.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Last Name", fg="white", bg="black", font=('calibri', 12)).grid(row=2, column=0, padx=10, pady=5)
entry_last_name = tk.Entry(root, width=50)
entry_last_name.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Email", fg="white", bg="black", font=('calibri', 12)).grid(row=3, column=0, padx=10, pady=5)
entry_email = tk.Entry(root, width=50)
entry_email.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Country Name", fg="white", bg="black", font=('calibri', 12)).grid(row=4, column=0, padx=10, pady=5)
entry_country_name = tk.Entry(root, width=50)
entry_country_name.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Phone", fg="white", bg="black", font=('calibri', 12)).grid(row=5, column=0, padx=10, pady=5)
entry_phone = tk.Entry(root, width=50)
entry_phone.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Address", fg="white", bg="black", font=('calibri', 12)).grid(row=6, column=0, padx=10, pady=5)
entry_address = tk.Entry(root, width=50)
entry_address.grid(row=6, column=1, padx=10, pady=5)

# Buttons for add, cancel, search, and update
btn_add = tk.Button(root, text="Add", command=add_contact, bg="gray", fg="black", width=10)
btn_add.grid(row=7, column=1, padx=10, pady=5)

btn_cancel = tk.Button(root, text="Clear", command=clear_form, bg="gray", fg="black", width=10)
btn_cancel.grid(row=8, column=1, padx=10, pady=5)

suptitle_lable = tk.Label(root, text="Enter First and Last Name to Search", fg="white", bg="black",
                          font=('calibri', 12))
suptitle_lable.grid(row=10, column=1, padx=10, pady=5)

# Search field and contact details display
tk.Label(root, text="Search Contact", fg="white", bg="black", font=('calibri', 12)).grid(row=11, column=0, padx=10,
                                                                                         pady=5)
entry_search = tk.Entry(root, width=50)
entry_search.grid(row=11, column=1, padx=10, pady=5)

btn_search = tk.Button(root, text="Search", command=search_contact, bg="gray", fg="black", font=('calibri', 10))
btn_search.grid(row=11, column=2, padx=10, pady=5)

contact_details = tk.Text(root, height=9, width=60, state='disabled', bg="black", fg="white", font=('calibri', 12))
contact_details.grid(row=13, column=0, columnspan=3, padx=10, pady=5)

# Update button (initially disabled)
btn_update = tk.Button(root, text="Update", command=update_contact_window, state='disable', bg="gray", fg="black",
                       width=10)
btn_update.grid(row=14, column=1, columnspan=1, padx=15, pady=6)

# Ensure CSV file exists
if not os.path.exists(CONTACTS_FILE):
    with open(CONTACTS_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["First Name", "Last Name", "Country Name", "Email", "Phone", "Address"])


# Run the main application loop
root.mainloop()