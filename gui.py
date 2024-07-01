import tkinter as tk
from tkinter import messagebox, ttk
from config import Config
from scraper import Scraper
from database import DatabaseManager


class Gui:
    def __init__(self, master):
        self.master = master
        self.master.title("Yaga Scraper")
        self.config = Config()
        self.db_manager = DatabaseManager()
        self.create_widgets()

    def create_widgets(self):
        """
        Create the main window
        """
        self.base_url_label = ttk.Label(self.master, text="Base URL:")
        self.base_url_entry = ttk.Entry(self.master, width=50)
        self.base_url_entry.insert(0, self.config.get('yaga', 'base_url'))
        self.base_url_label.grid(row=0, column=0, sticky=tk.W)
        self.base_url_entry.grid(row=0, column=1, padx=10, pady=5)

        self.term_label = ttk.Label(self.master, text="Search term:")
        self.term_entry = ttk.Entry(self.master, width=50)
        self.term_entry.insert(0, self.config.get('yaga', 'term'))
        self.term_label.grid(row=1, column=0, sticky=tk.W)
        self.term_entry.grid(row=1, column=1, padx=10, pady=5)

        self.min_price_label = ttk.Label(self.master, text="Min Price:")
        self.min_price_entry = ttk.Entry(self.master, width=50)
        self.min_price_entry.insert(0, self.config.get('yaga', 'min_price'))
        self.min_price_label.grid(row=2, column=0, sticky=tk.W)
        self.min_price_entry.grid(row=2, column=1, padx=10, pady=5)

        self.max_price_label = ttk.Label(self.master, text="Max Price:")
        self.max_price_entry = ttk.Entry(self.master, width=50)
        self.max_price_entry.insert(0, self.config.get('yaga', 'max_price'))
        self.max_price_label.grid(row=3, column=0, sticky=tk.W)
        self.max_price_entry.grid(row=3, column=1, padx=10, pady=5)

        self.brand_label = ttk.Label(self.master, text="Brand:")
        self.brand_entry = ttk.Entry(self.master, width=50)
        self.brand_entry.insert(0, self.config.get('yaga', 'brand'))
        self.brand_label.grid(row=4, column=0, sticky=tk.W)
        self.brand_entry.grid(row=4, column=1, padx=10, pady=5)

        self.sender_email_label = ttk.Label(self.master, text="Sender Email:")
        self.sender_email_entry = ttk.Entry(self.master, width=50)
        self.sender_email_entry.insert(0, self.config.get('email', 'sender_email'))
        self.sender_email_label.grid(row=5, column=0, sticky=tk.W)
        self.sender_email_entry.grid(row=5, column=1, padx=10, pady=5)

        self.sender_pass_label = ttk.Label(self.master, text="Sender Password:")
        self.sender_pass_entry = ttk.Entry(self.master, width=50, show='*')
        self.sender_pass_entry.insert(0, self.config.get('email', 'sender_pass'))
        self.sender_pass_label.grid(row=6, column=0, sticky=tk.W)
        self.sender_pass_entry.grid(row=6, column=1, padx=10, pady=5)

        self.recipient_email_label = ttk.Label(self.master, text="Recipient Email:")
        self.recipient_email_entry = ttk.Entry(self.master, width=50)
        self.recipient_email_entry.insert(0, self.config.get('email', 'recipient_email'))
        self.recipient_email_label.grid(row=7, column=0, sticky=tk.W)
        self.recipient_email_entry.grid(row=7, column=1, padx=10, pady=5)

        self.interval_label = ttk.Label(self.master, text="Interval (minutes):")
        self.interval_entry = ttk.Entry(self.master, width=50)
        self.interval_entry.insert(0, self.config.get('general', 'interval_minutes'))
        self.interval_label.grid(row=8, column=0, sticky=tk.W)
        self.interval_entry.grid(row=8, column=1, padx=10, pady=5)

        self.max_items_label = ttk.Label(self.master, text="Max Items:")
        self.max_items_entry = ttk.Entry(self.master, width=50)
        self.max_items_entry.insert(0, self.config.get('general', 'max_items'))
        self.max_items_label.grid(row=9, column=0, sticky=tk.W)
        self.max_items_entry.grid(row=9, column=1, padx=10, pady=5)

        self.run_button = ttk.Button(self.master, text="Run", command=self.save_and_run)
        self.run_button.grid(row=10, columnspan=2, pady=10)

        self.clear_db_button = ttk.Button(self.master, text="Clear Database", command=self.clear_database)
        self.clear_db_button.grid(row=11, columnspan=2, pady=10)

    def save_and_run(self):
        """
        Save inserted configurations to config file and run the scraper.
        """
        try:
            self.config.set('yaga', 'base_url', self.base_url_entry.get())
            self.config.set('yaga', 'term', self.term_entry.get())
            self.config.set('yaga', 'min_price', self.min_price_entry.get())
            self.config.set('yaga', 'max_price', self.max_price_entry.get())
            self.config.set('yaga', 'brand', self.brand_entry.get())

            self.config.set('email', 'sender_email', self.sender_email_entry.get())
            self.config.set('email', 'sender_pass', self.sender_pass_entry.get())
            self.config.set('email', 'recipient_email', self.recipient_email_entry.get())

            self.config.set('general', 'interval_minutes', self.interval_entry.get())
            self.config.set('general', 'max_items', self.max_items_entry.get())
            self.config.save_config()
            self.master.destroy()
            scraper = Scraper()
            scraper.run()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configurations: {e}")

    def clear_database(self):
        """
        Clear the database
        """
        try:
            self.db_manager.clear_database()
            messagebox.showinfo("Success", "Database cleared successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear database: {e}")


def main():
    root = tk.Tk()
    app = Gui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
