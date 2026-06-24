import customtkinter as ctk
import webbrowser
import os
import requests
import threading
import subprocess
from PIL import Image
import io

ctk.set_appearance_mode("System") #Авто-тема
ctk.set_default_color_theme("dark-blue") #Тема


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1000x800") 
        self.title("iTunes App Opener")

        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)

        #Вкладки
        self.tab1 = self.tabs.add("Открыть по ID")
        self.tab2 = self.tabs.add("AppStore")
        self.tab3 = self.tabs.add("Proxy")

        #лого
        ctk.CTkLabel(
            self.tab1,
            text="iTunes App Opener",
            font=("Fixedsys", 28, "bold")
        ).pack(pady=20)

        ctk.CTkLabel(
            self.tab2,
            text="iTunes App Opener",
            font=("Fixedsys", 28, "bold")
        ).pack(pady=20)

        ctk.CTkLabel(
            self.tab3,
            text="iTunes App Opener",
            font=("Fixedsys", 28, "bold")
        ).pack(pady=20)

        #Кнопки
        self.appid = ctk.CTkEntry(
            self.tab1,
            width=350,
            placeholder_text="Поиск приложения по ID...",
            font=("Arial", 20, "bold"),
            justify="center"
        )
        self.appid.pack(pady=15,anchor="center")
        self.appid.bind(
            "<KeyPress>",
            self.paste_text
        )


        ctk.CTkButton(
            self.tab1,
            text="Открыть в iTunes",
            font=("Times New Roman", 15, "bold"),
            width=200,
            command=self.open_itunes
        ).pack(pady=10)

        ctk.CTkButton(
            self.tab1,
            text="Открыть AppStore в браузере",
            font=("Times New Roman", 15, "bold"),
            width=200,
            command=self.open_browser
        ).pack(pady=5)

        #AppStoreWeb


        search_frame = ctk.CTkFrame(self.tab2, fg_color="transparent")
        search_frame.pack(fill="x", padx=30, pady=10)

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Поиск приложений...",justify="center", font=("Arial", 20, "bold"))
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.search_entry.bind(
            "<Return>",
        lambda event: self.start_search_thread()
        )

        self.country = ctk.CTkComboBox(search_frame, values=["ru","us","cn","jp","fr","gb","de"], width=80)
        self.country.set("ru")
        self.country.pack(side="left", padx=5)

        ctk.CTkButton(search_frame, text="Поиск", width=90, command=self.start_search_thread).pack(side="left", padx=(5, 0))

        self.scroll = ctk.CTkScrollableFrame(self.tab2, width=850, height=420)
        self.scroll.pack(fill="both", expand=True, padx=30, pady=10)

        # --- ВКЛАДКА 3 ---

        proxy_buttons = ctk.CTkFrame(self.tab3, fg_color="transparent")
        proxy_buttons.pack(pady=10)

        # Исправлено: Добавлен self. перед методами прокси
        ctk.CTkButton(proxy_buttons, text="Запустить Proxy",font=("Times New Roman", 15, "bold"), command=self.proxy_mode_on).pack(side="left", padx=10)
        ctk.CTkButton(proxy_buttons, text="Остановить Proxy",font=("Times New Roman", 15, "bold"),command=self.proxy_mode_off).pack(side="left", padx=10)

        self.status = ctk.CTkLabel(self.tab3, text="Остановлено", font=("Arial", 16, "bold"), text_color="red")
        self.status.pack(pady=15)

    #Открытие iTunes
    def open_itunes(self):
        app_id = self.appid.get().strip()
        if app_id:
            webbrowser.open(f"itmss://itunes.apple.com/app/id{app_id}")

    #Открытие браузера
    def open_browser(self):
        webbrowser.open("https://apps.apple.com")

    #Поиск
    def search(self):
        query = self.search_entry.get().strip()
        country = self.country.get()

        if not query:
            return

        url = "https://itunes.apple.com/search"
        params = {
            "term": query,
            "country": country,
            "entity": "software",
            "limit": 20
        }

        try:
            r = requests.get(url, params=params, timeout=5)
            data = r.json()
        except Exception:
            return

        for w in self.scroll.winfo_children():
            w.destroy()

        self.results = []

        for app in data.get("results", []):
            self.results.append(app)

            frame = ctk.CTkFrame(self.scroll)
            frame.pack(fill="x", pady=5, padx=5)

            icon_url = app.get("artworkUrl100")
            img_label = ctk.CTkLabel(frame, text="")
            img_label.pack(side="left", padx=10, pady=5)

            try:
                img_data = requests.get(icon_url, timeout=3).content
                img = Image.open(io.BytesIO(img_data))
                photo = ctk.CTkImage(light_image=img, dark_image=img, size=(60, 60))
                img_label.configure(image=photo)
                img_label.image = photo
            except Exception:
                img_label.configure(text="No Img")

            name = app.get("trackName", "Unknown")
            app_id = app.get("trackId", "Unknown")

            info = ctk.CTkLabel(frame, text=f"{name}\nID: {app_id}", anchor="w", justify="left")
            info.pack(side="left", padx=10, fill="x", expand=True)

            ctk.CTkButton(
                frame, text="Открыть", width=120,
                command=lambda i=app_id: webbrowser.open(f"itmss://itunes.apple.com/app/id{i}")
            ).pack(side="right", padx=5)

            ctk.CTkButton(
                frame, text="Скопировать ID", width=120,
                command=lambda i=app_id: self.copy(i)
            ).pack(side="right", padx=5)
        

    #Добавлен недостающий метод для поиска
    def start_search_thread(self):
        threading.Thread(target=self.search, daemon=True).start()

    #Включение прокси
    def proxy_mode_on(self):
        try:
            os.startfile("Proxy.exe")
            self.status.configure(text="Включено", text_color="green")
        except FileNotFoundError:
            print("Ошибка: Файл Proxy.exe не найден, добавьте Proxy.exe и повторите попытку!")
    #Выключение прокси
    def proxy_mode_off(self):
        try:
            os.system("taskkill /F /IM Proxy.exe")
            self.status.configure(text="Остановлено", text_color="red")
        except Exception as e:
            print(f"Не удалось остановить прокси: {e}")

    #Копирование ID
    def copy(self, text):
        self.clipboard_clear()
        self.clipboard_append(str(text))

    #Вставка текста
    def paste_text(self, event):
        if event.state & 0x4:
            try:
                self.appid.insert(
                    "insert",
                    self.clipboard_get()
                )
            except:
                pass
            return "break"

if __name__ == "__main__":
    App().mainloop()
