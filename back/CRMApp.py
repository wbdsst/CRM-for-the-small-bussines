import tkinter as tk
from tkinter import ttk, messagebox
import csv


class CRMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CRM для малого бизнеса")
        self.root.geometry("1000x800")
        self.filename = "clients.csv"

        # Заголовок
        ttk.Label(root, text="CRM для малого бизнеса", font=("Arial", 20)).pack(pady=10)

        # Таблица клиентов
        self.table = ttk.Treeview(root, columns=("ID", "Name", "Phone", "Email", "Notes"), show="headings")
        self.table.heading("ID", text="ID")
        self.table.heading("Name", text="Имя")
        self.table.heading("Phone", text="Телефон")
        self.table.heading("Email", text="Email")
        self.table.heading("Notes", text="Заметки")
        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        # Кнопки
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Добавить клиента", command=self.add_client_window).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Удалить клиента", command=self.delete_client).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Обновить", command=self.load_clients).grid(row=0, column=2, padx=5)

        # Загрузка данных
        self.load_clients()

    def load_clients(self):
        """Загрузка данных из файла и отображение в таблице."""
        for row in self.table.get_children():
            self.table.delete(row)

        try:
            with open(self.filename, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                for client in reader:
                    self.table.insert("", "end", values=(client["ID"], client["Name"], client["Phone"], client["Email"], client["Notes"]))
        except FileNotFoundError:
            with open(self.filename, mode="w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["ID", "Name", "Phone", "Email", "Notes"])
                writer.writeheader()

    def add_client_window(self):
        """Открытие окна добавления нового клиента."""
        add_window = tk.Toplevel(self.root)
        add_window.title("Добавить клиента")
        add_window.geometry("400x400")

        ttk.Label(add_window, text="Имя:").pack(pady=5)
        name_entry = ttk.Entry(add_window)
        name_entry.pack(pady=5)

        ttk.Label(add_window, text="Телефон:").pack(pady=5)
        phone_entry = ttk.Entry(add_window)
        phone_entry.pack(pady=5)

        ttk.Label(add_window, text="Email:").pack(pady=5)
        email_entry = ttk.Entry(add_window)
        email_entry.pack(pady=5)

        ttk.Label(add_window, text="Заметки:").pack(pady=5)
        notes_entry = ttk.Entry(add_window)
        notes_entry.pack(pady=5)

        def save_client():
            name = name_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()
            notes = notes_entry.get()

            if not name or not phone or not email:
                messagebox.showerror("Ошибка", "Пожалуйста, заполните все обязательные поля.")
                return

            self.add_client(name, phone, email, notes)
            add_window.destroy()

        ttk.Button(add_window, text="Сохранить", command=save_client).pack(pady=20)

    def add_client(self, name, phone, email, notes=""):
        """Добавление клиента в базу данных."""
        try:
            with open(self.filename, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                clients = list(reader)
                client_id = str(len(clients) + 1)
        except FileNotFoundError:
            client_id = "1"

        with open(self.filename, mode="a", newline="") as file:
            fieldnames = ["ID", "Name", "Phone", "Email", "Notes"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if client_id == "1":
                writer.writeheader()
            writer.writerow({"ID": client_id, "Name": name, "Phone": phone, "Email": email, "Notes": notes})

        self.load_clients()
    def delete_client(self):
            """Удаление выбранного клиента."""
            selected_item = self.table.selection()
            if not selected_item:
                messagebox.showwarning("Ошибка", "Пожалуйста, выберите клиента для удаления.")
                return

            client_id = self.table.item(selected_item)["values"][0]
            try:
                with open(self.filename, mode="r", newline="") as file:
                    reader = csv.DictReader(file)
                    clients = [client for client in reader if client["ID"] != str(client_id)]
                with open(self.filename, mode="w", newline="") as file:
                    fieldnames = ["ID", "Name", "Phone", "Email", "Notes"]
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(clients)
            except FileNotFoundError:
                pass

            self.load_clients()


if __name__ == "__main__":
    root = tk.Tk()
    app = CRMApp(root)
    root.mainloop()
