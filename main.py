import json
import os
import urllib.request
import urllib.error


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
        print('لطفاً API_KEY را در فایل .env تنظیم کنید.')
        return None
    payload = json.dumps({'model': model, 'messages': messages}).encode('utf-8')
    req = urllib.request.Request(
        f'{base_url}/chat/completions', data=payload,
        headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            data = json.loads(response.read().decode('utf-8'))
        return data['choices'][0]['message']['content']
    except urllib.error.HTTPError as e:
        print(f'خطای API: HTTP {e.code}')
    except urllib.error.URLError:
        print('ارتباط با API برقرار نشد؛ اتصال اینترنت و آدرس API را بررسی کنید.')
    except (KeyError, ValueError, TimeoutError):
        print('پاسخ API قابل پردازش نبود.')
    return None


def main():
    load_env()
    print('دستیار هوش مصنوعی آماده است. برای خروج exit و برای پاک کردن گفتگو reset را وارد کنید.')
    messages = [{'role': 'system', 'content': 'You are a helpful, clear assistant. Reply in Persian unless the user uses another language.'}]
    while True:
        try:
            user_text = input('\nشما: ').strip()
        except (KeyboardInterrupt, EOFError):
            print('\nخدانگهدار!')
            break
        if not user_text:
            continue
        if user_text.lower() in ('exit', 'quit'):
            print('خدانگهدار!')
            break
        if user_text.lower() == 'reset':
            messages = messages[:1]
            print('تاریخچه پاک شد.')
            continue
        messages.append({'role': 'user', 'content': user_text})
        reply = ask_api(messages)
        if reply:
            print(f'\nدستیار: {reply}')
            messages.append({'role': 'assistant', 'content': reply})
        else:
            messages.pop()


if __name__ == '__main__':
    main()
