import json
import os
import urllib.request
import urllib.error

MAX_HISTORY_MESSAGES = 20


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
  reset  پاک کردن تاریخچه همین جلسه
  exit   خروج از برنامه
''')


def main():
    load_env()
    print('دستیار فارسی آماده است. برای راهنما help را وارد کنید.')
    system_message = {
        'role': 'system',
        'content': (
            'You are a helpful, clear assistant. Reply in Persian unless the user '
            'uses another language. Explain uncertainty and do not invent facts.'
        )
    }
    messages = [system_message]

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
            print('تاریخچه این جلسه پاک شد.')
            continue

        messages.append({'role': 'user', 'content': user_text})
        reply = ask_api(messages)
        if reply:
            print(f'\nدستیار: {reply}')
            messages.append({'role': 'assistant', 'content': reply})
            # Keep recent context to limit token usage.
            messages = [system_message] + messages[-MAX_HISTORY_MESSAGES:]
        else:
            messages.pop()


if __name__ == '__main__':
    main()
