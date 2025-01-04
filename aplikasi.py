import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Label, Entry, Button
from PIL import Image, ImageTk
from PIL.Image import Resampling
import numpy as np

def animate_label(label, text):
    """Fungsi untuk animasi teks."""
    for i in range(len(text) + 1):
        label.config(text=text[:i])
        root.update_idletasks()

def on_enter(e):
    """Efek hover saat mouse masuk."""
    e.widget['background'] = '#45a049'

def on_leave(e):
    """Efek hover saat mouse keluar."""
    e.widget['background'] = '#4CAF50'

def simplex_method(z, constraints, rhs):
    try:
        # Inisialisasi tabel Simpleks
        num_vars = len(z)
        num_constraints = len(constraints)

        table = np.zeros((num_constraints + 1, num_vars + num_constraints + 1))
        table[:-1, :num_vars] = constraints
        table[:-1, num_vars:num_vars + num_constraints] = np.eye(num_constraints)
        table[:-1, -1] = rhs
        table[-1, :num_vars] = -np.array(z)

        # Iterasi Simpleks
        while True:
            # Cek optimalitas
            if all(val >= 0 for val in table[-1, :-1]):
                break

            # Temukan pivot kolom
            pivot_col = np.argmin(table[-1, :-1])
            if all(row[pivot_col] <= 0 for row in table[:-1]):
                raise ValueError("Masalah tidak memiliki solusi terbatas.")

            # Temukan pivot baris
            ratios = []
            for i in range(num_constraints):
                if table[i, pivot_col] > 0:
                    ratios.append(table[i, -1] / table[i, pivot_col])
                else:
                    ratios.append(float('inf'))
            pivot_row = np.argmin(ratios)

            # Pivoting
            pivot_element = table[pivot_row, pivot_col]
            table[pivot_row, :] /= pivot_element
            for i in range(len(table)):
                if i != pivot_row:
                    table[i, :] -= table[i, pivot_col] * table[pivot_row, :]

        # Ekstrak solusi
        solutions = np.zeros(num_vars)
        for i in range(num_vars):
            col = table[:-1, i]
            if np.count_nonzero(col == 1) == 1 and np.count_nonzero(col) == 1:
                row = np.where(col == 1)[0][0]
                solutions[i] = table[row, -1]

        z_value = table[-1, -1]
        return solutions, z_value
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def validate_input(input_str):
    """Fungsi untuk memvalidasi input dan memastikan dipisahkan dengan spasi."""
    try:
        # Pastikan semua nilai dipisahkan dengan spasi
        values = [float(i) for i in input_str.split()]
        return values
    except ValueError:
        raise ValueError("Pastikan semua nilai dipisahkan dengan spasi dan berupa angka.")

def calculate():
    """Fungsi untuk menghitung hasil menggunakan Metode Simpleks."""
    try:
        z = validate_input(entry_objective.get())
        constraints = int(entry_constraints.get())

        A = []
        b = []
        for i in range(constraints):
            constraint = validate_input(input_entries[i].get())
            rhs_value = float(rhs_entries[i].get())
            if len(constraint) != len(z):
                raise ValueError("Jumlah elemen kendala harus sama dengan jumlah variabel.")
            A.append(constraint)
            b.append(rhs_value)

        A = np.array(A)
        b = np.array(b)

        solutions, optimal_value = simplex_method(z, A, b)
        hasil = f'Hasil Optimal: {optimal_value}\nSolusi: {solutions}'
    except ValueError as ve:
        hasil = f"Error: {ve}. Pastikan Anda memasukkan nilai-nilai yang dipisahkan dengan spasi."
    except Exception as e:
        hasil = f'Error: {e}'
    label_result.config(text=hasil)

def run_app():
    global root, entry_objective, entry_constraints, input_entries, rhs_entries, label_result
    root = ttk.Window(themename="darkly")
    root.title("Aplikasi Metode Simpleks")
    root.geometry("800x600")
    root.iconbitmap("candy.ico")

    bg_image = Image.open("metode simplek.png")
    bg_image = bg_image.resize((800, 600), Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    label_title = ttk.Label(root, text="", font=("Helvetica", 18, "bold"), bootstyle=PRIMARY)
    label_title.pack(pady=20)
    animate_label(label_title, "Aplikasi Metode Simpleks")

    frame_input = ttk.Frame(root, padding=20, relief="ridge")
    frame_input.pack(pady=20, padx=20, fill="x")

    label_input = ttk.Label(frame_input, text="Masukkan Koefisien Fungsi Tujuan (z):", bootstyle=INFO)
    label_input.grid(row=0, column=0, sticky="w", padx=5, pady=5)

    entry_objective = ttk.Entry(frame_input, bootstyle=SUCCESS)
    entry_objective.grid(row=0, column=1, sticky="w", padx=5, pady=5)

    label_constraints = ttk.Label(frame_input, text="Jumlah Kendala:", bootstyle=INFO)
    label_constraints.grid(row=1, column=0, sticky="w", padx=5, pady=5)

    entry_constraints = ttk.Entry(frame_input, bootstyle=SUCCESS)
    entry_constraints.grid(row=1, column=1, sticky="w", padx=5, pady=5)

    frame_buttons = ttk.Frame(root, padding=20)
    frame_buttons.pack()

    btn_calculate = Button(frame_buttons, text="Hitung", bg="#4CAF50", fg="white", padx=20, pady=10, command=calculate)
    btn_calculate.grid(row=0, column=0, padx=10)

    btn_calculate.bind("<Enter>", on_enter)
    btn_calculate.bind("<Leave>", on_leave)

    btn_exit = Button(frame_buttons, text="Keluar", bg="#f44336", fg="white", padx=20, pady=10, command=root.quit)
    btn_exit.grid(row=0, column=1, padx=10)

    label_result = ttk.Label(root, text="", font=("Helvetica", 12), bootstyle=SUCCESS)
    label_result.pack(pady=20)

    def create_input_entries():
        """Fungsi untuk membuat entri input kendala."""
        global input_entries, rhs_entries
        input_entries = []
        rhs_entries = []
        for i in range(int(entry_constraints.get())):
            label = ttk.Label(frame_input, text=f"Kendala {i+1} (contoh: 1 2 3):", bootstyle=INFO)
            label.grid(row=2+i, column=0, sticky="w", padx=5, pady=5)
            entry = ttk.Entry(frame_input, bootstyle=SUCCESS)
            entry.grid(row=2+i, column=1, sticky="w", padx=5, pady=5)
            input_entries.append(entry)
            label_rhs = ttk.Label(frame_input, text="RHS:", bootstyle=INFO)
            label_rhs.grid(row=2+i, column=2, sticky="w", padx=5, pady=5)
            entry_rhs = ttk.Entry(frame_input, bootstyle=SUCCESS)
            entry_rhs.grid(row=2+i, column=3, sticky="w", padx=5, pady=5)
            rhs_entries.append(entry_rhs)
    
    btn_create_entries = Button(frame_input, text="Buat Entri Kendala", bg="#ff9800", fg="white", command=create_input_entries)
    btn_create_entries.grid(row=2, column=1, sticky="w", padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    run_app()
