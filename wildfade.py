import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

# 🐾 Load CSV (Update this path to your own file)
csv_path = r"C:\Users\gracy\OneDrive\Documents\wildfade\WildFade_Detailed_Extinct_Asia.csv"
df = pd.read_csv(csv_path)

# 🎨 Setup GUI window
root = tk.Tk()
root.title("🌿 WildFade: Echoes of Extinction in the Wilds of Asia")
root.geometry("850x650")
root.configure(bg="#e6f2ff")

tk.Label(root, text="🌿 WildFade", font=("Segoe UI", 18, "bold"), bg="#e6f2ff", fg="#003366").pack(pady=10)

# 🌍 Country Selection
tk.Label(root, text="Select Country:", bg="#e6f2ff", font=("Segoe UI", 12, "bold")).pack()
country_combo = ttk.Combobox(root, values=sorted(df["Country"].unique()), state="readonly", width=50)
country_combo.pack(pady=5)

# 🎯 Category Selection Buttons
selected_category = tk.StringVar(value="")
selected_animal = tk.StringVar(value="")

def highlight_button(selected):
    selected_category.set(selected)
    if selected == "Animal":
        animal_btn.config(bg="#800080")
        bird_btn.config(bg="#3F51B5")
    elif selected == "Bird":
        bird_btn.config(bg="#800080")
        animal_btn.config(bg="#009688")

# 🐾 Animal/Bird Radio Button Area
radio_frame = tk.Frame(root, bg="#e6f2ff")
radio_frame.pack(pady=5)

def update_animals(category):
    highlight_button(category)
    selected_country = country_combo.get()
    selected_animal.set("")  # ✅ Reset radio button selection

    # Clear previous buttons
    for widget in radio_frame.winfo_children():
        widget.destroy()

    if not selected_country:
        messagebox.showwarning("Missing Info", "Please select a country first.")
        return

    filtered = df[df["Country"] == selected_country]

    if category == "Animal":
        result = filtered[~filtered['Animal/Bird Name'].str.lower().str.contains("duck|lapwing|quail|eagle|vulture|owl|bird|dove")]
        message = "🎉 Great news! No animals went extinct in this country."
    else:
        result = filtered[filtered['Animal/Bird Name'].str.lower().str.contains("duck|lapwing|quail|eagle|vulture|owl|bird|dove")]
        message = "🎉 Great news! No birds went extinct in this country."

    if result.empty:
        messagebox.showinfo("Nothing Found", message)
        info_box.delete("1.0", tk.END)
    else:
        tk.Label(radio_frame, text="Select Animal/Bird:", bg="#e6f2ff", font=("Segoe UI", 12, "bold")).pack()
        for name in result["Animal/Bird Name"].tolist():
            tk.Radiobutton(
                radio_frame, text=name, variable=selected_animal, value=name,
                bg="#e6f2ff", anchor="w", font=("Segoe UI", 10), wraplength=600
            ).pack(fill="x", padx=10, anchor="w")

# 💜 Buttons to Choose Animals or Birds
animal_btn = tk.Button(root, text="Show Animals", bg="#009688", fg="white",
                       font=("Segoe UI", 10, "bold"), width=18, command=lambda: update_animals("Animal"))
animal_btn.pack(pady=5)

bird_btn = tk.Button(root, text="Show Birds", bg="#3F51B5", fg="white",
                     font=("Segoe UI", 10, "bold"), width=18, command=lambda: update_animals("Bird"))
bird_btn.pack(pady=5)

# 📋 Information Display
info_box = tk.Text(root, height=12, wrap="word", font=("Segoe UI", 11),
                   bg="#ffffff", fg="#000000", borderwidth=2, relief="ridge")
info_box.pack(padx=20, pady=15, fill="both", expand=True)

# 🧠 Show Info Logic
def show_info():
    country = country_combo.get()
    animal = selected_animal.get()
    if country and animal:
        record = df[(df["Country"] == country) & (df["Animal/Bird Name"] == animal)]
        if not record.empty:
            details = record.iloc[0]
            info = (
                f"🦴 Scientific Name:\n{details['Scientific Name']}\n\n"
                f"🌍 Origin/Range:\n{details['Origin / Native Range']}\n\n"
                f"🕰️ Lifetime/Era:\n{details['Lifetime / Era']}\n\n"
                f"⚠️ Cause of Extinction:\n{details['Cause of Extinction']}\n\n"
                f"📅 Year of Extinction:\n{details['Extinction Year']}\n\n"
                f"📌 Additional Facts:\n{details['Additional Facts']}"
            )
            info_box.delete("1.0", tk.END)
            info_box.insert(tk.END, info)
        else:
            messagebox.showinfo("Oops", "No info found.")
    else:
        messagebox.showwarning("Missing Info", "Please select an animal/bird to view information.")

# 🔎 Show Info Button
tk.Button(root, text="Show Information", command=show_info, bg="#3366cc", fg="white",
          font=("Segoe UI", 11, "bold")).pack(pady=10)

root.mainloop()
