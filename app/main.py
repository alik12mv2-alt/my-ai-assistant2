import json
import threading
import urllib.request
import urllib.error
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

KV = '''
BoxLayout:
    orientation: 'vertical'
    padding: '12dp'
    spacing: '8dp'
    Label:
        text: 'دستیار هوش مصنوعی'
        size_hint_y: None
        height: '42dp'
        font_size: '22sp'
    TextInput:
        id: api_key
        hint_text: 'کلید API را وارد کنید (فقط روی دستگاه)'
        password: True
        multiline: False
        size_hint_y: None
        height: '48dp'
    TextInput:
        id: base_url
        text: 'https://api.openai.com/v1'
        hint_text: 'آدرس API'
        multiline: False
        size_hint_y: None
        height: '42dp'
    TextInput:
        id: model
        text: 'gpt-4o-mini'
        hint_text: 'مدل'
        multiline: False
        size_hint_y: None
        height: '42dp'
    TextInput:
        id: chat
        text: 'سلام! پیام خود را بنویسید.\\n'
        readonly: True
        size_hint_y: 1
    TextInput:
        id: prompt
        hint_text: 'پیام شما...'
        size_hint_y: None
        height: '90dp'
    Button:
        text: 'ارسال'
        size_hint_y: None
        height: '48dp'
        on_release: app.send_message()
    Label:
        id: status
        text: 'کلید API را داخل برنامه وارد کنید.'
        size_hint_y: None
        height: '28dp'
'''

class ChatApp(App):
    def build(self):
        self.messages = [{"role": "system", "content": "You are a helpful assistant. Reply in Persian unless the user uses another language."}]
        self.root = Builder.load_string(KV)
        return self.root

    def send_message(self):
        ui = self.root.ids
        key = ui.api_key.text.strip()
        prompt = ui.prompt.text.strip()
        if not key:
            ui.status.text = "ابتدا کلید API را وارد کنید."
            return
        if not prompt:
            return
        base = ui.base_url.text.strip().rstrip("/")
        model = ui.model.text.strip()
        self.messages.append({"role": "user", "content": prompt})
        ui.chat.text += "\\nشما: " + prompt + "\\n"
        ui.prompt.text = ""
        ui.status.text = "در حال دریافت پاسخ..."
        threading.Thread(target=self._request, args=(key, base, model), daemon=True).start()

    def _request(self, key, base, model):
        try:
            payload = json.dumps({"model": model, "messages": self.messages[-20:], "temperature": 0.7}).encode()
            req = urllib.request.Request(base + "/chat/completions", data=payload, headers={"Content-Type": "application/json", "Authorization": "Bearer " + key})
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode())
            answer = data["choices"][0]["message"]["content"]
            self.messages.append({"role": "assistant", "content": answer})
            Clock.schedule_once(lambda dt: self._show_answer(answer), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self._show_error(str(e)), 0)

    def _show_answer(self, answer):
        self.root.ids.chat.text += "دستیار: " + answer + "\\n\\n"
        self.root.ids.status.text = "آماده"
    def _show_error(self, error):
        self.root.ids.status.text = "خطا: " + error[:180]

ChatApp().run()
