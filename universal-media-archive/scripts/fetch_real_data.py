import requests
import base64
import random
from pymongo import MongoClient
from datetime import datetime, UTC
import time
import os
import json
import threading
import hashlib
from urllib.parse import quote

# ─── CONFIG ───
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "universal_media_archive"

TMDB_API_KEY = "fe3469a608d95bbaab8e72a8388c73ea"
RAWG_API_KEY = "19df3cf2a810459599d4b205f86678ee"
SPOTIFY_CLIENT_ID = "d45d82d80c66466c8c3b3be26aa35167"
SPOTIFY_CLIENT_SECRET = "904efece61114288a869472fa76d3ba2"
YOUTUBE_API_KEY = "AIzaSyARKdi8pNMqNGf8WCSTodjhBCGg3RIVrIg"

SYNC_INTERVAL = 1800

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
media_col = db["media"]

# ─── CACHE ───
CACHE_DIR = "cache"
CACHE_TTL = 86400
os.makedirs(CACHE_DIR, exist_ok=True)

def make_cache_key(url, params=None):
    return hashlib.md5((url + str(params)).encode()).hexdigest()

def load_cache(key):
    path = os.path.join(CACHE_DIR, f"{key}.json")
    if not os.path.exists(path):
        return None
    if time.time() - os.path.getmtime(path) > CACHE_TTL:
        return None
    return json.load(open(path))

def save_cache(key, data):
    path = os.path.join(CACHE_DIR, f"{key}.json")
    json.dump(data, open(path, "w"))

# ─── SAFE REQUEST ───
def safe_request(url, params=None, headers=None, retries=5):
    key = make_cache_key(url, params)
    cached = load_cache(key)

    if cached:
        return cached

    for i in range(retries):
        try:
            h = {
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json"
            }
            if headers:
                h.update(headers)

            res = requests.get(url, params=params, headers=h, timeout=15)

            if res.status_code == 200:
                data = res.json()
                save_cache(key, data)
                return data

        except Exception:
            pass

        time.sleep(2 ** i)

    return {}

# ─── HELPERS ───
def exists(title, t):
    return media_col.find_one({"title": title, "type": t}) is not None

def generate_sources(title, t):
    q = title.replace(" ", "+")

    if t in ["movie", "show"]:
        return [
            {"platform": "google", "url": f"https://www.google.com/search?q={q}+watch"},
            {"platform": "justwatch", "url": f"https://www.justwatch.com/in/search?q={q}"}
        ]

    if t == "song":
        return [
            {"platform": "spotify", "url": f"https://open.spotify.com/search/{q}"}
        ]

    if t == "game":
        return [
            {"platform": "steam", "url": f"https://store.steampowered.com/search/?term={q}"}
        ]

    return []

    return []
def count_type(t):
    return media_col.count_documents({"type": t})

# ─── FETCH FUNCTIONS ───

def fetch_movies():
    print("🎬 Movies...")

    page = 1
    TARGET = 120

    while count_type("movie") < TARGET and page <= 10:
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&page={page}"
        data = safe_request(url)

        for m in data.get("results", []):
            title = m.get("title")

            if not title or exists(title, "movie"):
                continue

            media_col.insert_one({
                "title": title,
                "type": "movie",
                "view_count": int(m.get("popularity", 0) * 100),
                "thumbnail": f"https://image.tmdb.org/t/p/w500{m.get('poster_path')}",
                "sources": generate_sources(title, "movie"),
                "added_at": datetime.now(UTC)
            })

        page += 1

def fetch_shows():
    print("📺 Shows...")

    page = 1
    TARGET = 120

    while count_type("show") < TARGET and page <= 10:
        url = f"https://api.themoviedb.org/3/tv/popular?api_key={TMDB_API_KEY}&page={page}"
        data = safe_request(url)

        for s in data.get("results", []):
            title = s.get("name")

            if not title or exists(title, "show"):
                continue

            media_col.insert_one({
                "title": title,
                "type": "show",
                "view_count": int(s.get("popularity", 0) * 100),
                "thumbnail": f"https://image.tmdb.org/t/p/w500{s.get('poster_path')}",
                "sources": generate_sources(title, "show"),
                "added_at": datetime.now(UTC)
            })

        page += 1

def fetch_games():
    print("🎮 Games...")

    page = 1
    TARGET = 120

    while count_type("game") < TARGET and page <= 5:
        url = f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&page={page}"
        data = safe_request(url)

        if "results" not in data:
            break

        for g in data["results"]:
            title = g.get("name")

            if not title or exists(title, "game"):
                continue

            media_col.insert_one({
                "title": title,
                "type": "game",
                "view_count": g.get("ratings_count", 0),
                "thumbnail": g.get("background_image"),
                "sources": generate_sources(title, "game"),
                "added_at": datetime.now(UTC)
            })

        page += 1

def fetch_books():
    print("📚 Books...")

    queries = ["fiction", "fantasy", "science", "history", "novel"]
    TARGET = 120

    for q in queries:
        if count_type("book") >= TARGET:
            break

        url = f"https://www.googleapis.com/books/v1/volumes?q={q}&maxResults=40"
        data = safe_request(url)

        for b in data.get("items", []):
            info = b.get("volumeInfo", {})
            title = info.get("title")

            if not title or exists(title, "book"):
                continue

            media_col.insert_one({
                "title": title,
                "type": "book",
                "thumbnail": info.get("imageLinks", {}).get("thumbnail"),
                "added_at": datetime.now(UTC)
            })
def fetch_comics():
    print("📖 Comics & Manga...")

    TARGET = 120

    queries = [
        "manga",
        "marvel comics",
        "dc comics",
        "graphic novel",
        "anime manga",
        "webtoon",
        "manhwa",
        "comic book",
        "shonen manga",
        "seinen manga",
        "superhero comic",
        "fantasy manga"
    ]

    POSITIVE = [
        "manga", "comic", "comics", "graphic",
        "marvel", "dc", "webtoon", "manhwa",
        "shonen", "seinen", "superhero"
    ]

    NEGATIVE = [
        "textbook", "guide", "manual",
        "study", "biography", "summary"
    ]

    for q in queries:
        if count_type("comic") >= TARGET:
            print("✅ Comics target reached")
            return

        start_index = 0

        # 🔥 PAGINATION LOOP
        while count_type("comic") < TARGET and start_index < 120:
            url = f"https://www.googleapis.com/books/v1/volumes?q={q}&maxResults=40&startIndex={start_index}"
            data = safe_request(url)

            items = data.get("items", [])
            if not items:
                break

            for b in items:
                info = b.get("volumeInfo", {})
                title = info.get("title", "")
                if not title:
                    continue

                if exists(title, "comic"):
                    continue

                title_lower = title.lower()
                categories = " ".join(info.get("categories", [])).lower()
                description = info.get("description", "").lower()

                combined = f"{title_lower} {categories} {description}"

                # ✅ Positive filter
                if not any(k in combined for k in POSITIVE):
                    continue

                # ❌ Negative filter
                if any(bad in combined for bad in NEGATIVE):
                    continue

                # 🧠 Smarter tagging
                if any(x in combined for x in ["manga", "anime", "shonen", "seinen"]):
                    tag = "manga"
                elif any(x in combined for x in ["webtoon", "manhwa"]):
                    tag = "webtoon"
                else:
                    tag = "comic"

                try:
                    year = int(info.get("publishedDate", "2000")[:4])
                except:
                    year = None

                media_col.insert_one({
                    "title": title,
                    "type": "comic",
                    "genres": info.get("categories", []),
                    "release_year": year,
                    "creators": info.get("authors", []),
                    "description": info.get("description", ""),
                    "thumbnail": info.get("imageLinks", {}).get("thumbnail"),
                    "sources": [{
                        "platform": "google_books",
                        "url": info.get("infoLink")
                    }],
                    "tags": [tag],
                    "added_at": datetime.now(UTC),
                    "view_count": random.randint(50, 500),
                })

            start_index += 40  # 🔥 move to next page

def fetch_songs():
    print("🎵 Songs...")

    TARGET = 120
    LIMIT = 20

    queries = ["pop", "rock", "hip hop", "lofi", "jazz"]

    # ─── AUTH ───
    auth = base64.b64encode(
        f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()
    ).decode()

    token_res = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={"grant_type": "client_credentials"}
    )

    token_json = token_res.json()
    print("Spotify token:", token_json)

    token = token_json.get("access_token")

    # ─── FALLBACK ───
    if not token:
        print("❌ Spotify auth failed — using fallback songs")

        fallback = [
            "Blinding Lights",
            "Shape of You",
            "Starboy",
            "Levitating",
            "Closer"
        ]

        for title in fallback:
            if exists(title, "song"):
                continue

            media_col.insert_one({
                "title": title,
                "type": "song",
                "sources": [{
                    "platform": "spotify",
                    "url": f"https://open.spotify.com/search/{title.replace(' ', '%20')}"
                }],
                "view_count": 100,
                "added_at": datetime.now(UTC)
            })

        return

    inserted = 0

    # ─── FETCH LOOP ───
    for q in queries:
        if count_type("song") >= TARGET:
            print("✅ Songs target reached")
            break

        offset = 0

        while count_type("song") < TARGET and offset < 200:
            q_clean = q.strip()

            res = requests.get(
                "https://api.spotify.com/v1/search",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/json"
                },
                params={
                    "q": q_clean,
                    "type": "track",
                    "limit": LIMIT,
                    "offset": offset
                }
            )

            print("Spotify status:", res.status_code)

            if res.status_code != 200:
                print("❌ Spotify error:", res.text)
                break

            data = res.json()

            tracks = data.get("tracks", {}).get("items", [])
            if not tracks:
                break

            for t in tracks:
                title = t.get("name")
                if not title:
                    continue

                if exists(title, "song"):
                    continue

                media_col.insert_one({
                    "title": title,
                    "type": "song",
                    "artists": [a["name"] for a in t.get("artists", [])],
                    "album": t.get("album", {}).get("name"),
                    "thumbnail": t["album"]["images"][0]["url"] if t["album"]["images"] else "",
                    "sources": [{
                        "platform": "spotify",
                        "url": t["external_urls"]["spotify"]
                    }],
                    "view_count": t.get("popularity", 0),
                    "added_at": datetime.now(UTC)
                })

                inserted += 1

            offset += LIMIT  # correct pagination

    print(f"✅ Songs inserted: {inserted}")

def get_youtube_views_batch(video_ids):
    url = "https://www.googleapis.com/youtube/v3/videos"

    params = {
        "part": "statistics",
        "id": ",".join(video_ids),
        "key": YOUTUBE_API_KEY
    }

    data = safe_request(url, params=params)

    views_map = {}

    for item in data.get("items", []):
        vid = item["id"]
        views = int(item["statistics"].get("viewCount", 0))
        views_map[vid] = views

    return views_map
    
def fetch_videos():
    print("🎥 Videos...")

    TARGET = 120
    page_token = None

    while count_type("video") < TARGET:
        params = {
            "part": "snippet",
            "q": "documentary",
            "type": "video",
            "maxResults": 25,
            "key": YOUTUBE_API_KEY,
            "pageToken": page_token
        }

        data = safe_request("https://www.googleapis.com/youtube/v3/search", params=params)

        items = data.get("items", [])
        if not items:
            break

        # ✅ Collect IDs
        video_ids = [v["id"]["videoId"] for v in items]

        # ✅ Fetch views in batch
        views_map = get_youtube_views_batch(video_ids)

        for v in items:
            video_id = v["id"]["videoId"]
            title = v["snippet"]["title"]

            if exists(title, "video"):
                continue

            media_col.insert_one({
                "title": title,
                "type": "video",
                "thumbnail": v["snippet"]["thumbnails"]["high"]["url"],
                "sources": [{
                    "platform": "youtube",
                    "url": f"https://youtube.com/watch?v={video_id}"
                }],
                "view_count": views_map.get(video_id, 0),  # ✅ REAL VIEWS
                "added_at": datetime.now(UTC)
            })

        page_token = data.get("nextPageToken")
        if not page_token:
            break

# ─── SYNC ───
def sync_all():
    print("🧹 Clearing database...")
    media_col.delete_many({})   # 👈 add here

    print("🔄 Sync started...")
    fetch_movies()
    fetch_shows()
    fetch_games()
    fetch_books()
    fetch_comics()
    fetch_songs()
    fetch_videos()
    print("✅ Sync complete")

def worker():
    while True:
        sync_all()
        time.sleep(SYNC_INTERVAL)

# ─── MAIN ───
if __name__ == "__main__":
    threading.Thread(target=worker, daemon=True).start()
    while True:
        time.sleep(1)