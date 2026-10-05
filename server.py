import os, sqlite3, secrets, datetime, hashlib
from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

APP=Flask(__name__); CORS(APP)
DB=os.getenv("DB_PATH","fly.db")
JWT_SECRET=os.getenv("JWT_SECRET","CHANGE_ME_IN_PRODUCTION")
ADMIN_USER=os.getenv("ADMIN_USER","noabot5")
ADMIN_PASS=os.getenv("ADMIN_PASS","CHANGE_ME_ADMIN_PASSWORD")

def db():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
    c.execute("""CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,username TEXT UNIQUE,password TEXT NOT NULL,is_admin INTEGER DEFAULT 0,created TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS keys(id INTEGER PRIMARY KEY,key TEXT UNIQUE,duration TEXT,created TEXT)"""); c.commit(); return c
def ensure_admin():
    c=db(); u=c.execute("SELECT * FROM users WHERE username=?",(ADMIN_USER,)).fetchone()
    if not u: c.execute("INSERT INTO users(username,password,is_admin,created) VALUES(?,?,?,?,?)".replace("VALUES(?,?,?,?,?)","VALUES(?,?,1,?)"),(ADMIN_USER,generate_password_hash(ADMIN_PASS),datetime.datetime.utcnow().isoformat())); c.commit()
ensure_admin()

def auth(admin=False):
    h=request.headers.get("Authorization","")
    if not h.startswith("Bearer "): return None
    try:
        p=jwt.decode(h[7:],JWT_SECRET,algorithms=["HS256"])
        c=db(); u=c.execute("SELECT * FROM users WHERE id=?",(p["id"],)).fetchone()
        if not u or (admin and not u["is_admin"]): return None
        return u
    except: return None
def login_response(u):
    t=jwt.encode({"id":u["id"],"exp":datetime.datetime.utcnow()+datetime.timedelta(days=7)},JWT_SECRET,algorithm="HS256")
    return {"token":t,"user":{"username":u["username"],"isAdmin":bool(u["is_admin"])}}

@APP.post("/api/register")
def register():
    d=request.json or {}; name=d.get("username","").strip(); pw=d.get("password","")
    if len(name)<3 or len(pw)<8:return jsonify(error="Логин от 3 символов, пароль от 8"),400
    if name.lower()==ADMIN_USER.lower():return jsonify(error="Этот логин зарезервирован"),400
    c=db()
    try:c.execute("INSERT INTO users(username,password,created) VALUES(?,?,?)",(name,generate_password_hash(pw),datetime.datetime.utcnow().isoformat()));c.commit()
    except sqlite3.IntegrityError:return jsonify(error="Такой логин уже существует"),409
    return jsonify(login_response(c.execute("SELECT * FROM users WHERE username=?",(name,)).fetchone()))
@APP.post("/api/login")
def login():
    d=request.json or {}; c=db();u=c.execute("SELECT * FROM users WHERE username=?",(d.get("username",""),)).fetchone()
    if not u or not check_password_hash(u["password"],d.get("password","")):return jsonify(error="Неверный логин или пароль"),401
    return jsonify(login_response(u))
@APP.post("/api/admin/keys")
def make_key():
    u=auth(True)
    if not u:return jsonify(error="Доступ запрещён"),403
    d=request.json or {}; duration=d.get("duration","30 дней")
    key="FLY-"+secrets.token_hex(2).upper()+"-"+secrets.token_hex(2).upper()+"-"+secrets.token_hex(2).upper()
    c=db();c.execute("INSERT INTO keys(key,duration,created) VALUES(?,?,?)",(key,duration,datetime.datetime.utcnow().isoformat()));c.commit()
    return jsonify(key=key,duration=duration)
if __name__=="__main__": APP.run(host="0.0.0.0",port=int(os.getenv("PORT","8080")))
