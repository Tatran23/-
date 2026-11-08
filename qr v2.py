import os
import tempfile
import qrcode
from tkinter import Tk, Label, Entry, Button, StringVar, PhotoImage, Frame, messagebox

# ---------- цвета темы ----------
BG        = "#2b2b2b"   # тёмно-серый фон окна
BG_FIELD  = "#3c3c3c"   # фон полей ввода (чуть светлее окна)
FG        = "#e6e6e6"   # светлый текст
ACCENT    = "#8e44ad"   # фиолетовый акцент для кнопки

# глобальная ссылка на изображение-предпросмотр.
# Tkinter удаляет PhotoImage из памяти, если на него никто не ссылается,
# поэтому держим его в модульной переменной.
preview_image = None


# ---------- логика генерации ----------
def generate_qr():
    """Читает поля, сохраняет PNG с QR-кодом и показывает предпросмотр."""
    global preview_image

    # 1) читаем и проверяем текст/ссылку
    data = text_var.get().strip()
    if not data:
        messagebox.showerror("Ошибка", "Введите текст или ссылку")
        return

    # 2) проверяем размер (1..40)
    try:
        version = int(size_var.get())
        if not 1 <= version <= 40:
            raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка", "Размер должен быть числом от 1 до 40")
        return

    # 3) путь сохранения: папка и имя файла (по умолчанию — текущая папка)
    folder   = folder_var.get().strip() or os.getcwd()
    filename = filename_var.get().strip() or "qrcode"
    path     = os.path.join(folder, filename + ".png")

    # 4) создаём QR-код с параметрами пользователя
    qr = qrcode.QRCode(version=version, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    qr.make_image().save(path)         # полный PNG — сохраняем на диск

    # 5) уменьшенная копия для предпросмотра внутри окна
    qr.box_size = 5
    qr.border   = 2
    preview_path = os.path.join(tempfile.gettempdir(), "qr_preview.png")
    qr.make_image().save(preview_path)

    # 6) показываем предпросмотр в окне
    preview_image = PhotoImage(file=preview_path)
    preview_label.config(image=preview_image)

    # 7) сообщаем пользователю, куда сохранили файл
    messagebox.showinfo("Готово", f"QR-код сохранён:\n{path}")


# ---------- главное окно ----------
root = Tk()
root.title("Генератор QR-кодов")
root.geometry("720x780")
root.configure(bg=BG)
root.resizable(False, False)

# контейнер по центру окна: place с anchor="center" ставит его ровно посередине
container = Frame(root, bg=BG)
container.place(relx=0.5, rely=0.5, anchor="center")

# ---------- переменные полей ввода ----------
text_var     = StringVar()               # текст/URL
folder_var   = StringVar()               # куда сохранять
filename_var = StringVar(value="qrcode") # имя файла
size_var     = StringVar(value="10")     # версия QR (1–40)

# ---------- поля ввода: (подпись, переменная) ----------
fields = [
    ("Текст или ссылка:",      text_var),
    ("Папка для сохранения:",  folder_var),
    ("Имя файла:",             filename_var),
    ("Размер (1–40):",         size_var),
]

for row, (caption, var) in enumerate(fields):
    # подпись слева
    Label(container, text=caption, bg=BG, fg=FG,
          font=("Courier", 12, "bold")).grid(
        row=row, column=0, sticky="w", padx=(0, 12), pady=8)
    # само поле справа
    Entry(container, textvariable=var, font="Century 12", width=36,
          bg=BG_FIELD, fg=FG, insertbackground=FG,
          relief="flat", highlightthickness=1,
          highlightbackground="#555", highlightcolor=ACCENT).grid(
        row=row, column=1, pady=8)

# ---------- метка для предпросмотра QR ----------
preview_label = Label(container, bg=BG)
preview_label.grid(row=len(fields), column=0, columnspan=2, pady=15)

# ---------- кнопка генерации ----------
Button(container, text="Сгенерировать", font=("Courier", 14),
       bg=ACCENT, fg="white", activebackground="#a569bd",
       relief="flat", cursor="hand2",
       command=generate_qr).grid(
    row=len(fields) + 1, column=0, columnspan=2, pady=(0, 10),
    ipadx=12, ipady=4)

# ---------- запуск ----------
root.mainloop()