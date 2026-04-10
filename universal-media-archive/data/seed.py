"""
Seed script — populates MongoDB with sample media entries.
Run: python seed.py
"""

from pymongo import MongoClient, TEXT
from datetime import datetime
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "universal_media_archive")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

media_col = db["media"]
users_col = db["users"]
reviews_col = db["reviews"]

# ── drop existing ──────────────────────────────────────────────
media_col.drop()
users_col.drop()
reviews_col.drop()

# ── indexes ────────────────────────────────────────────────────
media_col.create_index([("title", TEXT), ("genres", TEXT), ("tags", TEXT), ("description", TEXT)])
media_col.create_index("type")
media_col.create_index("release_year")

# ── sample media ───────────────────────────────────────────────
MEDIA = [
    # MOVIES
    {
        "title": "Inception",
        "type": "movie",
        "genres": ["Sci-Fi", "Thriller", "Action"],
        "release_year": 2010,
        "creators": ["Christopher Nolan"],
        "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page"],
        "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
        "thumbnail": "https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=400",
        "ratings": {"imdb": 8.8, "user": 8.9, "review_count": 2},
        "sources": [
            {"platform": "Netflix", "url": "https://www.netflix.com/title/70131314", "availability": "subscription"},
            {"platform": "YouTube", "url": "https://www.youtube.com/watch?v=YoHD9XEInc0", "availability": "rent"},
        ],
        "tags": ["dreams", "heist", "mind-bending", "christopher-nolan"],
        "related": [],
        "view_count": 1420,
        "added_at": datetime(2024, 1, 10),
    },
    {
        "title": "The Dark Knight",
        "type": "movie",
        "genres": ["Action", "Crime", "Drama"],
        "release_year": 2008,
        "creators": ["Christopher Nolan"],
        "cast": ["Christian Bale", "Heath Ledger", "Aaron Eckhart"],
        "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
        "thumbnail": "https://images.unsplash.com/photo-1635805737707-575885ab0820?w=400",
        "ratings": {"imdb": 9.0, "user": 9.2, "review_count": 1},
        "sources": [
            {"platform": "HBO Max", "url": "https://www.hbomax.com/", "availability": "subscription"},
            {"platform": "Amazon Prime", "url": "https://www.amazon.com/", "availability": "rent"},
        ],
        "tags": ["batman", "joker", "superhero", "gotham", "crime"],
        "related": [],
        "view_count": 1980,
        "added_at": datetime(2024, 1, 11),
    },
    {
        "title": "Parasite",
        "type": "movie",
        "genres": ["Thriller", "Drama", "Dark Comedy"],
        "release_year": 2019,
        "creators": ["Bong Joon-ho"],
        "cast": ["Song Kang-ho", "Lee Sun-kyun", "Cho Yeo-jeong"],
        "description": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
        "thumbnail": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=400",
        "ratings": {"imdb": 8.5, "user": 8.7, "review_count": 0},
        "sources": [
            {"platform": "Hulu", "url": "https://www.hulu.com/", "availability": "subscription"},
        ],
        "tags": ["korean", "class-warfare", "oscar-winner", "social-commentary"],
        "related": [],
        "view_count": 890,
        "added_at": datetime(2024, 2, 1),
    },
    {
        "title": "Interstellar",
        "type": "movie",
        "genres": ["Sci-Fi", "Drama", "Adventure"],
        "release_year": 2014,
        "creators": ["Christopher Nolan"],
        "cast": ["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain"],
        "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
        "thumbnail": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=400",
        "ratings": {"imdb": 8.6, "user": 8.8, "review_count": 0},
        "sources": [
            {"platform": "Paramount+", "url": "https://www.paramountplus.com/", "availability": "subscription"},
        ],
        "tags": ["space", "time", "relativity", "wormhole", "father-daughter"],
        "related": [],
        "view_count": 1100,
        "added_at": datetime(2024, 2, 15),
    },

    # TV SHOWS
    {
        "title": "Breaking Bad",
        "type": "show",
        "genres": ["Crime", "Drama", "Thriller"],
        "release_year": 2008,
        "creators": ["Vince Gilligan"],
        "cast": ["Bryan Cranston", "Aaron Paul", "Anna Gunn"],
        "description": "A chemistry teacher diagnosed with lung cancer teams up with a former student to manufacture and sell methamphetamine.",
        "thumbnail": "https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=400",
        "ratings": {"imdb": 9.5, "user": 9.6, "review_count": 0},
        "sources": [
            {"platform": "Netflix", "url": "https://www.netflix.com/title/70143836", "availability": "subscription"},
            {"platform": "AMC+", "url": "https://www.amc.com/", "availability": "subscription"},
        ],
        "tags": ["meth", "crime", "transformation", "new-mexico", "antihero"],
        "related": [],
        "view_count": 2310,
        "added_at": datetime(2024, 1, 5),
    },
    {
        "title": "Chernobyl",
        "type": "show",
        "genres": ["Drama", "History", "Thriller"],
        "release_year": 2019,
        "creators": ["Craig Mazin"],
        "cast": ["Jared Harris", "Stellan Skarsgård", "Emily Watson"],
        "description": "A dramatization of the 1986 Chernobyl nuclear disaster and the cleanup efforts that followed.",
        "thumbnail": "https://images.unsplash.com/photo-1593007791459-4b05e1158229?w=400",
        "ratings": {"imdb": 9.4, "user": 9.3, "review_count": 0},
        "sources": [
            {"platform": "HBO Max", "url": "https://www.hbomax.com/", "availability": "subscription"},
        ],
        "tags": ["nuclear", "soviet", "disaster", "historical", "miniseries"],
        "related": [],
        "view_count": 980,
        "added_at": datetime(2024, 3, 1),
    },

    # BOOKS
    {
        "title": "Dune",
        "type": "book",
        "genres": ["Sci-Fi", "Fantasy", "Epic"],
        "release_year": 1965,
        "creators": ["Frank Herbert"],
        "cast": [],
        "description": "Set on the desert planet Arrakis, Dune is the story of the boy Paul Atreides, heir to a noble family tasked with ruling an inhospitable world.",
        "thumbnail": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400",
        "ratings": {"imdb": None, "user": 8.9, "review_count": 0},
        "sources": [
            {"platform": "Goodreads", "url": "https://www.goodreads.com/book/show/44767458-dune", "availability": "free"},
            {"platform": "Amazon Kindle", "url": "https://www.amazon.com/", "availability": "purchase"},
            {"platform": "Project Gutenberg", "url": "https://www.gutenberg.org/", "availability": "free"},
        ],
        "tags": ["desert", "politics", "religion", "ecology", "classic-sci-fi"],
        "related": [],
        "view_count": 760,
        "added_at": datetime(2024, 1, 20),
    },
    {
        "title": "1984",
        "type": "book",
        "genres": ["Dystopian", "Political Fiction", "Sci-Fi"],
        "release_year": 1949,
        "creators": ["George Orwell"],
        "cast": [],
        "description": "Set in a totalitarian society ruled by Big Brother, 1984 follows Winston Smith who secretly hates the Party and dreams of rebellion.",
        "thumbnail": "https://images.unsplash.com/photo-1495640388908-05fa85288e61?w=400",
        "ratings": {"imdb": None, "user": 9.0, "review_count": 0},
        "sources": [
            {"platform": "Project Gutenberg", "url": "https://www.gutenberg.org/", "availability": "free"},
            {"platform": "Open Library", "url": "https://openlibrary.org/", "availability": "free"},
        ],
        "tags": ["totalitarianism", "surveillance", "dystopia", "classic", "politics"],
        "related": [],
        "view_count": 1050,
        "added_at": datetime(2024, 1, 22),
    },

    # SONGS
    {
        "title": "Bohemian Rhapsody",
        "type": "song",
        "genres": ["Rock", "Progressive Rock", "Opera Rock"],
        "release_year": 1975,
        "creators": ["Freddie Mercury", "Queen"],
        "cast": [],
        "description": "A six-minute suite, structured as multiple sections without a chorus: an intro, a ballad segment, an operatic passage, a hard rock part, and a reflective coda.",
        "thumbnail": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=400",
        "ratings": {"imdb": None, "user": 9.5, "review_count": 0},
        "sources": [
            {"platform": "Spotify", "url": "https://open.spotify.com/track/7tFiyTwD0nx5a1eklYtX2J", "availability": "subscription"},
            {"platform": "YouTube", "url": "https://www.youtube.com/watch?v=fJ9rUzIMcZQ", "availability": "free"},
            {"platform": "Apple Music", "url": "https://music.apple.com/", "availability": "subscription"},
        ],
        "tags": ["queen", "classic-rock", "iconic", "operatic", "70s"],
        "related": [],
        "view_count": 2890,
        "added_at": datetime(2024, 1, 8),
    },
    {
        "title": "Lose Yourself",
        "type": "song",
        "genres": ["Hip-Hop", "Rap"],
        "release_year": 2002,
        "creators": ["Eminem"],
        "cast": [],
        "description": "Written for the film 8 Mile, the song talks about the opportunity of a lifetime and giving it everything you have.",
        "thumbnail": "https://images.unsplash.com/photo-1571330735066-03aaa9429d89?w=400",
        "ratings": {"imdb": None, "user": 9.1, "review_count": 0},
        "sources": [
            {"platform": "Spotify", "url": "https://open.spotify.com/track/5Z01UMMf7V1o0MzF86s6WJ", "availability": "subscription"},
            {"platform": "YouTube", "url": "https://www.youtube.com/watch?v=_Yhyp-_hX2s", "availability": "free"},
        ],
        "tags": ["eminem", "motivational", "oscar-winning", "rap", "2000s"],
        "related": [],
        "view_count": 1760,
        "added_at": datetime(2024, 2, 10),
    },

    # GAMES
    {
        "title": "The Witcher 3: Wild Hunt",
        "type": "game",
        "genres": ["RPG", "Open World", "Fantasy"],
        "release_year": 2015,
        "creators": ["CD Projekt Red"],
        "cast": [],
        "description": "An award-winning role-playing game set in a vast fantasy world. Play as Geralt of Rivia, a monster hunter, and search for a child of prophecy.",
        "thumbnail": "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=400",
        "ratings": {"imdb": None, "user": 9.7, "review_count": 0},
        "sources": [
            {"platform": "GOG", "url": "https://www.gog.com/game/the_witcher_3_wild_hunt", "availability": "purchase"},
            {"platform": "Steam", "url": "https://store.steampowered.com/app/292030/", "availability": "purchase"},
            {"platform": "PlayStation Store", "url": "https://store.playstation.com/", "availability": "purchase"},
        ],
        "tags": ["witcher", "geralt", "open-world", "goty", "rpg", "fantasy"],
        "related": [],
        "view_count": 2100,
        "added_at": datetime(2024, 1, 15),
    },
    {
        "title": "Portal 2",
        "type": "game",
        "genres": ["Puzzle", "Sci-Fi", "Co-op"],
        "release_year": 2011,
        "creators": ["Valve"],
        "cast": [],
        "description": "An award-winning puzzle-platform game that puts players through a thinking-with-portals adventure full of physics-based challenges.",
        "thumbnail": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=400",
        "ratings": {"imdb": None, "user": 9.8, "review_count": 0},
        "sources": [
            {"platform": "Steam", "url": "https://store.steampowered.com/app/620/", "availability": "purchase"},
        ],
        "tags": ["portal", "glados", "puzzle", "valve", "co-op", "physics"],
        "related": [],
        "view_count": 1340,
        "added_at": datetime(2024, 2, 20),
    },

    # YOUTUBE VIDEOS
    {
        "title": "The Feynman Technique - How to Learn Anything",
        "type": "video",
        "genres": ["Education", "Science", "Self-Improvement"],
        "release_year": 2017,
        "creators": ["Thomas Frank"],
        "cast": [],
        "description": "A video explaining Richard Feynman's learning technique, where you explain concepts in simple terms to identify gaps in your knowledge.",
        "thumbnail": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400",
        "ratings": {"imdb": None, "user": 8.5, "review_count": 0},
        "sources": [
            {"platform": "YouTube", "url": "https://www.youtube.com/watch?v=_f-qkGJBPts", "availability": "free"},
        ],
        "tags": ["learning", "feynman", "education", "productivity", "study"],
        "related": [],
        "view_count": 670,
        "added_at": datetime(2024, 3, 5),
    },

    # COMICS
    {
        "title": "Watchmen",
        "type": "comic",
        "genres": ["Superhero", "Political", "Dystopian"],
        "release_year": 1986,
        "creators": ["Alan Moore", "Dave Gibbons"],
        "cast": [],
        "description": "Set in an alternative history 1985 America, Watchmen follows costumed heroes and asks 'who watches the watchmen?'",
        "thumbnail": "https://images.unsplash.com/photo-1612036782180-6f0b6cd846fe?w=400",
        "ratings": {"imdb": None, "user": 9.3, "review_count": 0},
        "sources": [
            {"platform": "DC Universe", "url": "https://www.dc.com/", "availability": "subscription"},
            {"platform": "ComiXology", "url": "https://www.comixology.com/", "availability": "purchase"},
        ],
        "tags": ["alan-moore", "superheroes", "political", "graphic-novel", "classic"],
        "related": [],
        "view_count": 540,
        "added_at": datetime(2024, 3, 10),
    },

    # PODCAST
    {
        "title": "Lex Fridman Podcast — Elon Musk",
        "type": "podcast",
        "genres": ["Technology", "Science", "Interview"],
        "release_year": 2023,
        "creators": ["Lex Fridman"],
        "cast": ["Elon Musk"],
        "description": "Lex Fridman's in-depth conversation with Elon Musk covering AI, rockets, consciousness, and the future of humanity.",
        "thumbnail": "https://images.unsplash.com/photo-1478737270239-2f02b77fc618?w=400",
        "ratings": {"imdb": None, "user": 8.2, "review_count": 0},
        "sources": [
            {"platform": "YouTube", "url": "https://www.youtube.com/watch?v=JN3KPFbWCy8", "availability": "free"},
            {"platform": "Spotify", "url": "https://open.spotify.com/", "availability": "free"},
        ],
        "tags": ["elon-musk", "ai", "spacex", "tesla", "interview", "technology"],
        "related": [],
        "view_count": 920,
        "added_at": datetime(2024, 3, 15),
    },
]

result = media_col.insert_many(MEDIA)
ids = [str(i) for i in result.inserted_ids]
print(f"✓ Inserted {len(ids)} media items")

# Set up related links
inception_id = ids[0]
dark_knight_id = ids[1]
interstellar_id = ids[3]

# Nolan films related to each other
for mid, related_id in [(inception_id, interstellar_id), (interstellar_id, inception_id), (dark_knight_id, inception_id)]:
    media_col.update_one(
        {"_id": result.inserted_ids[ids.index(mid)]},
        {"$push": {"related": {"media_id": related_id, "relation": "same director"}}}
    )

# Dune book related to a movie
dune_id = ids[6]
# (Dune movie not in seed, but we set a self-reference example)

# ── sample users ────────────────────────────────────────────────
USERS = [
    {
        "username": "archivist_prime",
        "email": "archivist@example.com",
        "watchlist": [ids[0], ids[4], ids[8]],
        "history": [ids[1], ids[2], ids[6]],
        "preferences": ["Sci-Fi", "Thriller", "Drama"],
        "created_at": datetime(2024, 1, 1),
    },
    {
        "username": "cinephile99",
        "email": "cine@example.com",
        "watchlist": [ids[2], ids[3]],
        "history": [ids[0], ids[1]],
        "preferences": ["Drama", "Crime", "History"],
        "created_at": datetime(2024, 1, 15),
    },
]
users_result = users_col.insert_many(USERS)
user_ids = [str(i) for i in users_result.inserted_ids]
print(f"✓ Inserted {len(user_ids)} users")

# ── sample reviews ──────────────────────────────────────────────
REVIEWS = [
    {"user_id": user_ids[0], "media_id": ids[0], "rating": 9.5, "comment": "A mind-bending masterpiece. Nolan at his absolute peak.", "created_at": datetime(2024, 2, 1)},
    {"user_id": user_ids[1], "media_id": ids[0], "rating": 8.5, "comment": "Visually stunning but the plot needs attention.", "created_at": datetime(2024, 2, 5)},
    {"user_id": user_ids[0], "media_id": ids[1], "rating": 9.5, "comment": "Heath Ledger's Joker is the greatest villain ever put to screen.", "created_at": datetime(2024, 2, 10)},
]
reviews_col.insert_many(REVIEWS)
print(f"✓ Inserted {len(REVIEWS)} reviews")

# Update user ratings on media
for mid in [ids[0], ids[1]]:
    all_reviews = list(reviews_col.find({"media_id": mid}))
    if all_reviews:
        avg = sum(r["rating"] for r in all_reviews) / len(all_reviews)
        from bson import ObjectId
        media_col.update_one(
            {"_id": ObjectId(mid)},
            {"$set": {"ratings.user": round(avg, 1), "ratings.review_count": len(all_reviews)}}
        )

print("\n🎬 Universal Media Archive seed complete!")
print(f"   Media: {len(ids)} items")
print(f"   Users: {len(user_ids)}")
print(f"   Reviews: {len(REVIEWS)}")
