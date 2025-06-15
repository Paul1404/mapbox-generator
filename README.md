# mapbox-generator

Generate beautiful static route maps with Mapbox Static Images API, perfect for banners, flyers, or web use.  
Supports multiple styles, custom markers, and timestamped output files.

---

## Features

- **Static PNG map generation** with route and custom markers
- **Multiple Mapbox styles** in one run (define in `.env`)
- **Red club-style route and markers** (customizable)
- **Timestamped output files** for easy organization
- **Environment variable management** with [python-dotenv](https://pypi.org/project/python-dotenv/)
- **Easy to extend** for custom icons, colors, or more

---

## Quickstart

### 1. Clone the repo

```bash
git clone https://github.com/Paul1404/mapbox-generator.git
cd mapbox-generator
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
# or, if using uv:
uv pip install -r requirements.txt
```

### 3. Set up your `.env`

Create a `.env` file in the project root:

## Example `.env`

```env
MAPBOX_TOKEN=pk.eyJ...yourtoken...
STYLES=mapbox/streets-v12,mapbox/light-v11
START_POINT=
END_POINT=
```

- `START_POINT` and `END_POINT` are in the format: `longitude,latitude`
- You can get coordinates from Google Maps or OpenStreetMap (right-click → "What's here?")

- You can add as many styles as you want, separated by commas.
- Use [your own custom style](https://studio.mapbox.com/) if you like.

### 4. Run the generator

```bash
python main.py
# or, if using uv:
uv run main.py
```

### 5. Find your maps

Output files will be named like:

```
banner-map_streets-v12_20240615_153000.png
banner-map_light-v11_20240615_153000.png
```

---

## Configuration

- **Route start/end:**  
  Edit the `start_point` and `end_point` variables in `main.py` to your desired coordinates.
- **Route color/width:**  
  Change the `geojson` section in `main.py` for your club’s branding.
- **Markers:**  
  Uses a red circle for start and a red star for finish by default.  
  You can use [custom marker icons](https://docs.mapbox.com/api/maps/static-images/#custom-marker-icons) if you wish.

---

## Example `.env`

```env
MAPBOX_TOKEN=pk.eyJ...yourtoken...
STYLES=mapbox/streets-v12,mapbox/light-v11,paulcustom=citrus4787/yourcustomid
```

---

## Troubleshooting

- **Checkerboard/transparent background?**  
  Your style is likely a "Mapbox Standard" style, which is not supported by the Static Images API.  
  Use a classic style (Streets, Light, Outdoors) as your base.
- **Route is a straight line?**  
  Make sure the Directions API call is working and returning a valid route.
- **Markers not showing?**  
  Check your marker syntax and coordinates.

---

## License

[MIT License](https://github.com/Paul1404/mapbox-generator/blob/main/LICENSE)

---

## Credits

- [Mapbox Static Images API](https://docs.mapbox.com/api/maps/static-images/)
- [Mapbox Directions API](https://docs.mapbox.com/api/navigation/directions/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)