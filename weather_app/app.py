import tkinter as tk
from tkinter import ttk
import sqlite3

from apikeyinput_frame import APIKeyInputFrame
from main_frame import MainFrame
    
class Application(tk.Tk):
  def __init__(self):
    super().__init__()
    self.title("Weather App")
    self.geometry("400x720")
    self.notebook = ttk.Notebook(self)
    self.create_database()

    self.api_key_frame = APIKeyInputFrame(self.notebook)
    self.notebook.add(self.api_key_frame, text="API key")

    self.main_frame = MainFrame(self.notebook)
    self.notebook.add(self.main_frame, text="Main")

    self.notebook.pack(expand=True, fill="both")

  def create_database(self):
    conn = sqlite3.connect("weather.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS api_keys (key TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS weather_data (city TEXT, temperature REAL, humidity REAL, pressure REAL, weather TEXT)")
    
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='worldcities'")
    table_exists = c.fetchone()

    if not table_exists:
      c.execute("CREATE TABLE IF NOT EXISTS worldcities (city TEXT, city_ascii TEXT, lat REAL, lng REAL)")
      with open("seed/worldcities.csv", "r", encoding="utf8") as file:
        csv_data = file.readlines()
      cities_data = [line.strip().split(",") for line in csv_data[1:]]
      c.executemany("INSERT INTO worldcities VALUES (?, ?, ?, ?)", cities_data)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
  app = Application()
  app.mainloop()