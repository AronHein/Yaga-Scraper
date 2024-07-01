import configparser
from urllib.parse import quote


class Config:
    def __init__(self, config_file='config.cfg'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        """
        Loads the config file
        """
        self.config.read(self.config_file, encoding='utf-8')

    def save_config(self):
        """
        Save the config file
        """
        with open(self.config_file, 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)

    def get(self, section, option):
        """
        Get an option from the config file
        """
        return self.config.get(section, option)

    def set(self, section, option, value):
        """
        Set an option in the config file
        """
        self.config.set(section, option, value)

    def get_yaga_config(self):
        """
        Get the search filters and the base url from the config file
        """
        base_url = self.config['yaga']['base_url']
        term = quote(self.config['yaga']['term'])
        min_price = int(self.config['yaga']['min_price'])
        max_price = int(self.config['yaga']['max_price'])
        brand = quote(self.config['yaga']['brand'])
        return base_url, term, min_price, max_price, brand

    def get_email_config(self):
        """
        Get the email information from the config file
        """
        sender_email = self.config['email']['sender_email']
        sender_pass = self.config['email']['sender_pass']
        recipient_email = self.config['email']['recipient_email']
        return sender_email, sender_pass, recipient_email

    def get_schedule_interval(self):
        """
        Get the interval from config file which determines how often the program should run and scrape the website
        """
        return int(self.config['general']['interval_minutes'])

    def get_max_items(self):
        """
        Get the maximum number of items from config file to scrape so that the scraper does not run endlessly
        if the search filter is too narrow
        """
        return int(self.config['general']['max_items'])

    def get_url(self):
        """
        Get the url of the website to scrape
        """
        base_url, term, min_price, max_price, brand = self.get_yaga_config()
        if term and brand and (min_price < max_price):
            return f"{base_url}/brand/{brand}?query={term}&price=%7B\"min\"%3A{min_price}%2C\"max\"%3A{max_price}%7D"
        elif term and brand:
            return f"{base_url}/brand/{brand}?query={term}"
        elif term and (min_price < max_price):
            return f"{base_url}/otsi/{term}?price=%7B\"min\"%3A{min_price}%2C\"max\"%3A{max_price}%7D"
        elif term:
            return f"{base_url}/otsi/{term}"
        else:
            print("Can't get url")
