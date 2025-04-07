# Steam Deck Watcher for Raspberry Pi

This project checks the availability of [refurbished Steam Decks](https://store.steampowered.com/sale/steamdeckrefurbished/) using the Steam API and sends notifications via a Telegram bot when a status change is detected. The script is designed to run on a Raspberry Pi (recommended Raspberry Pi OS Lite) and uses a Python virtual environment for dependency management.

## How It Works

**Environment Variables:**  
 The script reads the Telegram bot token and chat ID from a `.env` file using the `python-dotenv` package. This ensures that sensitive data is not stored in the code or public repository.

**Steam API Check:**  
 The script uses the Steam API to check the availability for various Steam Deck models (64GB, 256GB, 512GB LCD, 512GB OLED, and 1TB OLED). For each version, it stores the last known status in a file (e.g., `903905.status`).

- If the current status differs from the stored one, the script sends a notification via the Telegram bot.
- It logs every check and status change to a local file called `steam_check.log`.

**Logging:**  
 The script writes log entries (including timestamps) to both the console and the `steam_check.log` file.

## Installation on Raspberry Pi (Raspberry Pi OS Lite)

Follow these steps to install and run the script on your Raspberry Pi running Raspberry Pi OS Lite.

### 1. Install Raspberry Pi OS Lite

- **Download:** Get the [Raspberry Pi OS Lite](https://www.raspberrypi.com/software/operating-systems/) image.
- **Flash:** Use the Raspberry Pi Imager to write the image to your SD card.
- **Setup:** Insert the SD card into your Pi, connect it to Ethernet (and optionally a monitor, keyboard, and mouse), and boot it up.

### 2. Connect via SSH (Optional)

If you prefer to work remotely, you can enable SSH during the setup process in the Raspberry Pi Imager.  
Be sure to also set a username and password so you can log in via SSH later with:

```bash
ssh <your_username>@<raspberry_pi_ip_address>
```

### 3. Install Git on the Pi

If Git is not already installed, install it with:

```bash
sudo apt update
sudo apt install git -y
```

### 4. Clone the Repository

Clone the project repository to the Pi:

```bash
git clone https://github.com/ScaxCodes/steam-deck-watcher-pi.git
cd steam-deck-watcher-pi
```

### 5. Create and Activate a Python Virtual Environment

A virtual environment isolates your project’s dependencies from the system packages. This is important to avoid conflicts and keep your system stable.

5.1. Create the virtual environment:

```bash
python3 -m venv venv
```

5.2. Activate the virtual environment:

```bash
source venv/bin/activate
```

You should see (venv) at the beginning of your terminal prompt.

### 6. Install Python Dependencies

Within the activated virtual environment, install the required Python packages:

```bash
pip install requests python-dotenv
```

### 7. Configure Environment Variables

Create a .env file in the project directory. You can use nano to edit the file:

```bash
nano .env
```

Then write or copy and paste via SSH the following (replace with your actual values):

```ini
BOT_TOKEN=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id
```

Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

### 8. Test the Script

Run the script to ensure everything works:

```bash
python3 steamdeck_notifier.py
```

Check the console output and the generated steam_check.log file to verify that the script runs correctly.

### 9. Set Up a Cron Job

To run the script every minute, add a cron job, so even if the Raspberry Pi restarts or you disconnect from SSH, the script continues to run. Open your crontab:

```bash
crontab -e
```

Add the following line (replace <YOUR_USERNAME> with your actual username):

```cron
* * * * * cd /home/<YOUR_USERNAME>/steam-deck-watcher-pi && /home/<YOUR_USERNAME>/steam-deck-watcher-pi/venv/bin/python3 steamdeck_notifier.py
```

This cron job will run the script every minute. Even after reboots or SSH disconnections, it will keep working.

## Additional Resources

To learn how to set up a Telegram bot and get an API key, check out the [Telegram Bot Tutorial](https://core.telegram.org/bots/tutorial).
