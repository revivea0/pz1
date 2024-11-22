import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
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
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        
        self.style = {
            'bg_color': '#f0f0f0',
            'button_bg': '#4a90e2',
            'button_fg': 'white',
            'button_active_bg': '#357abd',
            'label_fg': '#333333',
            'entry_bg': 'white',
            'font_family': ('Helvetica', 10),
            'header_font': ('Helvetica', 12, 'bold')
        }
        
        init_db()
        
        self.login_frame = tk.Frame(self.root, bg=self.style['bg_color'])
        self.register_frame = tk.Frame(self.root, bg=self.style['bg_color'])
        self.task_frame = tk.Frame(self.root, bg=self.style['bg_color'])
        self.admin_frame = tk.Frame(self.root, bg=self.style['bg_color'])
        
        self.create_login_ui()

    def create_login_ui(self):
        
        header = tk.Label(self.login_frame, text="Система управления задачами", 
                         font=self.style['header_font'], bg=self.style['bg_color'],
                         fg=self.style['label_fg'])
        header.grid(row=0, column=0, columnspan=2, pady=20)

        
        tk.Label(self.login_frame, text="Имя пользователя", 
                font=self.style['font_family'], bg=self.style['bg_color'],
                fg=self.style['label_fg']).grid(row=1, column=0, pady=5)
        self.username_entry = tk.Entry(self.login_frame, font=self.style['font_family'],
                                     bg=self.style['entry_bg'])
        self.username_entry.grid(row=1, column=1, pady=5)

        tk.Label(self.login_frame, text="Пароль", 
                font=self.style['font_family'], bg=self.style['bg_color'],
                fg=self.style['label_fg']).grid(row=2, column=0, pady=5)
        self.password_entry = tk.Entry(self.login_frame, show='*',
                                     font=self.style['font_family'],
                                     bg=self.style['entry_bg'])
        self.password_entry.grid(row=2, column=1, pady=5)

        
        login_btn = tk.Button(self.login_frame, text="Войти", 
                            command=self.login,
                            bg=self.style['button_bg'],
                            fg=self.style['button_fg'],
                            font=self.style['font_family'],
                            width=20,
                            relief=tk.FLAT)
        login_btn.grid(row=3, column=0, columnspan=2, pady=10)

        register_btn = tk.Button(self.login_frame, text="Зарегистрироваться",
                               command=self.show_register_ui,
                               bg=self.style['button_bg'],
                               fg=self.style['button_fg'],
                               font=self.style['font_family'],
                               width=20,
                               relief=tk.FLAT)
        register_btn.grid(row=4, column=0, columnspan=2, pady=5)

        self.login_frame.pack(pady=50)

    def show_register_ui(self):
        self.login_frame.pack_forget()
        self.register_frame = tk.Frame(self.root, bg=self.style['bg_color'])
        self.register_frame.pack(pady=50, padx=50, fill='both', expand=True)

        
        header = tk.Label(self.register_frame, 
                         text="Регистрация нового пользователя",
                         font=self.style['header_font'],
                         bg=self.style['bg_color'],
                         fg=self.style['label_fg'])
        header.pack(pady=(0, 20))

        
        fields_frame = tk.Frame(self.register_frame, bg=self.style['bg_color'])
        fields_frame.pack(fill='both', padx=20)

        
        tk.Label(fields_frame, text="Имя пользователя",
                font=self.style['font_family'],
                bg=self.style['bg_color'],
                fg=self.style['label_fg']).pack(anchor='w', pady=(5,0))
        self.register_username_entry = tk.Entry(fields_frame,
                                              font=self.style['font_family'],
                                              bg=self.style['entry_bg'],
                                              width=30)
        self.register_username_entry.pack(fill='x', pady=(0,10))

        
        tk.Label(fields_frame, text="Пароль",
                font=self.style['font_family'],
                bg=self.style['bg_color'],
                fg=self.style['label_fg']).pack(anchor='w', pady=(5,0))
        self.register_password_entry = tk.Entry(fields_frame,
                                              show='*',
                                              font=self.style['font_family'],
                                              bg=self.style['entry_bg'],
                                              width=30)
        self.register_password_entry.pack(fill='x', pady=(0,10))

        
        tk.Label(fields_frame, text="Роль",
                font=self.style['font_family'],
                bg=self.style['bg_color'],
                fg=self.style['label_fg']).pack(anchor='w', pady=(5,0))
        self.role_var = tk.StringVar(value='user')
        role_frame = tk.Frame(fields_frame, bg=self.style['bg_color'])
        role_frame.pack(fill='x', pady=(0,10))
        
        tk.Radiobutton(role_frame, text="Пользователь",
                      variable=self.role_var,
                      value='user',
                      font=self.style['font_family'],
                      bg=self.style['bg_color']).pack(side='left', padx=10)
        tk.Radiobutton(role_frame, text="Администратор",
                      variable=self.role_var,
                      value='admin',
                      font=self.style['font_family'],
                      bg=self.style['bg_color']).pack(side='left')

        
        button_frame = tk.Frame(self.register_frame, bg=self.style['bg_color'])
        button_frame.pack(pady=20)

        tk.Button(button_frame,
                 text="Зарегистрироваться",
                 command=self.register_user,
                 bg=self.style['button_bg'],
                 fg=self.style['button_fg'],
                 font=self.style['font_family'],
                 width=20,
                 relief=tk.FLAT).pack(pady=5)

        tk.Button(button_frame,
                 text="Назад",
                 command=self.back_to_login,
                 bg=self.style['button_bg'],
                 fg=self.style['button_fg'],
                 font=self.style['font_family'],
                 width=20,
                 relief=tk.FLAT).pack(pady=5)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
            return
        
        try:
            with sqlite3.connect("tasks_db.db") as db:
                cursor = db.cursor()
                cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                             (username, password))
                user = cursor.fetchone()
                
                if user:
                    self.current_user = user
                    self.username_entry.delete(0, tk.END)
                    self.password_entry.delete(0, tk.END)
                    if user[3] == 'admin':
                        self.show_admin_ui(user)
                    else:
                        self.show_user_ui(user)
                else:
                    messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Ошибка при входе: {str(e)}")
            print(f"Database error during login: {str(e)}")

    def register_user(self):
        username = self.register_username_entry.get().strip()
        password = self.register_password_entry.get().strip()
        role = self.role_var.get().strip().lower()

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
        self.task_frame.pack_forget()
        self.admin_frame.pack(pady=20, padx=40)

       
        for widget in self.admin_frame.winfo_children():
            widget.destroy()

        
        style = ttk.Style()
        style.configure('Admin.TButton',
                       padding=(20, 10),
                       font=('Helvetica', 10),
                       background='#4a90e2',
                       foreground='white',
                       width=30)
        style.map('Admin.TButton',
                 background=[('active', '#357abd')],
                 foreground=[('active', 'white')])

        
        header = ttk.Label(self.admin_frame, 
                          text=f"Панель администратора - {user[1]}", 
                          font=('Helvetica', 14, 'bold'))
        header.grid(row=0, column=0, pady=(0, 20), columnspan=2)

        
        buttons = [
            ("Добавить нового сотрудника", self.add_employee),
            ("Выдать задачу", self.assign_task),
            ("Изменить статус задачи", self.change_task_status),
            ("Редактировать задачу", self.update_task),
            ("Удалить задачу", self.delete_task),
            ("Отчет о выполненных задачах", self.print_completed_tasks_report),
            ("Отчет по задачам сотрудника", self.print_employee_tasks_report),
            ("Вернуться", self.back_to_login)
        ]

        
        for i, (text, command) in enumerate(buttons):
            row = (i // 2) + 1 
            col = i % 2
            ttk.Button(self.admin_frame, 
                      text=text,
                      command=command,
                      style='Admin.TButton').grid(row=row, 
                                                column=col,
                                                padx=10,
                                                pady=5,
                                                sticky='nsew')

        
        self.admin_frame.grid_columnconfigure(0, weight=1)
        self.admin_frame.grid_columnconfigure(1, weight=1)

    def show_user_ui(self, user):
        self.login_frame.pack_forget()
        self.register_frame.pack_forget()
        self.task_frame.pack(pady=20, padx=40)

        
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        
        style = ttk.Style()
        style.configure('UserButton.TButton',
                      font=('Helvetica', 10),
                      padding=(20, 10))

        
        header = ttk.Label(self.task_frame, 
                          text=f"Личный кабинет - {user[1]}", 
                          font=('Helvetica', 14, 'bold'))
        header.grid(row=0, column=0, pady=(0, 20))

        
        button_texts = [
            ("Посмотреть свои задачи", lambda: self.view_tasks(user[0])),
            ("Изменить статус задачи", self.change_user_task_status),
            ("Вывести отчет о проделанной работе", lambda: self.print_work_report(user[0])),
            ("Вернуться", self.back_to_login)
        ]

        for i, (text, command) in enumerate(button_texts):
            btn = ttk.Button(self.task_frame,
                           text=text,
                           command=command,
                           style='UserButton.TButton')
            btn.grid(row=i+1, column=0, padx=20, pady=5, sticky='ew')

        
        self.task_frame.grid_columnconfigure(0, weight=1)

        
        self.view_tasks(user[0])

    def back_to_login(self):
        
        self.admin_frame.pack_forget()
        self.task_frame.pack_forget()
        self.register_frame.pack_forget()
        self.login_frame.pack_forget()
        
        
        for widget in self.login_frame.winfo_children():
            widget.destroy()
        
        
        self.create_login_ui()

    def create_form_window(self, title, fields, callback):
       
        form_window = tk.Toplevel(self.root)
        form_window.title(title)
        form_window.geometry("400x400")
        form_window.configure(bg=self.style['bg_color'])
        
        
        form_window.transient(self.root)
        form_window.grab_set()
        
        
        header = ttk.Label(form_window, 
                          text=title,
                          font=('Helvetica', 14, 'bold'))
        header.pack(pady=(20, 20))
        
        
        entries = {}
        for field_name, field_type in fields.items():
            frame = tk.Frame(form_window, bg=self.style['bg_color'])
            frame.pack(fill='x', padx=20, pady=5)
            
            label = ttk.Label(frame, 
                            text=field_name,
                            font=self.style['font_family'])
            label.pack(anchor='w')
            
            if field_type == 'text':
                entry = ttk.Entry(frame, width=40)
            elif field_type == 'password':
                entry = ttk.Entry(frame, width=40, show='*')
            entries[field_name] = entry
            entry.pack(fill='x', pady=(2, 5))
        
        
        button_frame = tk.Frame(form_window, bg=self.style['bg_color'])
        button_frame.pack(pady=20)
        
        def submit():
            values = {name: entry.get().strip() for name, entry in entries.items()}
            form_window.destroy()
            callback(values)
            
        def cancel():
            form_window.destroy()
        
        
        ttk.Button(button_frame,
                  text="Подтвердить",
                  command=submit,
                  style='UserButton.TButton').pack(side='left', padx=5)
                  
        ttk.Button(button_frame,
                  text="Отмена",
                  command=cancel,
                  style='UserButton.TButton').pack(side='left', padx=5)
        
        
        form_window.update_idletasks()
        width = form_window.winfo_width()
        height = form_window.winfo_height()
        x = (form_window.winfo_screenwidth() // 2) - (width // 2)
        y = (form_window.winfo_screenheight() // 2) - (height // 2)
        form_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def add_employee(self):
        def handle_submit(values):
            username = values['Имя пользователя']
            password = values['Пароль']
            role = values['Роль'].lower()
            
            if username and password and role in ('admin', 'user'):
                try:
                    with sqlite3.connect("tasks_db.db") as db:
                        cursor = db.cursor()
                        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                                     (username, password, role))
                        db.commit()
                        messagebox.showinfo("Успех", "Сотрудник добавлен!")
                except sqlite3.IntegrityError:
                    messagebox.showerror("Ошибка", "Имя пользователя уже занято.")
            else:
                messagebox.showerror("Ошибка", "Пожалуйста, введите корректные данные.")
            self.show_admin_ui(self.current_user)
            
        fields = {
            'Имя пользователя': 'text',
            'Пароль': 'password',
            'Роль': 'text'
        }
        self.create_form_window("Добавить сотрудника", fields, handle_submit)

    def assign_task(self):
        def handle_submit(values):
            username = values['Имя пользователя'].strip()
            description = values['Описание задачи'].strip()
            
            if not username or not description:
                messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
                return
            
            if len(description) > self.MAX_TASK_DESC_LENGTH:
                messagebox.showerror("Ошибка", f"Описание задачи не может быть длиннее {self.MAX_TASK_DESC_LENGTH} символов.")
                return
            
            try:
                with sqlite3.connect("tasks_db.db") as db:
                    cursor = db.cursor()
                    
                    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                    target_user = cursor.fetchone()
                    
                    if target_user:
                        
                        cursor.execute("""
                            INSERT INTO tasks (user_id, description, status, created_at, created_by) 
                            VALUES (?, ?, 'в работе', datetime('now', 'localtime'), ?)
                        """, (target_user[0], description, self.current_user[1]))
                        db.commit()
                        messagebox.showinfo("Успех", "Задача добавлена!")
                        
                        
                        if hasattr(self, 'task_tree') and self.task_tree.winfo_exists():
                            self.refresh_tasks(target_user[0])
                    else:
                        messagebox.showerror("Ошибка", "Пользователь не найден.")
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка базы данных", f"Не удалось добавить задачу: {str(e)}")
                print(f"Database error: {str(e)}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
                print(f"General error: {str(e)}")
        
        fields = {
            'Имя пользователя': 'text',
            'Описание задачи': 'text'
        }
        self.create_form_window("Выдать задачу", fields, handle_submit)

    def change_task_status(self):
        def handle_submit(values):
            task_id = values['ID задачи'].strip()
            new_status = values['Новый статус'].strip().lower()
            
            try:
                task_id = int(task_id)
                if new_status in ['в работе', 'выполнено', 'ожидает']:
                    with sqlite3.connect("tasks_db.db") as db:
                        cursor = db.cursor()
                        cursor.execute("SELECT user_id, status FROM tasks WHERE id = ?", (task_id,))
                        task = cursor.fetchone()
                        if task:
                            
                            completed_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S') if new_status == 'выполнено' else None
                            cursor.execute("""
                                UPDATE tasks 
                                SET status = ?, 
                                    completed_at = ?
                                WHERE id = ?
                            """, (new_status, completed_at, task_id))
                            db.commit()
                            messagebox.showinfo("Успех", "Статус задачи обновлен!")
                            
                            if hasattr(self, 'task_tree') and self.task_tree.winfo_exists():
                                self.refresh_tasks(task[0])  
                        else:
                            messagebox.showerror("Ошибка", "Задача не найдена.")
                else:
                    messagebox.showerror("Ошибка", "Некорректный статус. Используйте: в работе, выполнено, ожидает")
            except ValueError:
                messagebox.showerror("Ошибка", "ID задачи должен быть числом.")
            except sqlite3.Error as e:
                messagebox.showerror("Ошибка базы данных", f"Ошибка при обновлении статуса: {str(e)}")
                print(f"Database error during status update: {str(e)}")
        
        fields = {
            'ID задачи': 'text',
            'Новый статус': 'text'
        }
        self.create_form_window("Изменить статус задачи", fields, handle_submit)

    def change_user_task_status(self):
        def handle_submit(values):
            task_id = values['ID задачи']
            new_status = values['Новый статус']
            
            try:
                task_id = int(task_id)
                if new_status in ['в работе', 'выполнено', 'ожидает']:
                    with sqlite3.connect("tasks_db.db") as db:
                        cursor = db.cursor()
                        cursor.execute("SELECT status FROM tasks WHERE id = ? AND user_id = ?", 
                                     (task_id, self.current_user[0]))
                        task = cursor.fetchone()
                        if task:
                            
                            completed_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S') if new_status == 'выполнено' else None
                            cursor.execute("""
                                UPDATE tasks 
                                SET status = ?, 
                                    completed_at = ?
                                WHERE id = ? AND user_id = ?
                            """, (new_status, completed_at, task_id, self.current_user[0]))
                            db.commit()
                            messagebox.showinfo("Успех", "Статус задачи обновлен!")
                            
                            self.refresh_tasks(self.current_user[0])
                        else:
                            messagebox.showerror("Ошибка", "Задача не найдена или не принадлежит вам.")
                else:
                    messagebox.showerror("Ошибка", "Некорректный статус. Используйте: в работе, выполнено, ожидает")
            except ValueError:
                messagebox.showerror("Ошибка", "ID задачи должен быть числом.")
            self.show_user_ui(self.current_user)
            
        fields = {
            'ID задачи': 'text',
            'Новый статус': 'text'
        }
        self.create_form_window("Изменить статус задачи", fields, handle_submit)

    def update_task(self):
        def handle_submit(values):
            task_id = values['ID задачи']
            new_description = values['Новое описание']
            
            try:
                task_id = int(task_id)
                if new_description:
                    with sqlite3.connect("tasks_db.db") as db:
                        cursor = db.cursor()
                        cursor.execute("UPDATE tasks SET description = ? WHERE id = ?", 
                                     (new_description, task_id))
                        if cursor.rowcount > 0:
                            db.commit()
                            messagebox.showinfo("Успех", "Задача обновлена!")
                        else:
                            messagebox.showerror("Ошибка", "Задача не найдена.")
                else:
                    messagebox.showerror("Ошибка", "Описание не может быть пустым.")
            except ValueError:
                messagebox.showerror("Ошибка", "ID задачи должен быть числом.")
            self.show_admin_ui(self.current_user)
            
        fields = {
            'ID задачи': 'text',
            'Новое описание': 'text'
        }
        self.create_form_window("Обновить задачу", fields, handle_submit)

    def delete_task(self):
        def handle_submit(values):
            task_id = values['ID задачи']
            
            try:
                task_id = int(task_id)
                with sqlite3.connect("tasks_db.db") as db:
                    cursor = db.cursor()
                    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
                    if cursor.rowcount > 0:
                        db.commit()
                        messagebox.showinfo("Успех", "Задача удалена!")
                    else:
                        messagebox.showerror("Ошибка", "Задача не найдена.")
            except ValueError:
                messagebox.showerror("Ошибка", "ID задачи должен быть числом.")
            self.show_admin_ui(self.current_user)
            
        fields = {
            'ID задачи': 'text'
        }
        self.create_form_window("Удалить задачу", fields, handle_submit)

    def print_completed_tasks_report(self):
        fields = {
            'Дата начала': 'text',
            'Дата окончания': 'text'
        }
        self.create_form_window("Отчет о выполненных задачах", fields, self.handle_completed_tasks_report)

    def handle_completed_tasks_report(self, values):
        start_date = values['Дата начала']
        end_date = values['Дата окончания']
        
        try:
            
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
                datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат даты. Используйте формат ГГГГ-ММ-ДД")
                return

            with sqlite3.connect("tasks_db.db") as db:
                cursor = db.cursor()
                cursor.execute("""
                    SELECT t.id, t.description, t.status, t.created_at, t.completed_at, u.username
                    FROM tasks t
                    LEFT JOIN users u ON t.user_id = u.id
                    WHERE t.status = 'выполнено'
                    AND date(t.completed_at) BETWEEN date(?) AND date(?)
                    ORDER BY t.completed_at
                """, (start_date, end_date))
                
                tasks = cursor.fetchall()
                if tasks:
                    report = f"Отчет о выполненных задачах с {start_date} по {end_date}\n"
                    report += f"Дата создания отчета: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    report += "=" * 80 + "\n\n"
                    
                    for task in tasks:
                        report += f"ID задачи: {task[0]}\n"
                        report += f"Исполнитель: {task[5]}\n"
                        report += f"Описание: {task[1]}\n"
                        report += f"Дата создания: {task[3]}\n"
                        report += f"Дата выполнения: {task[4]}\n"
                        report += "-" * 40 + "\n"
                    
                    
                    filename = f"completed_tasks_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(report)
                    
                    
                    report_window = tk.Toplevel(self.root)
                    report_window.title("Отчет о выполненных задачах")
                    report_window.geometry("800x600")
                    report_window.configure(bg=self.style['bg_color'])
                    
                    
                    text_frame = tk.Frame(report_window, bg=self.style['bg_color'])
                    text_frame.pack(fill='both', expand=True, padx=20, pady=20)
                    
                    text_widget = tk.Text(text_frame, wrap='word', font=('Courier', 10))
                    scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
                    text_widget.configure(yscrollcommand=scrollbar.set)
                    
                    text_widget.pack(side='left', fill='both', expand=True)
                    scrollbar.pack(side='right', fill='y')
                    
                    text_widget.insert('1.0', report)
                    text_widget.config(state='disabled')
                    
                    messagebox.showinfo("Успех", f"Отчет сохранен в файл: {filename}")
                else:
                    messagebox.showinfo("Информация", "Нет выполненных задач за указанный период")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при создании отчета: {str(e)}")

    def print_employee_tasks_report(self):
        fields = {
            'Имя сотрудника': 'text'
        }
        self.create_form_window("Отчет по задачам сотрудника", fields, self.handle_employee_tasks_report)

    def handle_employee_tasks_report(self, values):
        username = values['Имя сотрудника']
        
        try:
            with sqlite3.connect("tasks_db.db") as db:
                cursor = db.cursor()
                cursor.execute("""
                    SELECT t.id, t.description, t.status, t.created_at, t.completed_at, u.username
                    FROM tasks t
                    INNER JOIN users u ON t.user_id = u.id
                    WHERE u.username = ?
                    ORDER BY t.created_at
                """, (username,))
                
                tasks = cursor.fetchall()
                if tasks:
                    report = f"Отчет по задачам сотрудника: {username}\n"
                    report += f"Дата создания отчета: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    report += "=" * 80 + "\n\n"
                    
                    for task in tasks:
                        report += f"ID задачи: {task[0]}\n"
                        report += f"Описание: {task[1]}\n"
                        report += f"Статус: {task[2]}\n"
                        report += f"Дата создания: {task[3]}\n"
                        report += f"Дата выполнения: {task[4] or 'Не выполнено'}\n"
                        report += f"Создана: {task[5]}\n"
                        report += "-" * 40 + "\n"
                    
                    
                    filename = f"employee_tasks_report_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(report)
                    
                    
                    report_window = tk.Toplevel(self.root)
                    report_window.title(f"Отчет по задачам сотрудника: {username}")
                    report_window.geometry("800x600")
                    report_window.configure(bg=self.style['bg_color'])
                    
                    # Add text widget with scrollbar
                    text_frame = tk.Frame(report_window, bg=self.style['bg_color'])
                    text_frame.pack(fill='both', expand=True, padx=20, pady=20)
                    
                    text_widget = tk.Text(text_frame, wrap='word', font=('Courier', 10))
                    scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
                    text_widget.configure(yscrollcommand=scrollbar.set)
                    
                    text_widget.pack(side='left', fill='both', expand=True)
                    scrollbar.pack(side='right', fill='y')
                    
                    text_widget.insert('1.0', report)
                    text_widget.config(state='disabled')
                    
                    messagebox.showinfo("Успех", f"Отчет сохранен в файл: {filename}")
                else:
                    messagebox.showinfo("Информация", f"Задачи для сотрудника {username} не найдены")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при создании отчета: {str(e)}")

    def print_work_report(self, user_id):
        fields = {
            'Дата начала': 'text',
            'Дата окончания': 'text'
        }
        self.create_form_window("Отчет о проделанной работе", fields, lambda values: self.handle_work_report(values, user_id))

    def handle_work_report(self, values, user_id):
        start_date = values['Дата начала']
        end_date = values['Дата окончания']
        
        try:
            with sqlite3.connect("tasks_db.db") as db:
                cursor = db.cursor()
                cursor.execute("""
                    SELECT t.id, t.description, t.status, t.created_at, t.completed_at, u.username
                    FROM tasks t
                    LEFT JOIN users u ON t.created_by = u.username
                    WHERE t.user_id = ?
                    AND date(t.created_at) BETWEEN date(?) AND date(?)
                    ORDER BY t.created_at
                """, (user_id, start_date, end_date))
                
                tasks = cursor.fetchall()
                if tasks:
                    report = f"Отчет о проделанной работе с {start_date} по {end_date}\n\n"
                    report += "=" * 80 + "\n\n"
                    
                    for task in tasks:
                        report += f"ID задачи: {task[0]}\n"
                        report += f"Описание: {task[1]}\n"
                        report += f"Статус: {task[2]}\n"
                        report += f"Дата создания: {task[3]}\n"
                        report += f"Дата выполнения: {task[4] or 'Не выполнено'}\n"
                        report += f"Создана: {task[5]}\n"
                        report += "-" * 40 + "\n"
                    
                    
                    filename = f"work_report_{start_date}_{end_date}.txt"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(report)
                    
                    
                    report_window = tk.Toplevel(self.root)
                    report_window.title("Отчет о проделанной работе")
                    report_window.geometry("800x600")
                    report_window.configure(bg=self.style['bg_color'])
                    
                    
                    text_frame = tk.Frame(report_window, bg=self.style['bg_color'])
                    text_frame.pack(fill='both', expand=True, padx=20, pady=20)
                    
                    text_widget = tk.Text(text_frame, wrap='word', font=('Courier', 10))
                    scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
                    text_widget.configure(yscrollcommand=scrollbar.set)
                    
                    text_widget.pack(side='left', fill='both', expand=True)
                    scrollbar.pack(side='right', fill='y')
                    
                    text_widget.insert('1.0', report)
                    text_widget.config(state='disabled')
                    
                    messagebox.showinfo("Успех", f"Отчет сохранен в файл: {filename}")
                else:
                    messagebox.showinfo("Информация", "Нет задач за указанный период")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при создании отчета: {str(e)}")

    def view_tasks(self, user_id):
        task_window = tk.Toplevel(self.root)
        task_window.title("Список задач")
        task_window.geometry("800x600")
        task_window.configure(bg=self.style['bg_color'])

       
        header = tk.Label(task_window,
                         text="Список задач",
                         font=self.style['header_font'],
                         bg=self.style['bg_color'],
                         fg=self.style['label_fg'])
        header.pack(pady=20)

        
        list_frame = tk.Frame(task_window, bg=self.style['bg_color'])
        list_frame.pack(fill='both', expand=True, padx=20)

        
        columns = ('ID', 'Описание', 'Статус', 'Дата создания', 'Дата выполнения', 'Создана кем')
        self.task_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)

        
        for col in columns:
            self.task_tree.heading(col, text=col)
            self.task_tree.column(col, width=100)
        self.task_tree.column('Описание', width=200)

        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=scrollbar.set)

       
        self.task_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        
        with sqlite3.connect("tasks_db.db") as db:
            cursor = db.cursor()
            cursor.execute("""
                SELECT t.id, t.description, t.status, t.created_at, t.completed_at, u.username
                FROM tasks t
                LEFT JOIN users u ON t.created_by = u.username
                WHERE t.user_id = ?
                ORDER BY t.created_at DESC
            """, (user_id,))
            tasks = cursor.fetchall()
            
            for task in tasks:
                self.task_tree.insert('', 'end', values=task)

        
        button_frame = tk.Frame(task_window, bg=self.style['bg_color'])
        button_frame.pack(pady=20)

        if hasattr(self, 'current_user') and self.current_user[3] == 'admin':
            buttons = [
                ("Изменить статус", self.change_task_status),
                ("Обновить список", lambda: self.refresh_tasks(user_id)),
                ("Закрыть", task_window.destroy)
            ]
        else:
            buttons = [
                ("Изменить статус", self.change_user_task_status),
                ("Обновить список", lambda: self.refresh_tasks(user_id)),
                ("Закрыть", task_window.destroy)
            ]

        for text, command in buttons:
            tk.Button(button_frame,
                     text=text,
                     command=command,
                     bg=self.style['button_bg'],
                     fg=self.style['button_fg'],
                     font=self.style['font_family'],
                     width=15,
                     relief=tk.FLAT).pack(side='left', padx=5)

    def refresh_tasks(self, user_id):
        try:
            if not hasattr(self, 'task_tree') or not self.task_tree.winfo_exists():
                return
            
            
            for item in self.task_tree.get_children():
                self.task_tree.delete(item)
                
        
            with sqlite3.connect("tasks_db.db") as db:
                cursor = db.cursor()
                cursor.execute("""
                    SELECT t.id, t.description, t.status, t.created_at, t.completed_at, t.created_by, u.username
                    FROM tasks t
                    JOIN users u ON t.user_id = u.id
                    WHERE t.user_id = ?
                    ORDER BY 
                        CASE 
                            WHEN t.status = 'в работе' THEN 1
                            WHEN t.status = 'ожидает' THEN 2
                            WHEN t.status = 'выполнено' THEN 3
                        END,
                        t.created_at DESC
                """, (user_id,))
                tasks = cursor.fetchall()
                
                for task in tasks:
                    task_id, desc, status, created, completed, created_by, username = task
                    created = datetime.strptime(created, '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M')
                    completed = datetime.strptime(completed, '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M') if completed else ''
                
                    self.task_tree.insert('', 'end', values=(task_id, desc, status, created, completed, created_by, username))
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Ошибка при обновлении списка задач: {str(e)}")
            print(f"Database error during task refresh: {str(e)}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при обновлении списка задач: {str(e)}")
            print(f"General error during task refresh: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
