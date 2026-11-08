import os
import qrcode
from tkinter import (
    Tk, Frame, Label, Entry, Button, StringVar, messagebox, PhotoImage
)

# --- цвета темы ---
BG = "#1e1e1e"        # основной фон (тёмно-серый)
PANEL = "#2b2b2b"     # фон полей ввода
FG = "#e6e6e6"        # светлый текст
HINT = "#8a8a8a"      # приглушённый текст
ACCENT = "#3a3a3a"    # кнопки
ACCENT_HOVER = "#505050"


def make_qr():
    """Генерирует QR-код, сохраняет его и показывает превью."""
    data = text_var.get().strip()
    if not data:
        messagebox.showerror("Ошибка", "Введите текст или ссылку")
        return

    try:
        version = int(size_var.get())
        if not 1 <= version <= 40:
            raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка", "Размер должен быть числом от 1 до 40")
        return

    folder = folder_var.get().strip() or os.getcwd()
    filename = filename_var.get().strip() or "qrcode"
    path = os.path.join(folder, filename + ".png")

    if not os.path.isdir(folder):
        messagebox.showerror("Ошибка", f"Папка не существует:\n{folder}")
        return

    try:
        qr = qrcode.QRCode(version=version, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image()
        img.save(path)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось создать QR-код:\n{e}")
        return

    show_preview(path)
    status_var.set(f"Сохранено:\n{path}")


def show_preview(path):
    """Загружает PNG и отображает его в окне (при необходимости — уменьшает)."""
    global preview_image
    try:
        img = PhotoImage(file=path)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось открыть картинку:\n{e}")
        return

    # уменьшаем, если картинка больше 260px по стороне
    limit = 260
    w, h = img.width(), img.height()
    if max(w, h) > limit:
        factor = max(w, h) // limit + 1
        img = img.subsample(factor, factor)

    preview_image = img  # важно: ссылка должна жить, иначе картинка исчезнет
    image_label.config(image=preview_image, text="")


# --- главное окно ---
root = Tk()
root.title("Генератор QR-кодов")
root.geometry("860x560")
root.configure(bg=BG)

# центрирование контейнера: 1 ячейка, растянутая на всё окно
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

main = Frame(root, bg=BG)
main.grid(row=0, column=0)   # без sticky => Frame центрируется сам

# ------- левая панель: форма -------
form = Frame(main, bg=BG)
form.grid(row=0, column=0, padx=40, pady=20, sticky="n")

text_var = StringVar()
folder_var = StringVar()
filename_var = StringVar(value="qrcode")
size_var = StringVar(value="10")
status_var = StringVar(value="Здесь появится превью")

fields = [
    ("Текст или ссылка:", text_var),
    ("Папка для сохранения:", folder_var),
    ("Имя файла:", filename_var),
    ("Размер (1–40):", size_var),
]

for row, (title, var) in enumerate(fields):
    Label(form, text=title, bg=BG, fg=FG,
          font=("Courier", 12, "bold")).grid(
        row=row, column=0, sticky="w", pady=10)
    Entry(form, textvariable=var, font="Century 12", width=38,
          bg=PANEL, fg=FG, insertbackground=FG, relief="flat").grid(
        row=row, column=1, padx=(12, 0), pady=10, sticky="w")

Button(form, text="Сгенерировать",
       font=("Courier", 14, "bold"),
       bg=ACCENT, fg=FG,
       activebackground=ACCENT_HOVER, activeforeground=FG,
       relief="flat", padx=20, pady=6,
       command=make_qr).grid(
    row=len(fields), column=0, columnspan=2, pady=25)

# ------- правая панель: превью -------
preview_frame = Frame(main, bg=BG)
preview_frame.grid(row=0, column=1, padx=40, pady=20, sticky="n")

Label(preview_frame, text="Предпросмотр", bg=BG, fg=FG,
      font=("Courier", 12, "bold")).pack(pady=(0, 10))

# фиксированная площадка под картинку, чтобы окно не «прыгало»
image_holder = Frame(preview_frame, bg=BG, width=270, height=270)
image_holder.pack_propagate(False)
image_holder.pack()

image_label = Label(image_holder, bg=BG, fg=HINT,
                    text="(пусто)", font=("Courier", 11))
image_label.pack(expand=True, fill="both")

Label(preview_frame, textvariable=status_var, bg=BG, fg=HINT,
      font=("Courier", 10), wraplength=270,
      justify="center").pack(pady=15)

root.mainloop()