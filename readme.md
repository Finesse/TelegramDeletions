# Telegram Deletions

A simple CLI application to save messages deleted in specific Telegram chats.

How it works:
1. The app signs-in to Telegram behalf your account
2. The app watches all incoming messages in selected dialogs and saves them to disk
3. When a saved message is deleted, the app posts the message to another chat

The script can't restore messages posted or deleted when it didn't run.
So you should always keep it running, ideally on a server.

## Installation

Requirements:
- Python version 3.10 or newer
- A Telegram account
- Git (optional)

Download the code and install the dependencies:

```bash
git clone --depth 1 git@github.com:Finesse/WordleSolver.git telegram_deletions
cd telegram_deletions
python3 -m venv .venv
source ./.venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
cp .env.example .env
```

Get a Telegram application credentials from https://my.telegram.org, under API Development.
Or from https://tjhorner.dev/webogram/#/login.

Configure the app by editing the `.env` file (or provide the environment variable any other way):

- `TELEGRAM_APP_ID` — the application id
- `TELEGRAM_APP_HASH` — the application hash
- `APP_DATA_DIRECTORY` (optional) — path to the directory to store data (cookie, messages) at.
  The running application must have permissions to read and write there.
  The default it `data`.
- Ignore the chat options for now

List your dialogs to see their ids by running:

```bash
python3 src/list_dialogs.py
```

When you run it the first time, it will ask your credentials to sign in.

Configure `.env` again:

- `APP_CHATS_TO_WATCH` — id of the chat(s) to watch (integer).
    If multiple, must be separated by `,`.
    You can find them after `Chat id:` in the dialog list.
- `APP_CHAT_TO_OUTPUT` — input entity of the chat to post deleted messages (Python function call string).
    Copy the part after `Input entity:` in the dialog list.

## Usage

Run the app:

```bash
python3 src/watch_deletions.py
```

Keep it running. Press <kbd>Ctrl</kbd>+<kbd>C</kbd> to stop watching.

> [!WARNING]  
> The app never deletes messages from the data directory.
> You should remove them manually; it's ok to delete any message when the app is running. 

## Running as daemon

This section tells how to configure the app as a Linux service so that the app always runs.

Connect to the server via SSH as a regular user.
It must have sudo access for a single command.
Install and configure the app following the above steps.
Make sure you've called `python3 src/list_dialogs.py` on the server,
otherwise the service will stuck on the Telegram sign-in dialog.

> [!IMPORTANT]  
> The following steps assume the app directory is `~/telegram_deletions`.
> If it's false in your case, adjust the commands accordingly.

Run on the server:

```bash
sudo loginctl enable-linger "$USER"

mkdir -p ~/.config/systemd/user
ln -s ~/telegram_deletions/telegram_deletions.service ~/.config/systemd/user/telegram_deletions.service
systemctl --user daemon-reload
systemctl --user enable telegram_deletions
systemctl --user start telegram_deletions
```

Check the logs to make sure it works:

```bash
journalctl --user -u telegram_deletions
```

If you want to stop and unregister the service:

```bash
systemctl --user stop telegram_deletions
systemctl --user disable telegram_deletions
```
