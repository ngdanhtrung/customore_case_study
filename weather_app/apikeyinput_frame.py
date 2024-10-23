import tkinter as tk
from tkinter import ttk
import sqlite3



class APIKeyInputFrame(tk.Frame):
  def __init__(self, parent):
    super().__init__(parent)
    self.label = ttk.Label(self, text="Enter API Key:")
    self.label.pack()
    self.entry = ttk.Entry(self, width=40)
    api_key = self.get_api_key()
    if api_key:
      self.entry.insert(0, api_key)
    self.entry.pack()
    self.button = ttk.Button(self, text="Save", command=self.save_api_key)
    self.button.pack()

  def save_api_key(self):
    api_key = self.entry.get()
    conn = sqlite3.connect("weather.db")
    c = conn.cursor()
    c.execute("DELETE FROM api_keys")
    c.execute("INSERT INTO api_keys VALUES (?)", (api_key,))
    conn.commit()
    conn.close()

  def get_api_key(self):
    conn = sqlite3.connect("weather.db")
    c = conn.cursor()
    c.execute("SELECT key FROM api_keys")
    api_key = c.fetchone()
    conn.close()
    return api_key[0] if api_key else None