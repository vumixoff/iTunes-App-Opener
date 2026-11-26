import customtkinter as ctk
import webbrowser
import os
import json
import requests
import threading
import io
from PIL import Image



ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


ACCENT       = ("#0071E3", "#0A84FF")
ACCENT_HOVER = ("#0062C4", "#409CFF")
ACCENT_SOFT  = ("#E8F0FE", "#1C2C44")
SUCCESS      = ("#28A745", "#34C759")
DANGER       = ("#D70015", "#FF3B30")
MUTED        = ("#86868B", "#8E8E93")
TEXT         = ("#1D1D1F", "#F5F5F7")
CARD         = ("#FFFFFF", "#2C2C2E")
PANEL        = ("#F5F5F7", "#1C1C1E")
SEPARATOR    = ("#E5E5EA", "#38383A")

FONT_DISPLAY = ("Fixedsys", 26, "bold")     
FONT_TITLE   = ("Segoe UI", 18, "bold")     
FONT_BODY    = ("Segoe UI", 14)             
FONT_BODY_B  = ("Segoe UI", 13, "bold")     
FONT_SMALL   = ("Segoe UI", 13)             
FONT_TINY    = ("Segoe UI", 12)             
FONT_INPUT   = ("Segoe UI", 17, "bold")     

APP_NAME = "iTunes App Opener"
APPDATA = os.environ.get("APPDATA") or os.path.expanduser("~")
SETTINGS_DIR = os.path.join(APPDATA, APP_NAME)
SETTINGS_FILE = os.path.join(SETTINGS_DIR, "settings.json")
os.makedirs(SETTINGS_DIR, exist_ok=True)

ALL_REGIONS = [
    "ae","ag","ai","al","am","ao","ar","at","au","az","ba","bb","be","bf","bg","bh",
    "bj","bm","bn","bo","br","bs","bt","bw","by","bz","ca","cg","ch","ci","cl","cm",
    "cn","co","cr","cv","cy","cz","de","dk","dm","do","dz","ec","ee","eg","es","fi",
    "fj","fm","fr","gb","gd","gh","gm","gr","gt","gw","gy","hk","hn","hr","hu","id",
    "ie","il","in","is","it","jm","jo","jp","ke","kg","kh","kn","kr","kw","ky","kz",
    "la","lb","lc","lk","lr","lt","lu","lv","ly","ma","md","me","mg","mk","ml","mm",
    "mn","mo","mr","ms","mt","mu","mv","mw","mx","my","mz","na","ne","ng","ni","nl",
    "no","np","nz","om","pa","pe","pg","ph","pk","pl","pt","pw","py","qa","ro","ru",
    "rw","sa","sb","sc","se","sg","si","sk","sl","sn","sr","sv","sz","tc","td","th",
    "tj","tm","tn","tr","tt","tw","tz","ua","ug","us","uy","uz","vc","ve","vg","vn",
    "ye","za","zm","zw"
]

ALL_LANGUAGES = {
    "aa": "Afaraf", "ab": "Аҧсуа", "ae": "Avesta", "af": "Afrikaans",
    "ak": "Akan", "am": "አማርኛ", "an": "Aragonés", "ar": "العربية",
    "as": "অসমীয়া", "av": "Авар", "ay": "Aymar aru", "az": "Azərbaycan",
    "ba": "Башҡорт", "be": "Беларуская", "bg": "Български", "bh": "भोजपुरी",
    "bi": "Bislama", "bm": "Bamanankan", "bn": "বাংলা", "bo": "བོད་ཡིག",
    "br": "Brezhoneg", "bs": "Bosanski", "ca": "Català", "ce": "Нохчийн",
    "ch": "Chamoru", "co": "Corsu", "cr": "ᓀᐦᐃᔭᐍᐏᐣ", "cs": "Čeština",
    "cu": "Словѣ́ньскъ", "cv": "Чӑваш", "cy": "Cymraeg", "da": "Dansk",
    "de": "Deutsch", "dv": "ދިވެހި", "dz": "རྫོང་ཁ", "ee": "Eʋegbe",
    "el": "Ελληνικά", "en": "English", "eo": "Esperanto", "es": "Español",
    "et": "Eesti", "eu": "Euskara", "fa": "فارسی", "ff": "Fulfulde",
    "fi": "Suomi", "fj": "Vosa Vakaviti", "fo": "Føroyskt", "fr": "Français",
    "fy": "Frysk", "ga": "Gaeilge", "gd": "Gàidhlig", "gl": "Galego",
    "gn": "Avañe'ẽ", "gu": "ગુજરાતી", "gv": "Gaelg", "ha": "هَوُسَ",
    "he": "עברית", "hi": "हिन्दी", "ho": "Hiri Motu", "hr": "Hrvatski",
    "ht": "Kreyòl ayisyen", "hu": "Magyar", "hy": "Հայերեն", "hz": "Otjiherero",
    "ia": "Interlingua", "id": "Bahasa Indonesia", "ie": "Interlingue",
    "ig": "Igbo", "ii": "ꆈꌠ꒿", "ik": "Iñupiaq", "io": "Ido",
    "is": "Íslenska", "it": "Italiano", "iu": "ᐃᓄᒃᑎᑐᑦ", "ja": "日本語",
    "jv": "Basa Jawa", "ka": "ქართული", "kg": "Kikongo", "ki": "Gĩkũyũ",
    "kj": "Kuanyama", "kk": "Қазақ", "kl": "Kalaallisut", "km": "ខ្មែរ",
    "kn": "ಕನ್ನಡ", "ko": "한국어", "kr": "Kanuri", "ks": "कॉशुर",
    "ku": "Kurdî", "kv": "Коми", "kw": "Kernewek", "ky": "Кыргызча",
    "la": "Latina", "lb": "Lëtzebuergesch", "lg": "Luganda", "li": "Limburgs",
    "ln": "Lingála", "lo": "ລາວ", "lt": "Lietuvių", "lu": "Kiluba",
    "lv": "Latviešu", "mg": "Malagasy", "mh": "Kajin M̧ajeļ", "mi": "Te Reo Māori",
    "mk": "Македонски", "ml": "മലയാളം", "mn": "Монгол", "mr": "मराठी",
    "ms": "Bahasa Melayu", "mt": "Malti", "my": "ဗမာ", "na": "Dorerin Naoero",
    "nb": "Norsk bokmål", "nd": "isiNdebele", "ne": "नेपाली", "ng": "Owambo",
    "nl": "Nederlands", "nn": "Norsk nynorsk", "no": "Norsk", "nr": "isiNdebele",
    "nv": "Diné bizaad", "ny": "ChiCheŵa", "oc": "Occitan", "oj": "ᐊᓂᔑᓈᐯᒧᐎᓐ",
    "om": "Oromoo", "or": "ଓଡ଼ିଆ", "os": "Ирон", "pa": "ਪੰਜਾਬੀ",
    "pi": "पाऴि", "pl": "Polski", "ps": "پښتو", "pt": "Português",
    "qu": "Runa Simi", "rm": "Rumantsch", "rn": "Ikirundi", "ro": "Română",
    "ru": "Русский", "rw": "Kinyarwanda", "sa": "संस्कृतम्", "sc": "Sardu",
    "sd": "سنڌي", "se": "Davvisámegiella", "sg": "Sängö", "si": "සිංහල",
    "sk": "Slovenčina", "sl": "Slovenščina", "sm": "Gagana Sāmoa", "sn": "chiShona",
    "so": "Soomaaliga", "sq": "Shqip", "sr": "Српски", "ss": "SiSwati",
    "st": "Sesotho", "su": "Basa Sunda", "sv": "Svenska", "sw": "Kiswahili",
    "ta": "தமிழ்", "te": "తెలుగు", "tg": "Тоҷикӣ", "th": "ไทย",
    "ti": "ትግርኛ", "tk": "Türkmen", "tl": "Tagalog", "tn": "Setswana",
    "to": "Lea Fakatonga", "tr": "Türkçe", "ts": "Xitsonga", "tt": "Татар",
    "tw": "Twi", "ty": "Reo Tahiti", "ug": "ئۇيغۇرچە", "uk": "Українська",
    "ur": "اردو", "uz": "Oʻzbek", "ve": "Tshivenḓa", "vi": "Tiếng Việt",
    "vo": "Volapük", "wa": "Walon", "wo": "Wollof", "xh": "isiXhosa",
    "yi": "ייִדיש", "yo": "Yorùbá", "za": "Vahcuengh", "zh": "中文",
    "zu": "isiZulu",
}

TRANSLATED_LANGS = {"ru", "en"}
LANG = {"value": "ru"}

I18N = {
    "ru": {
        "title": "iTunes App Opener",
        "dark_theme": "Тёмная тема",
        "tab1": "Открыть по ID",
        "tab2": "Найти приложение",
        "tab3": "Управление Proxy",
        "tab4": "Настройки",
        "open_by_id": "Открыть приложение по ID",
        "id_hint": "ID — это число в конце ссылки на приложение в App Store.\n"
                   "Пример: apps.apple.com/app/id1234567890 → ID: 1234567890",
        "id_placeholder": "Введите числовой ID (только цифры)",
        "btn_itunes": "▶  Открыть в iTunes",
        "btn_appstore": "🌍  Открыть AppStore",
        "search_placeholder": "Введите название приложения и нажмите Enter…",
        "btn_search": "🔎  Поиск",
        "region_hint": "Регион влияет на то, какие приложения найдутся.",
        "empty_search": "Здесь появятся результаты поиска.\nПопробуйте, например: «Telegram» или «WhatsApp».",
        "empty_none": "Ничего не найдено.\nПопробуйте другое название или смените регион.",
        "proxy_title": "Управление Proxy",
        "proxy_hint": "Proxy помогает, если приложение недоступно в вашем регионе.\n"
                      "Убедитесь, что файл Proxy.exe лежит рядом с приложением.",
        "btn_proxy_on": "▶  Запустить Proxy",
        "btn_proxy_off": "■  Остановить Proxy",
        "proxy_stopped": "● Proxy остановлен",
        "proxy_running": "● Proxy запущен",
        "proxy_not_found": "● Proxy не запущен",
        "copy_id": "Скопировать ID",
        "open": "Открыть",
        "ready": "Готово",
        "settings_title": "Настройки",
        "settings_lang": "Язык интерфейса",
        "settings_region": "Регион по умолчанию",
        "settings_theme": "Тёмная тема",
        "settings_saved": "Настройки сохранены",
        "settings_apply_lang": "Применить язык",
        "status_searching": "Ищу «{q}» в регионе {c}…",
        "status_not_found": "По запросу «{q}» ничего не найдено",
        "status_found": "Найдено приложений: {n}",
        "status_copied": "ID {i} скопирован в буфер обмена",
        "status_net_err": "Не удалось выполнить поиск. Проверьте интернет.",
        "status_empty_q": "Введите название приложения для поиска",
        "status_no_id": "Сначала введите ID приложения",
        "status_bad_id": "ID должен состоять только из цифр",
        "status_proxy_on": "Proxy запущен",
        "status_proxy_off": "Proxy остановлен",
        "status_proxy_missing": "Proxy.exe не найден",
        "hint_proxy_missing": "Файл Proxy.exe не найден. Положите его рядом с приложением.",
        "hint_proxy_running": "Работает в фоне. Остановите, когда закончите.",
    },
    "en": {
        "title": "iTunes App Opener",
        "dark_theme": "Dark theme",
        "tab1": "Open by ID",
        "tab2": "Find app",
        "tab3": "Proxy control",
        "tab4": "Settings",
        "open_by_id": "Open app by ID",
        "id_hint": "ID — the number at the end of an App Store link.\n"
                   "Example: apps.apple.com/app/id1234567890 → ID: 1234567890",
        "id_placeholder": "Enter numeric ID (digits only)",
        "btn_itunes": "▶  Open in iTunes",
        "btn_appstore": "🌍  Open AppStore",
        "search_placeholder": "Enter app name and press Enter…",
        "btn_search": "🔎  Search",
        "region_hint": "Region affects which apps are found.",
        "empty_search": "Search results will appear here.\nTry «Telegram» or «WhatsApp».",
        "empty_none": "Nothing found.\nTry another name or change region.",
        "proxy_title": "Proxy control",
        "proxy_hint": "Proxy helps if an app is unavailable in your region.\n"
                      "Make sure Proxy.exe is next to the application.",
        "btn_proxy_on": "▶  Start Proxy",
        "btn_proxy_off": "■  Stop Proxy",
        "proxy_stopped": "● Proxy stopped",
        "proxy_running": "● Proxy running",
        "proxy_not_found": "● Proxy not running",
        "copy_id": "Copy ID",
        "open": "Open",
        "ready": "Ready",
        "settings_title": "Settings",
        "settings_lang": "Interface language",
        "settings_region": "Default region",
        "settings_theme": "Dark theme",
        "settings_saved": "Settings saved",
        "settings_path": "Settings file",
        "settings_apply_lang": "Apply language",
        "status_searching": "Searching «{q}» in region {c}…",
        "status_not_found": "Nothing found for «{q}»",
        "status_found": "Apps found: {n}",
        "status_copied": "ID {i} copied to clipboard",
        "status_net_err": "Search failed. Check your internet.",
        "status_empty_q": "Enter an app name to search",
        "status_no_id": "Enter app ID first",
        "status_bad_id": "ID must contain digits only",
        "status_proxy_on": "Proxy started",
        "status_proxy_off": "Proxy stopped",
        "status_proxy_missing": "Proxy.exe not found",
        "hint_proxy_missing": "Proxy.exe not found. Put it next to the app.",
        "hint_proxy_running": "Runs in background. Stop when done.",
    },
}


def tr(key, **kw):
    lang = LANG["value"]
    text = (
        I18N.get(lang, {}).get(key)
        or I18N["en"].get(key)
        or I18N["ru"].get(key, key)
    )
    return text.format(**kw) if kw else text


def load_settings():
    defaults = {"theme": "Dark", "lang": "ru", "region": "ru"}
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        defaults.update({k: v for k, v in data.items() if k in defaults})
    except Exception:
        pass
    return defaults


def save_settings(data):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Не удалось сохранить настройки:", e)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.settings = load_settings()
        LANG["value"] = self.settings["lang"]
        ctk.set_appearance_mode(self.settings["theme"])

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.abspath(os.path.join(BASE_DIR, "icon.ico"))
        self.after(200, lambda: self._safe_icon(icon_path))

        self.geometry("800x400")
        self.minsize(500, 500)
        self.title(tr("title"))
        self.configure(fg_color=PANEL)

        self._state = {
            "appid": "",
            "query": "",
            "results": [],
            "proxy_status": "stopped",
        }

        self._apply_global_style()
        self._build_root()

    def _apply_global_style(self):
        t = ctk.ThemeManager.theme
        t["CTkButton"]["corner_radius"] = 12
        t["CTkButton"]["fg_color"] = ACCENT
        t["CTkButton"]["hover_color"] = ACCENT_HOVER
        t["CTkButton"]["text_color"] = ("#FFFFFF", "#FFFFFF")
        t["CTkButton"]["border_width"] = 0
        t["CTkButton"]["font"] = FONT_BODY_B

        t["CTkEntry"]["corner_radius"] = 12
        t["CTkEntry"]["border_width"] = 1
        t["CTkEntry"]["border_color"] = SEPARATOR
        t["CTkEntry"]["fg_color"] = CARD
        t["CTkEntry"]["text_color"] = TEXT

        t["CTkComboBox"]["corner_radius"] = 12
        t["CTkComboBox"]["border_width"] = 1
        t["CTkComboBox"]["border_color"] = SEPARATOR
        t["CTkComboBox"]["button_color"] = ACCENT
        t["CTkComboBox"]["button_hover_color"] = ACCENT_HOVER

        t["CTkSwitch"]["progress_color"] = ACCENT
        t["CTkSwitch"]["button_hover_color"] = ACCENT_HOVER

        t["CTkScrollbar"]["button_color"] = ACCENT
        t["CTkScrollbar"]["button_hover_color"] = ACCENT_HOVER

    def _build_root(self):
        self._header = ctk.CTkFrame(self, fg_color="transparent")
        self._header.pack(fill="x", padx=28, pady=(22, 0))

        self._tabs_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._tabs_frame.pack(fill="both", expand=True, padx=0, pady=0)

        self._statusbar_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._statusbar_frame.pack(fill="x", padx=0, pady=0)

        self._build_header()
        self._build_tabs()
        self._build_statusbar()
        self._restore_state()

    def _rebuild_ui(self):
        if hasattr(self, "appid"):
            self._state["appid"] = self.appid.get()
        if hasattr(self, "search_entry"):
            self._state["query"] = self.search_entry.get()

        for w in list(self.winfo_children()):
            w.destroy()

        self.title(tr("title"))
        self._build_root()

    def _restore_state(self):
        if self._state["appid"]:
            self.appid.insert(0, self._state["appid"])
        if self._state["query"]:
            self.search_entry.insert(0, self._state["query"])
        if self._state["results"]:
            for app in self._state["results"]:
                self._make_result_card(app)
        st = self._state["proxy_status"]
        if st == "running":
            self.status.configure(text=tr("proxy_running"), text_color=SUCCESS)
            self.proxy_hint.configure(text=tr("hint_proxy_running"))
        elif st == "missing":
            self.status.configure(text=tr("proxy_not_found"), text_color=DANGER)
            self.proxy_hint.configure(text=tr("hint_proxy_missing"), text_color=DANGER)

    def _build_header(self):
        ctk.CTkLabel(
            self._header, text=tr("title"),
            font=FONT_DISPLAY, text_color=TEXT, anchor="center",
        ).pack(fill="x", pady=(0, 2))

    def _toggle_theme(self):
        mode = "Dark" if self.theme_switch.get() else "Light"
        ctk.set_appearance_mode(mode)
        self.settings["theme"] = mode
        save_settings(self.settings)

    def _safe_icon(self, path):
        try:
            if os.path.exists(path):
                self.iconbitmap(path)
        except Exception:
            pass

    def _build_tabs(self):
        self.tabs = ctk.CTkTabview(
            self._tabs_frame, corner_radius=16,
            fg_color="transparent",
            segmented_button_fg_color=PANEL,
            segmented_button_selected_color=ACCENT,
            segmented_button_selected_hover_color=ACCENT_HOVER,
            segmented_button_unselected_hover_color=ACCENT_SOFT,
            border_width=0,
        )
        try:
            self.tabs._segmented_button.configure(corner_radius=10)
        except Exception:
            pass

        self.tabs.pack(fill="both", expand=True, padx=20, pady=(10, 6))

        self.tab1 = self.tabs.add(tr("tab1"))
        self.tab2 = self.tabs.add(tr("tab2"))
        self.tab3 = self.tabs.add(tr("tab3"))
        self.tab4 = self.tabs.add(tr("tab4"))

        self._build_tab1()
        self._build_tab2()
        self._build_tab3()
        self._build_tab4()

    def _build_tab1(self):
        card = ctk.CTkFrame(self.tab1, corner_radius=20, fg_color=CARD,
                            border_width=1, border_color=SEPARATOR)
        card.pack(pady=20, padx=60, fill="x")

        ctk.CTkLabel(card, text=tr("open_by_id"),
                     font=FONT_TITLE, text_color=TEXT).pack(pady=(22, 4))
        ctk.CTkLabel(card, text=tr("id_hint"),
                     font=FONT_SMALL, text_color=MUTED, justify="center").pack(pady=(0, 14))

        self.appid = ctk.CTkEntry(
            card, width=380, height=48,
            placeholder_text=tr("id_placeholder"),
            font=FONT_INPUT, justify="center",
            corner_radius=12, border_width=1, border_color=SEPARATOR,
            fg_color=PANEL,
        )
        self.appid.pack(pady=6)
        self.appid.bind("<KeyPress>", self.paste_text)

        self.tab1_hint = ctk.CTkLabel(card, text=" ", font=FONT_SMALL,
                                      text_color=DANGER, height=18)
        self.tab1_hint.pack()

        btns = ctk.CTkFrame(card, fg_color="transparent")
        btns.pack(pady=(4, 22))

        ctk.CTkButton(
            btns, text=tr("btn_itunes"),
            font=FONT_BODY_B, height=44, width=220,
            corner_radius=12, command=self.open_itunes,
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            btns, text=tr("btn_appstore"),
            font=FONT_BODY_B, height=44, width=220,
            corner_radius=12,
            fg_color="transparent", border_width=1, border_color=SEPARATOR,
            text_color=ACCENT, hover_color=ACCENT_SOFT,
            command=self.open_browser,
        ).pack(side="left", padx=6)

    def _build_tab2(self):
        center = ctk.CTkFrame(self.tab2, fg_color="transparent")
        center.pack(fill="x", padx=24, pady=(10, 6))

        bar = ctk.CTkFrame(center, fg_color="transparent")
        bar.pack(anchor="center")

        self.search_entry = ctk.CTkEntry(
            bar, placeholder_text=tr("search_placeholder"),
            font=FONT_BODY, height=44, width=480, corner_radius=12,
            border_width=1, border_color=SEPARATOR, fg_color=CARD,
        )
        self.search_entry.pack(side="left", padx=(0, 8))
        self.search_entry.bind("<Return>", lambda e: self.start_search_thread())

        self.country = ctk.CTkComboBox(
            bar, values=ALL_REGIONS,
            width=110, height=44, corner_radius=12, border_width=1,
            border_color=SEPARATOR, fg_color=CARD,
            dropdown_fg_color=PANEL,
            dropdown_hover_color=ACCENT_SOFT,
            dropdown_text_color=TEXT,
            font=FONT_SMALL,
        )
        self.country.set(self.settings.get("region", "ru"))
        self.country.pack(side="left", padx=4)
        self.country.bind("<<ComboboxSelected>>", self._on_region_change)

        self.search_btn = ctk.CTkButton(
            bar, text=tr("btn_search"), width=120, height=44, corner_radius=12,
            font=FONT_BODY_B, command=self.start_search_thread,
        )
        self.search_btn.pack(side="left", padx=(4, 0))

        ctk.CTkLabel(self.tab2, text=tr("region_hint"),
                     font=FONT_TINY, text_color=MUTED).pack(anchor="center", pady=(0, 6))

        self.scroll = ctk.CTkScrollableFrame(self.tab2, corner_radius=16, fg_color=PANEL)
        self.scroll.pack(fill="both", expand=True, padx=24, pady=(0, 10))

        if not self._state["results"]:
            ctk.CTkLabel(
                self.scroll, text=tr("empty_search"),
                font=FONT_BODY, text_color=MUTED, justify="center",
            ).pack(pady=60)

    def _on_region_change(self, event=None):
        self.settings["region"] = self.country.get()
        save_settings(self.settings)

    def _build_tab3(self):
        card = ctk.CTkFrame(self.tab3, corner_radius=20, fg_color=CARD,
                            border_width=1, border_color=SEPARATOR)
        card.pack(pady=20, padx=60, fill="x")

        ctk.CTkLabel(card, text=tr("proxy_title"),
                     font=FONT_TITLE, text_color=TEXT).pack(pady=(22, 4))
        ctk.CTkLabel(card, text=tr("proxy_hint"),
                     font=FONT_SMALL, text_color=MUTED, justify="center").pack(pady=(0, 16))

        btns = ctk.CTkFrame(card, fg_color="transparent")
        btns.pack(pady=4)

        ctk.CTkButton(
            btns, text=tr("btn_proxy_on"),
            font=FONT_BODY_B, height=44, width=200, corner_radius=12,
            fg_color=SUCCESS, hover_color=("#1E8E3E", "#2FB350"),
            command=self.proxy_mode_on,
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            btns, text=tr("btn_proxy_off"),
            font=FONT_BODY_B, height=44, width=200, corner_radius=12,
            fg_color=DANGER, hover_color=("#B00010", "#E0352B"),
            command=self.proxy_mode_off,
        ).pack(side="left", padx=8)

        self.status = ctk.CTkLabel(
            card, text=tr("proxy_stopped"), font=("SF Pro Text", 15, "bold"),
            text_color=DANGER,
        )
        self.status.pack(pady=(14, 2))

        self.proxy_hint = ctk.CTkLabel(card, text=" ", font=FONT_TINY,
                                       text_color=MUTED)
        self.proxy_hint.pack(pady=(0, 20))

    def _build_tab4(self):
        card = ctk.CTkFrame(self.tab4, corner_radius=20, fg_color=CARD,
                            border_width=1, border_color=SEPARATOR)
        card.pack(pady=20, padx=40, fill="x")

        ctk.CTkLabel(card, text=tr("settings_title"),
                     font=FONT_TITLE, text_color=TEXT).pack(pady=(22, 20))

        grid = ctk.CTkFrame(card, fg_color="transparent")
        grid.pack(padx=30, pady=(0, 20), fill="x")
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=0)
        grid.columnconfigure(2, weight=0)

        ctk.CTkLabel(grid, text=tr("settings_lang"), font=FONT_BODY, anchor="w", text_color=TEXT).grid(
            row=0, column=0, sticky="w", pady=(0, 10))

        lang_values = [f"{name} ({code})" for code, name in
                       sorted(ALL_LANGUAGES.items(),
                              key=lambda kv: (kv[0] not in TRANSLATED_LANGS, kv[1]))]

        self.lang_combo = ctk.CTkComboBox(
            grid, values=lang_values, width=260, height=42, corner_radius=10,
            border_width=1, border_color=SEPARATOR, fg_color=PANEL,
            dropdown_fg_color=PANEL, dropdown_hover_color=ACCENT_SOFT,
            dropdown_text_color=TEXT, font=("Segoe UI", 13),
        )
        cur_code = self.settings["lang"]
        cur_name = ALL_LANGUAGES.get(cur_code, cur_code)
        self.lang_combo.set(f"{cur_name} ({cur_code})")
        self.lang_combo.grid(row=0, column=1, padx=(20, 10), pady=(0, 10), sticky="e")

        self.btn_apply = ctk.CTkButton(
            grid, text=tr("settings_apply_lang"), height=42, width=165,
            corner_radius=10, font=("Segoe UI", 12, "bold"),
            fg_color=ACCENT, text_color="#FFFFFF", command=self._apply_language_now,
        )
        self.btn_apply.grid(row=0, column=2, pady=(0, 10), sticky="e")

        ctk.CTkLabel(grid, text=tr("settings_region"), font=FONT_BODY, anchor="w", text_color=TEXT).grid(
            row=2, column=0, sticky="w", pady=10)

        self.region_combo = ctk.CTkComboBox(
            grid, values=ALL_REGIONS, width=260, height=42, corner_radius=10,
            border_width=1, border_color=SEPARATOR, fg_color=PANEL,
            dropdown_fg_color=PANEL, dropdown_hover_color=ACCENT_SOFT,
            dropdown_text_color=TEXT, font=("Segoe UI", 13),
        )
        self.region_combo.set(self.settings["region"])
        self.region_combo.grid(row=2, column=1, padx=(20, 10), pady=10, sticky="e")
        self.region_combo.bind("<<ComboboxSelected>>", self._on_default_region_change)


        ctk.CTkLabel(grid, text=tr("settings_theme"), font=FONT_BODY, anchor="w", text_color=TEXT).grid(
            row=3, column=0, sticky="w", pady=10)

        switch_holder = ctk.CTkFrame(grid, fg_color="transparent")
        switch_holder.grid(row=3, column=1, columnspan=2, sticky="w", padx=(20, 0), pady=10)

        self.settings_theme_switch = ctk.CTkSwitch(
            switch_holder, text="", width=50, progress_color=ACCENT,
            command=self._on_theme_switch_change,
        )
        if self.settings["theme"] == "Dark":
            self.settings_theme_switch.select()
        self.settings_theme_switch.pack(side="left")

    def _apply_language_now(self):
        chosen = self.lang_combo.get()
        code = chosen.rsplit("(", 1)[-1].rstrip(")").strip()
        if code in ALL_LANGUAGES:
            self.settings["lang"] = code
            LANG["value"] = code
            save_settings(self.settings)
            self._rebuild_ui()
            self._set_status(tr("settings_saved"), SUCCESS)

    def _on_default_region_change(self, event=None):
        self.settings["region"] = self.region_combo.get()
        save_settings(self.settings)
        self.country.set(self.settings["region"])
        self._set_status(tr("settings_saved"), SUCCESS)

    def _on_theme_switch_change(self):
        mode = "Dark" if self.settings_theme_switch.get() else "Light"
        ctk.set_appearance_mode(mode)
        self.settings["theme"] = mode
        save_settings(self.settings)

    def _build_statusbar(self):
        sep = ctk.CTkFrame(self._statusbar_frame, height=1, fg_color=SEPARATOR)
        sep.pack(fill="x", pady=(6, 0))
        self.statusbar = ctk.CTkLabel(
            self._statusbar_frame, text=tr("ready"),
            font=FONT_TINY, text_color=MUTED, anchor="center",
        )
        self.statusbar.pack(fill="x", pady=(8, 10))

    def _set_status(self, text, color=None):
        self.statusbar.configure(text=text, text_color=color or MUTED)

    def open_itunes(self):
        app_id = self.appid.get().strip()
        if not app_id:
            self.tab1_hint.configure(text=tr("status_no_id"))
            return
        if not app_id.isdigit():
            self.tab1_hint.configure(text=tr("status_bad_id"))
            return
        self.tab1_hint.configure(text=" ")
        webbrowser.open(f"itmss://itunes.apple.com/app/id{app_id}")
        self._set_status(f"{tr('btn_itunes')}: {app_id}", ACCENT)

    def open_browser(self):
        webbrowser.open("https://apps.apple.com")
        self._set_status(tr("btn_appstore"), ACCENT)

    def start_search_thread(self):
        threading.Thread(target=self.search, daemon=True).start()

    def search(self):
        query = self.search_entry.get().strip()
        country = self.country.get()
        if not query:
            self._set_status(tr("status_empty_q"), DANGER)
            return

        self.search_btn.configure(state="disabled", text="⏳…")
        self._set_status(tr("status_searching", q=query, c=country), ACCENT)

        params = {"term": query, "country": country, "entity": "software", "limit": 20}
        try:
            r = requests.get("https://itunes.apple.com/search", params=params, timeout=8)
            data = r.json()
        except Exception:
            self.search_btn.configure(state="normal", text=tr("btn_search"))
            self._set_status(tr("status_net_err"), DANGER)
            return

        for w in self.scroll.winfo_children():
            w.destroy()

        results = data.get("results", [])
        self._state["results"] = results

        if not results:
            ctk.CTkLabel(
                self.scroll, text=tr("empty_none"),
                font=FONT_BODY, text_color=MUTED, justify="center",
            ).pack(pady=60)
            self._set_status(tr("status_not_found", q=query), DANGER)
        else:
            for app in results:
                self._make_result_card(app)
            self._set_status(tr("status_found", n=len(results)), SUCCESS)

        self.search_btn.configure(state="normal", text=tr("btn_search"))

    def _make_result_card(self, app):
        frame = ctk.CTkFrame(
            self.scroll, corner_radius=14, fg_color=CARD,
            border_width=1, border_color=SEPARATOR,
        )
        frame.pack(fill="x", pady=5, padx=4)

        icon_url = app.get("artworkUrl100")
        img_label = ctk.CTkLabel(frame, text="")
        img_label.pack(side="left", padx=(12, 10), pady=10)
        try:
            img_data = requests.get(icon_url, timeout=3).content
            img = Image.open(io.BytesIO(img_data))
            photo = ctk.CTkImage(light_image=img, dark_image=img, size=(56, 56))
            img_label.configure(image=photo)
            img_label.image = photo
        except Exception:
            img_label.configure(text="🖼", font=FONT_TITLE)

        text_frame = ctk.CTkFrame(frame, fg_color="transparent")
        text_frame.pack(side="left", padx=4, pady=10, fill="x", expand=True)

        ctk.CTkLabel(
            text_frame, text=app.get("trackName", "Unknown"),
            font=("SF Pro Text", 15, "bold"), text_color=TEXT, anchor="w",
        ).pack(anchor="w", fill="x")
        ctk.CTkLabel(
            text_frame,
            text=f"{app.get('sellerName','')}   ·   ID: {app.get('trackId','')}",
            font=FONT_SMALL, text_color=MUTED, anchor="w",
        ).pack(anchor="w", fill="x")

        ctk.CTkButton(
            frame, text=tr("open"), width=96, height=34, corner_radius=10,
            font=("SF Pro Text", 13, "bold"),
            command=lambda i=app.get("trackId"): webbrowser.open(
                f"itmss://itunes.apple.com/app/id{i}"),
        ).pack(side="right", padx=(0, 10), pady=10)

        ctk.CTkButton(
            frame, text=tr("copy_id"), width=120, height=34, corner_radius=10,
            fg_color="transparent", border_width=1, border_color=SEPARATOR,
            text_color=ACCENT, hover_color=ACCENT_SOFT,
            font=FONT_SMALL,
            command=lambda i=app.get("trackId"): self._copy_with_feedback(i),
        ).pack(side="right", padx=4, pady=10)

    def _copy_with_feedback(self, text):
        self.copy(text)
        self._set_status(tr("status_copied", i=text), SUCCESS)

    def proxy_mode_on(self):
        try:
            os.startfile("Proxy.exe")
            self._state["proxy_status"] = "running"
            self.status.configure(text=tr("proxy_running"), text_color=SUCCESS)
            self.proxy_hint.configure(text=tr("hint_proxy_running"), text_color=MUTED)
            self._set_status(tr("status_proxy_on"), SUCCESS)
        except FileNotFoundError:
            self._state["proxy_status"] = "missing"
            self.status.configure(text=tr("proxy_not_found"), text_color=DANGER)
            self.proxy_hint.configure(text=tr("hint_proxy_missing"), text_color=DANGER)
            self._set_status(tr("status_proxy_missing"), DANGER)

    def proxy_mode_off(self):
        try:
            os.system("taskkill /F /IM Proxy.exe >nul 2>&1")
            self._state["proxy_status"] = "stopped"
            self.status.configure(text=tr("proxy_stopped"), text_color=DANGER)
            self.proxy_hint.configure(text=" ", text_color=MUTED)
            self._set_status(tr("status_proxy_off"), MUTED)
        except Exception as e:
            self._set_status(str(e), DANGER)

    def copy(self, text):
        self.clipboard_clear()
        self.clipboard_append(str(text))

    def paste_text(self, event):
        if event.state & 0x4:
            try:
                self.appid.insert("insert", self.clipboard_get())
            except Exception:
                pass
            return "break"


if __name__ == "__main__":
    App().mainloop()