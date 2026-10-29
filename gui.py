import tkinter as tk
from tkinter import filedialog
from main import analyze_file
import json

window = tk.Tk()
window.title("ThreatLens - File Analyzer")
window.geometry("650x450")

title = tk.Label(
    window,
    text="ThreatLens",
    font=("Arial", 22, "bold")
)
title.pack(pady=20)

last_result = None


def select_file():
    global last_result

    file_path = filedialog.askopenfilename()

    # Si el usuario cancela la selección, no hacemos nada
    if not file_path:
        return

    # Limpiamos el resultado anterior
    last_result = None

    # Analizamos el archivo seleccionado
    result = analyze_file(file_path)

    # Comprobamos si ocurrió un error
    if "error" in result:
        result_label.config(text=result["error"])
        return

    # Guardamos el análisis para poder exportarlo
    last_result = result

    matches = result["yara_matches"]
    matches_text = ", ".join(matches) if matches else "None"

    result_text = (
        f"File: {result['file_name']}\n"
        f"Size: {result['file_size']} bytes\n"
        f"SHA-256: {result['sha256']}\n"
        f"YARA matches: {matches_text}"
    )

    result_label.config(text=result_text)

def export_report():
    if last_result is None:
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")]
    )

    if save_path:
        with open(save_path, "w", encoding="utf-8") as file:
            json.dump(last_result, file, indent=4)

browse_button = tk.Button(
    window,
    text="Select File",
    command=select_file
)
browse_button.pack(pady=10)

export_button = tk.Button(
    window,
    text="Export Report",
    command=export_report
)

export_button.pack(pady=10)

result_label = tk.Label(
    window,
    text="Select a file to see the results.",
    justify="left",
    anchor="w",
    wraplength=580,
    font=("Consolas", 11)
)

result_label.pack(
    padx=20,
    pady=20,
    fill="x"
)

window.mainloop()