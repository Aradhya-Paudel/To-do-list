import turtle
import json
import os
from datetime import datetime

tasks = []
buttons = []
FILENAME = "tasks.json"

drawer = turtle.Turtle()
drawer.hideturtle()
drawer.penup()
drawer.speed(0)

def load_tasks():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_tasks():
    with open(FILENAME, "w") as f:
        json.dump(tasks, f)

def to_24_hour(hour, minute, ampm):
    hour = int(hour)
    minute = int(minute)
    ampm = ampm.strip().upper()
    if ampm == "PM" and hour != 12:
        hour += 12
    elif ampm == "AM" and hour == 12:
        hour = 0
    return f"{hour:02d}:{minute:02d}"

def to_12_hour(time24):
    hour, minute = map(int, time24.split(":"))
    ampm = "AM"
    if hour >= 12:
        ampm = "PM"
    hour12 = hour % 12
    if hour12 == 0:
        hour12 = 12
    return f"{hour12}:{minute:02d} {ampm}"

def select_time():
    hour = screen.numinput("Set Reminder Time", "Select hour (1-12):", minval=1, maxval=12)
    if hour is None:
        return None
    hour = int(hour)

    minute = screen.numinput("Set Reminder Time", "Select minutes (0-59):", minval=0, maxval=59)
    if minute is None:
        return None
    minute = int(minute)

    ampm = screen.textinput("Set Reminder Time", "Enter AM or PM:").strip().upper()
    if ampm not in ["AM", "PM"]:
        return None

    return to_24_hour(hour, minute, ampm)

def draw_ui():
    screen.tracer(0)
    drawer.clear()
    draw_header()
    draw_buttons()
    draw_tasks()
    screen.tracer(1)

def draw_header():
    drawer.goto(0, 230)
    drawer.color("#222")
    drawer.write("To-Do List", align="center", font=("Arial", 16, "bold"))

def draw_buttons():
    buttons.clear()
    labels = ["Add Task", "Complete Task", "Delete Task", "Edit Task", "Clear Completed"]
    button_width = 140
    spacing = 20
    total_width = len(labels) * button_width + (len(labels) - 1) * spacing
    start_x = -total_width // 2
    y = 150

    for i, label in enumerate(labels):
        x = start_x + i * (button_width + spacing)
        draw_button(x, y, label)
        buttons.append((x, y, label))

def draw_button(x, y, label):
    drawer.goto(x, y)
    drawer.fillcolor("#4f8ef7")
    drawer.begin_fill()
    for _ in range(2):
        drawer.forward(140)
        drawer.right(90)
        drawer.forward(40)
        drawer.right(90)
    drawer.end_fill()
    drawer.penup()
    drawer.goto(x + 70, y - 30)
    drawer.color("white")
    drawer.write(label, align="center", font=("Arial", 12, "bold"))
    drawer.color("black")

def draw_tasks():
    y_start = 70  
    now = datetime.now()
    current_24 = now.strftime("%H:%M")

    for i, task in enumerate(tasks):
        y = y_start - i * 30
        drawer.goto(-300, y)
        status = "✔" if task['done'] else "✗"
        if task['priority'] == "High":
            color = "red"
        elif task['priority'] == "Medium":
            color = "orange"
        else:
            color = "green"

        reminder_24 = task.get('reminder', '')
        if reminder_24 and not task['done']:
            if current_24 > reminder_24:
                color = "darkred"

        drawer.color(color)
        reminder_str = f" (Remind at: {to_12_hour(reminder_24)})" if reminder_24 else ""
        drawer.write(f"{i+1}. [{status}] [{task['priority'][0]}] {task['desc']}{reminder_str}", font=("Arial", 12, "normal"))

    drawer.color("black")

def add_task():
    desc = screen.textinput("New Task", "Enter task description:")
    if not desc:
        return
    priority = screen.textinput("Priority", "Enter priority (Low, Medium, High):")
    if priority:
        priority = priority.capitalize()
        if priority not in ["Low", "Medium", "High"]:
            priority = "Low"
    else:
        priority = "Low"

    reminder_time = select_time()
    if reminder_time is None:
        reminder_time = ""

    tasks.append({'desc': desc, 'done': False, 'priority': priority, 'reminder': reminder_time})
    save_tasks()
    draw_ui()

def complete_task():
    if not tasks:
        return
    idx = screen.numinput("Complete Task", "Enter task number:", minval=1, maxval=len(tasks))
    if idx:
        tasks[int(idx)-1]['done'] = True
        save_tasks()
        draw_ui()

def delete_task():
    if not tasks:
        return
    idx = screen.numinput("Delete Task", "Enter task number:", minval=1, maxval=len(tasks))
    if idx:
        tasks.pop(int(idx)-1)
        save_tasks()
        draw_ui()

def edit_task():
    if not tasks:
        return
    idx = screen.numinput("Edit Task", "Enter task number to edit:", minval=1, maxval=len(tasks))
    if not idx:
        return
    idx = int(idx) - 1
    task = tasks[idx]
    new_desc = screen.textinput("Edit Description", "Edit task description:", initialvalue=task['desc'])
    if new_desc:
        task['desc'] = new_desc
    new_priority = screen.textinput("Edit Priority", "Edit priority (Low, Medium, High):", initialvalue=task['priority'])
    if new_priority:
        new_priority = new_priority.capitalize()
        if new_priority in ["Low", "Medium", "High"]:
            task['priority'] = new_priority

    change_reminder = screen.textinput("Edit Reminder", "Change reminder time? (yes/no):", initialvalue="no")
    if change_reminder and change_reminder.lower() == "yes":
        new_reminder = select_time()
        if new_reminder is not None:
            task['reminder'] = new_reminder

    save_tasks()
    draw_ui()

def clear_completed():
    global tasks
    tasks = [t for t in tasks if not t['done']]
    save_tasks()
    draw_ui()

def on_click(x, y):
    for bx, by, label in buttons:
        if bx <= x <= bx + 140 and by - 40 <= y <= by:
            if label == "Add Task":
                add_task()
            elif label == "Complete Task":
                complete_task()
            elif label == "Delete Task":
                delete_task()
            elif label == "Edit Task":
                edit_task()
            elif label == "Clear Completed":
                clear_completed()

def on_exit():
    save_tasks()
    screen.bye()

tasks = load_tasks()
for t in tasks:
    if 'priority' not in t:
        t['priority'] = "Low"
    if 'reminder' not in t:
        t['reminder'] = ""

screen = turtle.Screen()
screen.title("To-Do List")
screen.bgcolor("#f4f7fa")
screen.setup(width=800, height=550)
screen.onclick(on_click)
screen.onkeypress(on_exit, "Escape")
screen.listen()

draw_ui()
screen.mainloop()
