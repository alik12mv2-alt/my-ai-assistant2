import json
import os
import urllib.request
import urllib.error

MAX_HISTORY_MESSAGES = 20
HISTORY_FILE = 'chat_history.json'


def load_env(path='.env'):
    if not os.path.exists(path):
        return
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            os.environ.setdefault(key.strip(), value.strip())


def history_enabled():
    return os.getenv('SAVE_HISTORY', 'false').strip().lower() in ('1', 'true', 'yes', 'on')


def load_history(system_message):
    if not history_enabled() or not os.path.exists(HISTORY_FILE):
        return [system_message]
    try:
        with open(HISTORY_FILE, encoding='utf-8') as f:
            saved = json.load(f)
        if isinstance(saved, list):
            valid = [m for m in saved if isinstance(m, dict) and m.get('role') in ('user', 'assistant') and isinstance(m.get('content'), str)]
            return [system_message] + valid[-MAX_HISTORY_MESSAGES:]
    except (OSError, ValueError):
        print('فایل تاریخچه خوانده نشد؛ گفتگوی تازه آغاز می‌شود.')
    return [system_message]


def save_history(messages):
    if not history_enabled():
        return
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(messages[-MAX_HISTORY_MESSAGES:], f, ensure_ascii=False, indent=2)
    except OSError:
        print('ذخیره تاریخچه انجام نشد.')


def ask_api(messages):
    api_key = os.getenv('API_KEY', '').strip()
    base_url = os.getenv('API_BASE_URL', 'https://api.openai.com/v1').rstrip('/')
    model = os.getenv('MODEL', 'gpt-4o-mini')
    if not api_key or api_key == 'put_your_api_key_here':
        print('تنظیم API_KEY در فایل .env ضروری است.')
        return None

    payload = json.dumps({
        'model': model,
        'messages': messages,
        'temperature': 0.7
    }).encode('utf-8')
    req = urllib.request.Request(
        f'{base_url}/chat/completions',
        data=payload,
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        },
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            data = json.loads(response.read().decode('utf-8'))
        return data['choices'][0]['message']['content']
    except urllib.error.HTTPError as e:
        print(f'خطای API: HTTP {e.code}')
    except urllib.error.URLError:
        print('اتصال به API ناموفق بود. اینترنت یا API_BASE_URL را بررسی کنید.')
    except (KeyError, ValueError, TimeoutError):
        print('پاسخ سرویس قابل پردازش نبود.')
    return None


def show_help():
    print('''\nفرمان‌های دستیار:
  help   نمایش راهنما
  reset  پاک کردن تاریخچه گفتگو
  exit   خروج از برنامه
''')


def main():
    load_env()
    print('دستیار فارسی آماده است. برای راهنما help را وارد کنید.')
    if history_enabled():
        print('ذخیره تاریخچه فعال است؛ گفتگوها روی دستگاه ذخیره می‌شوند.')
    else:
        print('ذخیره تاریخچه خاموش است؛ گفتگو پس از خروج نگهداری نمی‌شود.')

    system_message = {
        'role': 'system',
        'content': (
            'You are a helpful, clear assistant. Reply in Persian unless the user '
            'uses another language. Explain uncertainty and do not invent facts.'
        )
    }
    messages = load_history(system_message)

    while True:
        try:
            user_text = input('\nشما: ').strip()
        except (KeyboardInterrupt, EOFError):
            print('\nخدانگهدار!')
            break

        if not user_text:
            continue
        command = user_text.lower()
        if command in ('exit', 'quit'):
            print('خدانگهدار!')
            break
        if command == 'help':
            show_help()
            continue
        if command == 'reset':
            messages = [system_message]
            if history_enabled():
                try:
                    if os.path.exists(HISTORY_FILE):
                        os.remove(HISTORY_FILE)
                except OSError:
                    print('حذف فایل تاریخچه ناموفق بود.')
            print('تاریخچه گفتگو پاک شد.')
            continue

        messages.append({'role': 'user', 'content': user_text})
        reply = ask_api(messages)
        if reply:
            print(f'\nدستیار: {reply}')
            messages.append({'role': 'assistant', 'content': reply})
            messages = [system_message] + messages[-MAX_HISTORY_MESSAGES:]
            save_history(messages[1:])
        else:
            messages.pop()


if __name__ == '__main__':
    main()
