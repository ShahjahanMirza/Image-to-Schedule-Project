import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from datetime import datetime
from image_processing import transform_image  # Assuming you have these modules
from image_read import chat_with_image_gemini  # Assuming you have these modules
from db import update_db  # Assuming you have these modules
import pandas as pd

class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Todo App")
        self.geometry("600x800")

        self.image_path = None

        # Image upload button
        self.upload_button = ttk.Button(self, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=10)

        # Image display
        self.image_label = tk.Label(self)
        self.image_label.pack()

        # Todos section
        self.todo_frame = ttk.Frame(self)
        self.todo_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.todo_canvas = tk.Canvas(self.todo_frame)
        self.todo_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.todo_scrollbar = ttk.Scrollbar(self.todo_frame, orient="vertical", command=self.todo_canvas.yview)
        self.todo_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.todo_container = ttk.Frame(self.todo_canvas)
        self.todo_container.bind(
            "<Configure>",
            lambda e: self.todo_canvas.configure(
                scrollregion=self.todo_canvas.bbox("all")
            )
        )

        self.todo_canvas.create_window((0, 0), window=self.todo_container, anchor="nw")
        self.todo_canvas.configure(yscrollcommand=self.todo_scrollbar.set)

        # Add Todo Entry
        self.todo_entry = ttk.Entry(self)
        self.todo_entry.pack(pady=5)
        self.add_todo_button = ttk.Button(self, text="Add Todo", command=self.add_todo)
        self.add_todo_button.pack()

        self.todos = []
        self.todo_dict = {}  # Dictionary to keep track of todos and their frames

    def upload_image(self):
        self.image_path = filedialog.askopenfilename()
        transform_image(self.image_path)
        if self.image_path:
            self.display_image()

    def display_image(self):
        img = Image.open('output_image.jpg')
        img = img.resize((400, 400), Image.BICUBIC)
        img = ImageTk.PhotoImage(img)
        self.image_label.config(image=img)
        self.image_label.image = img
        self.todos_from_image()

    def clear_todos(self):
        for todo in self.todos:
            todo.destroy()
        self.todos.clear()
        self.todo_dict.clear()

    def todos_from_image(self):
        self.clear_todos()
        events = chat_with_image_gemini('output_image.jpg')
        update_db(events=events)

        df = pd.read_csv('events.csv', index_col='Title')
        for index, row in df.iterrows():
            title = index
            date_str = row['Formatted_Date']
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            curr_date = datetime.now().date()
            remaining_time = (date - curr_date).days

            if remaining_time < 0:
                todo_with_date = f"{title} on {date} - Remaining: Completed"
            else:
                todo_with_date = f"{title} on {date} - Remaining Time: {remaining_time} days"

            self.add_todo_item(todo_with_date, title, date_str)

    def add_todo_item(self, todo_text, title, date_str):
        todo_frame = ttk.Frame(self.todo_container)
        todo_frame.pack(fill=tk.X, pady=2)

        todo_label = tk.Label(todo_frame, text=todo_text, wraplength=500)
        todo_label.pack(side=tk.LEFT, padx=5)

        edit_button = ttk.Button(todo_frame, text="Edit", command=lambda: self.edit_todo_item(todo_frame, todo_label, title, date_str))
        edit_button.pack(side=tk.LEFT, padx=5)

        delete_button = ttk.Button(todo_frame, text="Delete", command=lambda: self.delete_todo_item(todo_frame, title))
        delete_button.pack(side=tk.LEFT, padx=5)

        self.todos.append(todo_frame)
        self.todo_dict[title] = {"frame": todo_frame, "date": date_str}

    def edit_todo_item(self, todo_frame, todo_label, old_title, old_date_str):
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Todo")

        todo_text = todo_label.cget("text")
        edit_entry = ttk.Entry(edit_window, width=50)
        edit_entry.insert(0, todo_text)
        edit_entry.pack(pady=10)

        def save_edit():
            new_todo_text = edit_entry.get()
            todo_label.config(text=new_todo_text)
            edit_window.destroy()

            # Update CSV
            new_title = new_todo_text.split(' on ')[0]
            df = pd.read_csv('events.csv')

            if old_title in df['Title'].values:
                df.loc[df['Title'] == old_title, 'Title'] = new_title
                df.to_csv('events.csv', index=False)
                self.todo_dict.pop(old_title)
                self.todo_dict[new_title] = {"frame": todo_frame, "date": old_date_str}

        save_button = ttk.Button(edit_window, text="Save", command=save_edit)
        save_button.pack(pady=10)

    def delete_todo_item(self, todo_frame, title):
        todo_frame.destroy()
        self.todos.remove(todo_frame)
        self.todo_dict.pop(title)

        # Delete the todo from CSV
        df = pd.read_csv('events.csv')
        df = df[df['Title'] != title]
        df.to_csv('events.csv', index=False)

    def add_todo(self):
        todo_text = self.todo_entry.get()
        if todo_text:
            date_added = datetime.now().strftime("%Y-%m-%d")
            todo_with_date = f"{todo_text} on {date_added}"
            self.add_todo_item(todo_with_date, todo_text, date_added)
            self.todo_entry.delete(0, tk.END)

            # Add the todo to CSV
            new_todo = pd.DataFrame({"Title": [todo_text], "Date": [date_added], "Formatted_Date": [date_added]})
            new_todo.to_csv('events.csv', mode='a', header=False, index=False)

def empty_dataset():
    df = pd.read_csv('events.csv')
    df = pd.DataFrame(columns=df.columns)
    df.to_csv('events.csv', index=False)
    
if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
    empty_dataset()