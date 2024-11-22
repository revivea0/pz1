import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
from datetime import datetime

def init_db():
    with sqlite3.connect("tasks_db.db") as db:
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL,
                            role TEXT NOT NULL DEFAULT 'user')""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            description TEXT NOT NULL,
                            status TEXT NOT NULL DEFAULT 'pending',
                            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                            completed_at DATETIME,
                            created_by TEXT NOT NULL,
                            FOREIGN KEY (user_id) REFERENCES users(id))""")
        db.commit()

class TaskManagerApp:
    MAX_TASK_DESC_LENGTH = 200  

    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")

        
        init_db()

        
        self.login_frame = tk.Frame(self.root)
        self.register_frame = tk.Frame(self.root)
        self.task_frame = tk.Frame(self.root)
        self.admin_frame = tk.Frame(self.root)

        
        self.create_login_ui()

    def create_login_ui(self):
        tk.Label(self.login_frame, text="Имя пользователя").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.login_frame, text="Пароль").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show='*')
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.login_frame, text="Войти", command=self.login).grid(row=2, column=0, columnspan=2)
        tk.Button(self.login_frame, text="Зарегистрироваться", command=self.show_register_ui).grid(row=3, column=0, columnspan=2)

        self.login_frame.pack(pady=20)

    def show_register_ui(self):
        self.login_frame.pack_forget()
        self.register_frame.pack(pady=20)

        tk.Label(self.register_frame, text="Имя пользователя").grid(row=0, column=0)
        self.register_username_entry = tk.Entry(self.register_frame)
        self.register_username_entry.grid(row=0, column=1)

        tk.Label(self.register_frame, text="Пароль").grid(row=1, column=0)
        self.register_password_entry = tk.Entry(self.register_frame, show='*')
        self.register_password_entry.grid(row=1, column=1)

        tk.Label(self.register_frame, text="Роль (admin/user)").grid(row=2, column=0)
        self.role_entry = tk.Entry(self.register_frame)
        self.role_entry.grid(row=2, column=1)

        tk.Button(self.register_frame, text="Зарегистрироваться", command=self.register_user).grid(row=3, column=0, columnspan=2)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Ошибка", "Имя пользователя и пароль не могут быть пустыми.")
            return

        with sqlite3.connect("tasks_db.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()

            if user:
                messagebox.showinfo("Успех", f"Добро пожаловать, {user[1]}!")
                if user[3] == 'admin':
                    self.show_admin_ui(user)
                else:
                    self.show_user_ui(user)
            else:
                messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль.")

    def register_user(self):
        username = self.register_username_entry.get().strip()
        password = self.register_password_entry.get().strip()
        role = self.role_entry.get().strip().lower()

        if not username or not password:
            messagebox.showerror("Ошибка", "Имя пользователя и пароль не могут быть пустыми.")
            return
        if role not in ('admin', 'user'):
            messagebox.showerror("Ошибка", "Роль должна быть 'администратор' или 'пользователь'.")
            return

        try:
            with sqlite3.connect("tasks_db.db") as db:
                cursor = db.cursor()
                cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
                db.commit()
                messagebox.showinfo("Успех", "Регистрация успешна!")
            self.register_frame.pack_forget()
            self.login_frame.pack(pady=20)

        except sqlite3.IntegrityError:
            messagebox.showerror("Ошибка", "Имя пользователя уже занято.")

    def show_admin_ui(self, user):
        self.login_frame.pack_forget()
        self.register_frame.pack_forget()
        self.admin_frame.pack(pady=20)

        tk.Button(self.admin_frame, text="Добавить нового сотрудника", command=self.add_employee).grid(row=0, column=0)
        tk.Button(self.admin_frame, text="Выдать задачу", command=self.assign_task).grid(row=1, column=0)
        tk.Button(self.admin_frame, text="Изменить статус задачи", command=self.change_task_status).grid(row=2, column=0)
        tk.Button(self.admin_frame, text="Редактировать задачу", command=self.update_task).grid(row=3, column=0)
        tk.Button(self.admin_frame, text="Удалить задачу", command=self.delete_task).grid(row=4, column=0)
        tk.Button(self.admin_frame, text="Отчет о выполненных задачах", command=self.print_completed_tasks_report).grid(row=5, column=0)
        tk.Button(self.admin_frame, text="Отчет по задачам сотрудника", command=self.print_employee_tasks_report).grid(row=6, column=0)

        tk.Button(self.admin_frame, text="Вернуться", command=self.back_to_login).grid(row=7, column=0)

    def show_user_ui(self, user):
        self.login_frame.pack_forget()
        self.register_frame.pack_forget()
        self.task_frame.pack(pady=20)

        tk.Button(self.task_frame, text="Посмотреть свои задачи", command=lambda: self.view_tasks(user[0])).grid(row=0, column=0)
        tk.Button(self.task_frame, text="Изменить статус задачи", command=self.change_user_task_status).grid(row=1, column=0)
        tk.Button(self.task_frame, text="Вывести отчет о проделанной работе", command=lambda: self.print_work_report(user[0])).grid(row=2, column=0)
        tk.Button(self.task_frame, text="Вернуться", command=self.back_to_login).grid(row=3, column=0)

    def back_to_login(self):
        self.admin_frame.pack_forget()
        self.task_frame.pack_forget()
        self.login_frame.pack(pady=20)

    def add_employee(self):
        username = simpledialog.askstring("Добавить сотрудника", "Введите имя пользователя:")
        password = simpledialog.askstring("Добавить сотрудника", "Введите пароль:")
        role = simpledialog.askstring("Добавить сотрудника", "Введите роль (admin/user):").lower()

        if username and password and role in ('admin', 'user'):
            try:
                with sqlite3.connect("tasks_db.db") as db:
                    cursor = db.cursor()
                    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
                    db.commit()
                    messagebox.showinfo("Успех", "Сотрудник добавлен!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Ошибка", "Имя пользователя уже занято.")
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные данные.")

    def assign_task(self):
        username = simpledialog.askstring("Выдать задачу", "Введите имя пользователя сотрудника:")
        description = simpledialog.askstring("Выдать задачу", "Введите описание задачи:")

        if username and description:
            with sqlite3.connect("tasks_db.db") as db:
                cursor = db.cursor()
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                user = cursor.fetchone()

                if user:
                    cursor.execute("INSERT INTO tasks (user_id, description, created_by) VALUES (?, ?, ?)", (user[0], description, self.username_entry.get()))
                    db.commit()
                    messagebox.showinfo("Успех", f"Задача выдана сотруднику {username}!")
                else:
                    messagebox.showerror("Ошибка", "Сотрудник не найден.")
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные данные.")

    def change_task_status(self):
        task_id = simpledialog.askinteger("Изменение статуса", "Введите ID задачи:")
        new_status = simpledialog.askstring("Изменение статуса", "Введите новый статус (pending/completed/in_progress):")

        if new_status in ['pending', 'completed', 'in_progress']:
            with sqlite3.connect("tasks_db.db") as db:
                cursor = db.cursor()
                cursor.execute("UPDATE tasks SET status = ?, completed_at = ? WHERE id = ?",
                               (new_status, datetime.now() if new_status == 'completed' else None, task_id))
                db.commit()
                messagebox.showinfo("Успех", "Статус задачи изменен!")
        else:
            messagebox.showerror("Ошибка", "Некорректный статус задачи.")

    def change_user_task_status(self):

        task_id = simpledialog.askinteger("Изменение статуса", "Введите ID задачи:")
        new_status = simpledialog.askstring("Изменение статуса", "Введите новый статус (pending/completed/in_progress):")

        if new_status in ['pending', 'completed', 'in_progress']:
            with sqlite3.connect("tasks_db.db") as db:
                cursor = db.cursor()
                cursor.execute("UPDATE tasks SET status = ?, completed_at = ? WHERE id = ?",
                               (new_status, datetime.now() if new_status == 'completed' else None, task_id))
                db.commit()
                messagebox.showinfo("Успех", "Статус задачи изменен!")
        else:
            messagebox.showerror("Ошибка", "Некорректный статус задачи.")

    def update_task(self):
        task_id = simpledialog.askinteger("Редактирование задачи", "Введите ID задачи:")
        new_description = simpledialog.askstring("Редактирование задачи", "Введите новое описание задачи:")

        if new_description and len(new_description) <= self.MAX_TASK_DESC_LENGTH:
            with sqlite3.connect("tasks_db.db") as db:
                cursor = db.cursor()
                cursor.execute("UPDATE tasks SET description = ? WHERE id = ?", (new_description, task_id))
                db.commit()
                messagebox.showinfo("Успех", "Задача успешно обновлена!")
        else:
            messagebox.showerror("Ошибка", "Описание задачи не может быть пустым или превышать 200 символов.")

    def delete_task(self):
        task_id = simpledialog.askinteger("Удаление задачи", "Введите ID задачи:")
        with sqlite3.connect("tasks_db.db") as db:
            cursor = db.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            db.commit()
            messagebox.showinfo("Успех", "Задача успешно удалена!")

    def print_completed_tasks_report(self):
        start_date = simpledialog.askstring("Отчет", "Введите дату начала (гггг-мм-дд):")
        end_date = simpledialog.askstring("Отчет", "Введите дату окончания (гггг-мм-дд):")

        report = ""
        with sqlite3.connect("tasks_db.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM tasks WHERE status = 'completed' AND completed_at BETWEEN ? AND ?", (start_date, end_date))
            tasks = cursor.fetchall()
            for task in tasks:
                report += f"Задача ID: {task[0]}, Описание: {task[2]}, Статус: {task[3]}, Создана кем: {task[6]}, Дата создания: {task[4]}, Дата выполнения: {task[5]}\n"

        if report:
            with open("completed_tasks_report.txt", "w") as file:
                file.write(report)
            messagebox.showinfo("Отчет", f"Отчет сохранен в файл 'completed_tasks_report.txt'.\n{report}")
        else:
            messagebox.showinfo("Отчет", "Нет выполненных задач за указанный период.")

    def print_employee_tasks_report(self):
        username = simpledialog.askstring("Отчет", "Введите имя пользователя сотрудника:")
        report = ""

        with sqlite3.connect("tasks_db.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

            if user:
                cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (user[0],))
                tasks = cursor.fetchall()
                for task in tasks:
                    report += f"Задача ID: {task[0]}, Описание: {task[2]}, Статус: {task[3]}, Дата создания: {task[4]}, Дата выполнения: {task[5]}, Создана кем: {task[6]}\n"

            if report:

                with open(f"employee_tasks_report_{username}.txt", "w") as file:
                    file.write(report)
                messagebox.showinfo("Отчет", f"Отчет сохранен в файл 'employee_tasks_report_{username}.txt'.\n{report}")
            else:
                messagebox.showinfo("Отчет", "Нет задач для данного сотрудника.")

    def view_tasks(self, user_id):
        task_window = tk.Toplevel(self.root)
        task_window.title("Список задач")

        self.task_listbox = tk.Listbox(task_window, width=100)
        self.task_listbox.pack(pady=20)

        with sqlite3.connect("tasks_db.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
            tasks = cursor.fetchall()
            for task in tasks:
                self.task_listbox.insert(tk.END, f"ID: {task[0]}, Описание: {task[2]}, Статус: {task[3]}, Дата создания: {task[4]}, Дата выполнения: {task[5]}, Создана кем: {task[6]}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
