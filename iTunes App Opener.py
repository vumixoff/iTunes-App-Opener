import customtkinter as ctk
import webbrowser

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("500x300")
        self.title("iTunes App Opener")

        ctk.CTkLabel(
            self,
            text="iTunes App Opener",
            font=("Fixedsys", 28, "bold")
        ).pack(pady=20)

        self.appid = ctk.CTkEntry(
            self,
            width=350,
            placeholder_text="Поиск приложения по ID",
            font=("Arial", 27, "bold")
            
        )
        self.appid.pack(pady=15)

        ctk.CTkButton(
            self,
            text="Открыть в iTunes",
            font=("Times New Roman", 15, "bold"),
            width=200,
            command=self.open_itunes
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Открыть AppStore в браузере",
            font=("Times New Roman", 15, "bold"),
            width=200,
            command=self.open_browser
        ).pack(pady=5)

    def open_itunes(self):
        app_id = self.appid.get().strip()
        if app_id:
            webbrowser.open(
                f"itmss://itunes.apple.com/app/id{app_id}"
            )

    def open_browser(self):
        webbrowser.open("https://apps.apple.com")

App().mainloop()