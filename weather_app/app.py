import tkinter as tk
from tkinter import ttk
import sqlite3
import aiohttp
import asyncio

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

class MainFrame(tk.Frame):
  def __init__(self, parent):
    super().__init__(parent)
    self.openweather_url = "https://api.openweathermap.org/data/2.5/weather"

    self.label = ttk.Label(self, text="First boudary point", font=("TkDefaultFont", 12, "bold"))
    self.label.grid(row=0, column=0, sticky="w")

    self.xlat_label = ttk.Label(self, text="Latitude:")
    self.xlat_label.grid(row=1, column=0, sticky="w")
    self.xlat_entry = ttk.Entry(self)
    self.xlat_entry.grid(row=1, column=1)

    self.xlng_label = ttk.Label(self, text="Longitude:")
    self.xlng_label.grid(row=2, column=0, sticky="w")
    self.xlng_entry = ttk.Entry(self)
    self.xlng_entry.grid(row=2, column=1)

    self.label = ttk.Label(self, text="Second boudary point", font=("TkDefaultFont", 12, "bold"))
    self.label.grid(row=3, column=0, sticky="w")

    self.ylat_label = ttk.Label(self, text="Latitude:")
    self.ylat_label.grid(row=4, column=0, sticky="w")
    self.ylat_entry = ttk.Entry(self)
    self.ylat_entry.grid(row=4, column=1)

    self.ylng_label = ttk.Label(self, text="Longitude:")
    self.ylng_label.grid(row=5, column=0, sticky="w")
    self.ylng_entry = ttk.Entry(self)
    self.ylng_entry.grid(row=5, column=1)

    self.button = ttk.Button(self, text="Get Weather", command=self.get_weather)
    self.button.grid(row=6, column=0, columnspan=2)

    self.output_cities_label = ttk.Label(self, text="Cities:")
    self.output_cities_label.grid(row=7, column=0, sticky="w")
    self.output_cities = tk.Text(self, height=10, width=40)
    self.output_cities.insert(tk.END, "Output cities will be displayed here")
    self.output_cities.grid(row=8, column=0, columnspan=2)

    self.output_weather_label = ttk.Label(self, text="Weather:")
    self.output_weather_label.grid(row=9, column=0, sticky="w")
    self.output_weather = tk.Text(self, height=10, width=40)
    self.output_weather.insert(tk.END, "Output weather will be displayed here")

  def get_api_key(self):
    conn = sqlite3.connect("weather.db")
    c = conn.cursor()
    c.execute("SELECT key FROM api_keys")
    api_key = c.fetchone()
    conn.close()
    return api_key[0] if api_key else None

  def get_weather(self):
    xlat = self.xlat_entry.get()
    xlng = self.xlng_entry.get()
    ylat = self.ylat_entry.get()
    ylng = self.ylng_entry.get()

    print(f"First point: {xlat}, {xlng}")
    print(f"Second point: {ylat}, {ylng}")

    cities = self.get_cities(xlat, xlng, ylat, ylng)
    self.output_cities.delete("1.0", tk.END)
    for city in cities:
      self.output_cities.insert(tk.END, f"{city[0]}: {city[1]}, {city[2]}\n")

    api_key = self.get_api_key()
    print(api_key)

    loop = asyncio.get_event_loop()
    weather_data = loop.run_until_complete(self.get_weather_data(cities, api_key))
    print(weather_data)
    self.output_weather.delete("1.0", tk.END)
    for data in weather_data:
      if "error" in data:
        self.output_weather.insert(tk.END, f"Error fetching data for {data['city']}: {data['error']}\n")
      else:
        self.output_weather.insert(tk.END, f"Weather for {data['name']}:\n")
        self.output_weather.insert(tk.END, f"Temperature: {data['main']['temp']}\n")
        self.output_weather.insert(tk.END, f"Humidity: {data['main']['humidity']}\n")
        self.output_weather.insert(tk.END, f"Pressure: {data['main']['pressure']}\n")
        self.output_weather.insert(tk.END, f"Weather: {data['weather'][0]['description']}\n\n")

  async def fetch_weather(self, session, city, api_key):
    params = {
      "q": city,
      "appid": api_key
    }
    async with session.get(self.openweather_url, params=params) as response:
      if response.status == 200:
        data = await response.json()
        return data
      else:
        return {"city": city, "error": response.status}
  
  async def get_weather_data(self, cities, api_key):
    async with aiohttp.ClientSession(trust_env=True) as session:
      tasks = [self.fetch_weather(session, city[0], api_key) for city in cities]
      results = await asyncio.gather(*tasks)
      return results




  
  def get_cities(self, xlat, xlng, ylat, ylng):
    conn = sqlite3.connect("weather.db")
    c = conn.cursor()
    c.execute("SELECT city, lat, lng FROM worldcities WHERE lat BETWEEN ? AND ? AND lng BETWEEN ? AND ?", (xlat, ylat, xlng, ylng))
    cities = c.fetchall()
    print(cities)
    conn.close()
    return cities
  

    


class LogFrame(tk.Frame):
  def __init__(self, parent):
    super().__init__(parent)
    self.label = ttk.Label(self, text="Log Frame")
    self.label.pack()

class Application(tk.Tk):
  def __init__(self):
    super().__init__()
    self.title("Weather App")
    self.geometry("400x400")
    self.notebook = ttk.Notebook(self)
    self.create_database()

    self.api_key_frame = APIKeyInputFrame(self.notebook)
    self.notebook.add(self.api_key_frame, text="API key")

    self.main_frame = MainFrame(self.notebook)
    self.notebook.add(self.main_frame, text="Main")

    self.log_frame = LogFrame(self.notebook)
    self.notebook.add(self.log_frame, text="Logs")

    self.notebook.pack(expand=True, fill="both")

  def create_database(self):
    conn = sqlite3.connect("weather.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS api_keys (key TEXT)")
    conn.commit()

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