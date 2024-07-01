# Yaga Scraper

This is a web scraper that scrapes the [Yaga](https://www.yaga.ee) website. Yaga is an Estonian marketplace where people can sell their second-hand clothes and other preloved items. This program works by scraping the website with the user's search terms and filters. It runs at intervals chosen by the user. When a new item is found by the scraper that isn't already in the database, the user receives an email notification.

## Config File

In the `config.cfg` file, you can change options and input information for the program to work.

- **base_url** - This is the base URL for the web scraper (by default it is https://www.yaga.ee).
- **term** - The search term for the item (e.g., "iPhone 15 case").
- **min_price** - The minimum price of the item (By default 0).
- **max_price** - The maximum price of the item (by default 1000).
- **brand** - The brand of the item; the spelling must be correct. You can leave this field empty if you do not want to search for any specific brands.
- **sender_email** - The Gmail account from which emails are sent.
- **sender_pass** - The Google app password required for the sender email account.
- **recipient_email** - The email account to which emails are sent.
- **max_items** - The maximum number of items the scraper will scrape in one run. This setting can prevent scraping too many items to avoid overfilling the database and to decrease scraping time. (By default, it is 500).
- **interval_minutes** - The frequency at which the web scraper runs and checks for new items, in minutes (By default, 60).

## Setup

- Install all dependencies from the `requirements.txt` file.
- Have 2FA enabled for the Gmail account from where the emails will be sent to acquire a Google app password. This password must be entered into the `.cfg` file for the email sender to work. [Click here for a short guide on how to create an app password](https://knowledge.workspace.google.com/kb/how-to-create-app-passwords-000009237).
- Run the `gui.py` file to get a Tkinter GUI where you can input your scraper settings. The program saves these settings to the `.cfg` file and runs in the background. Alternatively, run the `scraper.py` file without the GUI, using settings already configured in the `.cfg` file.
- Let the script run in the background.
