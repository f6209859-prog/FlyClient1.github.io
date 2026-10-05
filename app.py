import os, sqlite3, secrets, datetime
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)
DB = os.getenv("DB_PATH", os.path.join(os.path.dirname(__file__), "fly.db"))
JWT_SECRET = os.getenv("JWT_SECRET", "dev-only-change-this-secret")
ADMIN_USER = os.getenv("ADMIN_USER", "noabot5")
ADMIN_PASS = os.getenv("ADMIN_PASS", "change-me-now")

HTML = r'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#08030f"><title>FLY CLIENT</title><link rel="stylesheet" href="/style.css"></head>
<body><div class="noise"></div><header><div class="nav wrap"><a class="brand" href="/"><span class="mark">F</span><span>FLY <b>CLIENT</b></span></a><nav><a href="#features">Возможности</a><a href="#prices">Тарифы</a><a href="#download">Скачать</a></nav><button class="btn ghost" id="authBtn">Войти</button></div></header>
<main><section class="hero"><div class="wrap heroGrid"><div><div class="eyebrow">● MINECRAFT CLIENT <b>PC</b></div><h1>ИГРАЙ<br><strong>СВОБОДНО.</strong></h1><p>Современный Fly Client с быстрым запуском, оптимизацией и аккуратным интерфейсом.</p><div class="actions"><a class="btn primary" href="#download">Скачать клиент ↗</a><button class="btn ghost" id="registerHero">Создать аккаунт</button></div><small>Доступно для Windows · лицензия активируется в аккаунте</small></div><div class="visual"><div class="crystal"><div class="crystalF">F</div><span>FLY CLIENT</span><b>READY TO PLAY</b></div></div></div></section>
<section class="section" id="features"><div class="wrap"><div class="head"><div><small>01 / ВОЗМОЖНОСТИ</small><h2>Всё, что нужно<br><em>для игры.</em></h2></div><p>Чистый интерфейс, быстрый запуск и настройки, которые не мешают играть.</p></div><div class="cards"><article><i>01</i><h3>Оптимизация</h3><p>Настройки для стабильной работы Minecraft и высокого FPS.</p></article><article><i>02</i><h3>Быстрый запуск</h3><p>Минимум действий — открывай клиент и заходи в игру.</p></article><article><i>03</i><h3>Чистый UI</h3><p>Современная тёмная визуальная система без перегруза.</p></article></div></div></section>
<section class="section" id="prices"><div class="wrap"><div class="head"><div><small>02 / ДОСТУП</small><h2>Выбери свой<br><em>тариф.</em></h2></div></div><div class="prices"><div class="price"><small>30 ДНЕЙ</small><strong>200 ₽</strong><p>Для знакомства с клиентом.</p><button class="btn ghost buy">Выбрать</button></div><div class="price"><small>180 ДНЕЙ</small><strong>500 ₽</strong><p>Полгода без лишних продлений.</p><button class="btn ghost buy">Выбрать</button></div><div class="price featured"><label>ПОПУЛЯРНЫЙ</label><small>1 ГОД</small><strong>600 ₽</strong><p>Лучший вариант для постоянной игры.</p><button class="btn primary buy">Выбрать</button></div><div class="price"><small>НАВСЕГДА</small><strong>800 ₽</strong><p>Один ключ — доступ без срока.</p><button class="btn ghost buy">Выбрать</button></div></div></div></section>
<section class="download" id="download"><div class="wrap downloadBox"><div><small>03 / DOWNLOAD</small><h2>Готов к игре?</h2><p>Войди в аккаунт и скачай клиент после публикации файла.</p></div><button class="btn primary" id="downloadBtn">Скачать лаунчер ↓</button></div></section></main><footer><div class="wrap"><span>© 2026 FLY CLIENT</span><span>MINECRAFT / PC</span></div></footer>
<div class="modal hidden" id="authModal"><div class="backdrop"></div><div class="box"><button class="close" id="closeAuth">×</button><div class="modalLogo"><span>F</span><b>FLY CLIENT</b></div><div id="loginView"><small>ACCOUNT / LOGIN</small><h2>С возвращением.</h2><label>Логин<input id="loginUser" autocomplete="username"></label><label>Пароль<input id="loginPass" type="password" autocomplete="current-password"></label><button class="btn primary full" id="loginBtn">Войти →</button><p>Нет аккаунта? <button class="link" id="showRegister">Создать</button></p></div><div id="registerView" class="hidden"><small>ACCOUNT / REGISTER</small><h2>Создай аккаунт.</h2><label>Логин<input id="regUser" autocomplete="username"></label><label>Пароль<input id="regPass" type="password" autocomplete="new-password"></label><label>Повтори пароль<input id="regPass2" type="password" autocomplete="new-password"></label><button class="btn primary full" id="registerBtn">Зарегистрироваться →</button><p>Уже есть аккаунт? <button class="link" id="showLogin">Войти</button></p></div></div></div>
<div class="modal hidden" id="accountModal"><div class="backdrop"></div><div class="box"><button class="close" id="closeAccount">×</button><small>ACCOUNT / PROFILE</small><h2>Мой аккаунт.</h2><div class="profile"><div class="avatar" id="avatar">F</div><div><b id="name">—</b><small id="role">Пользователь</small></div></div><div class="status">● Активен</div><div id="adminBox" class="hidden admin"><h3>Админ-панель</h3><select id="keyDays"><option value="30">30 дней</option><option value="180">180 дней</option><option value="365">1 год</option><option value="forever">Навсегда</option></select><button class="btn primary full" id="makeKey">Создать ключ</button><pre id="keyResult"></pre></div><button class="btn danger full" id="logout">Выйти</button></div></div><div class="toast hidden" id="toast"></div><script src="/script.js"></script></body></html>'''

CSS = r'''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#050207;color:#f7f2ff;font:15px Inter,Arial,sans-serif}a{color:inherit;text-decoration:none}button,input,select{font:inherit}.wrap{width:min(1160px,92%);margin:auto}header{position:fixed;z-index:5;top:0;width:100%;background:#050207cc;backdrop-filter:blur(18px);border-bottom:1px solid #ffffff12}.nav{height:76px;display:flex;align-items:center;gap:35px}.brand{display:flex;align-items:center;gap:10px;font-weight:900;letter-spacing:.08em}.brand b{opacity:.55}.mark,.modalLogo span,.avatar{display:grid;place-items:center;background:linear-gradient(145deg,#fff,#b879ff 45%,#6500ff);color:#08030f;font-weight:1000}.mark{width:36px;height:36px;clip-path:polygon(18% 0,100% 0,70% 35%,100% 35%,62% 100%,0 100%,31% 50%,0 50%);font-size:20px}nav{margin-left:auto;display:flex;gap:28px;color:#aaa0b4}nav a:hover{color:#fff}.btn{border:1px solid #ffffff18;border-radius:12px;padding:12px 18px;background:#ffffff08;color:#fff;cursor:pointer;transition:.2s}.btn:hover{transform:translateY(-1px);border-color:#a94cff55}.primary{background:linear-gradient(135deg,#8e2cff,#4e00ff);border:0;box-shadow:0 10px 35px #6b19ff35}.ghost{background:#ffffff08}.danger{background:#ff244015;border-color:#ff244044;color:#ff9fae}.hero{padding:170px 0 100px;overflow:hidden;background:radial-gradient(circle at 78% 38%,#6c16ff35,transparent 34%),linear-gradient(180deg,#08030f,#050207)}.heroGrid{display:grid;grid-template-columns:1fr 1fr;align-items:center;gap:50px}.eyebrow,section small{color:#a99cb2;letter-spacing:.14em;font-size:11px}.eyebrow b{margin-left:8px;color:#c978ff}.hero h1{font-size:clamp(56px,8vw,110px);line-height:.82;margin:25px 0}.hero h1 strong{color:#fff}.hero p{max-width:560px;color:#aaa0ad;font-size:18px;line-height:1.7}.actions{display:flex;gap:12px;margin:28px 0;flex-wrap:wrap}.hero> .wrap small{color:#6f6574}.visual{display:grid;place-items:center;min-height:440px}.crystal{width:320px;height:400px;border:1px solid #b84dff66;background:linear-gradient(145deg,#ffffff10,#9c16ff18);clip-path:polygon(0 8%,75% 0,100% 28%,83% 100%,10% 91%);display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 0 100px #8a18ff35,inset 0 0 80px #a900ff18;transform:rotate(-5deg)}.crystalF{font-size:210px;line-height:1;font-weight:1000;color:#12051b;text-shadow:0 0 2px #fff,0 0 18px #c34cff,0 0 50px #7b00ff}.crystal span{letter-spacing:.25em;font-size:11px}.crystal b{margin-top:8px;color:#a99cb2;font-size:10px}.section{padding:110px 0}.head{display:flex;justify-content:space-between;gap:30px;align-items:end;margin-bottom:45px}.head h2,.download h2{font-size:56px;line-height:.95;margin:15px 0}.head em{color:#a650ff;font-style:normal}.head p{max-width:430px;color:#8f8596;line-height:1.7}.cards,.prices{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.cards article,.price{position:relative;border:1px solid #ffffff10;background:#ffffff04;border-radius:20px;padding:28px}.cards article:hover,.price:hover{border-color:#a94cff44}.cards i{font-style:normal;color:#7f7488;font-size:12px}.cards h3{font-size:23px;margin-top:60px}.cards p,.price p{color:#8f8596;line-height:1.6}.prices{grid-template-columns:repeat(4,1fr)}.price strong{display:block;font-size:40px;margin:18px 0}.featured{background:linear-gradient(145deg,#9b24ff16,#ffffff04);border-color:#9b4cff55}.featured label{position:absolute;right:18px;top:18px;font-size:9px;background:#8e2cff;color:#fff;padding:5px 8px;border-radius:20px}.download{padding:40px 0 110px}.downloadBox{border:1px solid #ffffff12;border-radius:25px;padding:45px;display:flex;justify-content:space-between;align-items:center;background:radial-gradient(circle at 80% 50%,#761cff22,transparent 45%),#ffffff04}.downloadBox p{color:#8f8596}.download h2{font-size:44px}footer{border-top:1px solid #ffffff10;padding:28px 0;color:#655c6d;font-size:11px;display:flex}footer .wrap{display:flex;justify-content:space-between}.modal{position:fixed;inset:0;z-index:20;display:grid;place-items:center}.hidden{display:none!important}.backdrop{position:absolute;inset:0;background:#000b;backdrop-filter:blur(10px)}.box{position:relative;width:min(460px,92%);background:#0d0813;border:1px solid #ffffff18;border-radius:22px;padding:32px;box-shadow:0 30px 100px #000}.close{position:absolute;right:16px;top:12px;border:0;background:none;color:#aaa;font-size:30px;cursor:pointer}.box h2{font-size:38px;margin:12px 0}.box label{display:block;color:#918597;font-size:12px;margin:15px 0}.box input,.box select{display:block;width:100%;margin-top:7px;background:#050207;border:1px solid #ffffff15;border-radius:10px;padding:13px;color:#fff;outline:0}.box input:focus{border-color:#9a3dff}.full{width:100%;margin-top:10px}.modalLogo{display:flex;align-items:center;gap:10px;margin-bottom:30px}.modalLogo span{width:38px;height:38px;clip-path:polygon(18% 0,100% 0,70% 35%,100% 35%,62% 100%,0 100%,31% 50%,0 50%)}.modalLogo b{letter-spacing:.12em}.box p{color:#7f7488}.link{border:0;background:none;color:#b35cff;cursor:pointer}.profile{display:flex;align-items:center;gap:15px;padding:18px 0}.avatar{width:50px;height:50px;border-radius:14px}.profile small{display:block;color:#817689;margin-top:5px}.status{color:#6cff9a;margin:15px 0}.admin{border-top:1px solid #ffffff10;padding-top:18px;margin-top:18px}.admin pre{white-space:pre-wrap;color:#b96cff}.toast{position:fixed;right:20px;bottom:20px;background:#17101e;border:1px solid #ffffff18;border-radius:12px;padding:14px 18px;z-index:50;box-shadow:0 15px 50px #000}.noise{pointer-events:none;position:fixed;inset:0;z-index:100;opacity:.025;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence baseFrequency='.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
@media(max-width:850px){nav{display:none}.heroGrid{grid-template-columns:1fr}.visual{min-height:320px}.crystal{width:250px;height:310px}.crystalF{font-size:170px}.cards,.prices{grid-template-columns:1fr 1fr}.head,.downloadBox{display:block}.downloadBox .btn{margin-top:20px}}@media(max-width:560px){.cards,.prices{grid-template-columns:1fr}.hero h1{font-size:58px}.head h2{font-size:42px}.downloadBox{padding:28px}.nav{height:65px}}
'''

JS = r'''const $=s=>document.querySelector(s), tokenKey="fly_token", userKey="fly_user";
const toast=m=>{const t=$("#toast");t.textContent=m;t.classList.remove("hidden");clearTimeout(window.tt);window.tt=setTimeout(()=>t.classList.add("hidden"),2800)};
const user=()=>{try{return JSON.parse(localStorage.getItem(userKey)||"null")}catch{return null}};
const save=d=>{localStorage.setItem(tokenKey,d.token);localStorage.setItem(userKey,JSON.stringify(d.user))};
const clear=()=>{localStorage.removeItem(tokenKey);localStorage.removeItem(userKey)};
async function api(path,opts={}){const h={"Content-Type":"application/json",...(opts.headers||{})};const t=localStorage.getItem(tokenKey);if(t)h.Authorization="Bearer "+t;const r=await fetch("/api"+path,{...opts,headers:h});let d={};try{d=await r.json()}catch{}if(!r.ok)throw Error(d.error||"Ошибка сервера");return d}
function openAuth(reg=false){$("#authModal").classList.remove("hidden");$("#loginView").classList.toggle("hidden",reg);$("#registerView").classList.toggle("hidden",!reg)}
function update(){const u=user();$("#authBtn").textContent=u?u.username:"Войти"}
$("#authBtn").onclick=()=>{if(user()){$("#accountModal").classList.remove("hidden");const u=user();$("#name").textContent=u.username;$("#role").textContent=u.is_admin?"Администратор":"Пользователь";$("#avatar").textContent=u.username[0].toUpperCase();$("#adminBox").classList.toggle("hidden",!u.is_admin)}else openAuth()};
$("#registerHero").onclick=()=>openAuth(true);$("#closeAuth").onclick=()=>$("#authModal").classList.add("hidden");$("#closeAccount").onclick=()=>$("#accountModal").classList.add("hidden");$("#showRegister").onclick=()=>openAuth(true);$("#showLogin").onclick=()=>openAuth(false);
$("#registerBtn").onclick=async()=>{const u=$("#regUser").value.trim(),p=$("#regPass").value,p2=$("#regPass2").value;if(p!==p2)return toast("Пароли не совпадают");try{save(await api("/register",{method:"POST",body:JSON.stringify({username:u,password:p})}));$("#authModal").classList.add("hidden");update();toast("Регистрация успешна")}catch(e){toast(e.message)}};
$("#loginBtn").onclick=async()=>{try{save(await api("/login",{method:"POST",body:JSON.stringify({username:$("#loginUser").value.trim(),password:$("#loginPass").value})}));$("#authModal").classList.add("hidden");update();toast("Вход выполнен")}catch(e){toast(e.message)}};
$("#logout").onclick=()=>{clear();$("#accountModal").classList.add("hidden");update();toast("Вы вышли")};
$("#makeKey").onclick=async()=>{try{const d=await api("/admin/keys",{method:"POST",body:JSON.stringify({days:$("#keyDays").value})});$("#keyResult").textContent=d.key;toast("Ключ создан")}catch(e){toast(e.message)}};
document.querySelectorAll(".buy").forEach(b=>b.onclick=()=>user()?toast("Тариф выбран — активация доступна после оплаты"):openAuth());$("#downloadBtn").onclick=()=>user()?toast("Загрузка появится после публикации файла клиента"):openAuth();update();
'''

@app.get("/")
def index(): return Response(HTML, mimetype="text/html")
@app.get("/style.css")
def style(): return Response(CSS, mimetype="text/css")
@app.get("/script.js")
def script(): return Response(JS, mimetype="application/javascript")

def db():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c

def init():
    c=db(); c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE NOT NULL,password TEXT NOT NULL,is_admin INTEGER NOT NULL DEFAULT 0,created TEXT NOT NULL)")
    c.execute("CREATE TABLE IF NOT EXISTS keys(id INTEGER PRIMARY KEY AUTOINCREMENT,key TEXT UNIQUE NOT NULL,days TEXT NOT NULL,created TEXT NOT NULL,used INTEGER NOT NULL DEFAULT 0)")
    if not c.execute("SELECT 1 FROM users WHERE username=?",(ADMIN_USER,)).fetchone():
        c.execute("INSERT INTO users(username,password,is_admin,created) VALUES(?,?,1,?)",(ADMIN_USER,generate_password_hash(ADMIN_PASS),datetime.datetime.now(datetime.timezone.utc).isoformat()))
    c.commit(); c.close()

def token_for(u):
    return jwt.encode({"sub":u["id"],"username":u["username"],"is_admin":bool(u["is_admin"]),"exp":datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(days=7)},JWT_SECRET,algorithm="HS256")

def auth(admin=False):
    h=request.headers.get("Authorization","")
    if not h.startswith("Bearer "): return None
    try:
        p=jwt.decode(h[7:],JWT_SECRET,algorithms=["HS256"])
        return p if (not admin or p.get("is_admin")) else None
    except Exception:return None

@app.get("/api/health")
def health(): return jsonify(ok=True)
@app.post("/api/register")
def register():
    d=request.get_json(silent=True) or {}; u=str(d.get("username","")).strip(); p=str(d.get("password",""))
    if not 3<=len(u)<=32:return jsonify(error="Логин должен быть от 3 до 32 символов"),400
    if len(p)<8:return jsonify(error="Пароль должен быть минимум 8 символов"),400
    if u.lower()==ADMIN_USER.lower():return jsonify(error="Этот логин зарезервирован"),400
    c=db()
    try:
        cur=c.execute("INSERT INTO users(username,password,is_admin,created) VALUES(?,?,0,?)",(u,generate_password_hash(p),datetime.datetime.now(datetime.timezone.utc).isoformat()));c.commit();row=c.execute("SELECT * FROM users WHERE id=?",(cur.lastrowid,)).fetchone()
    except sqlite3.IntegrityError:c.close();return jsonify(error="Такой логин уже занят"),409
    c.close();return jsonify(token=token_for(row),user={"id":row["id"],"username":row["username"],"is_admin":False})
@app.post("/api/login")
def login():
    d=request.get_json(silent=True) or {}; c=db();u=c.execute("SELECT * FROM users WHERE username=?",(str(d.get("username","")).strip(),)).fetchone();c.close()
    if not u or not check_password_hash(u["password"],str(d.get("password",""))):return jsonify(error="Неверный логин или пароль"),401
    return jsonify(token=token_for(u),user={"id":u["id"],"username":u["username"],"is_admin":bool(u["is_admin"])})
@app.post("/api/admin/keys")
def make_key():
    if not auth(True):return jsonify(error="Доступ запрещён"),403
    d=request.get_json(silent=True) or {};days=str(d.get("days",""))
    if days not in {"30","180","365","forever"}:return jsonify(error="Неверный срок"),400
    key="FLY-"+"-".join(secrets.token_hex(2).upper() for _ in range(3));c=db();c.execute("INSERT INTO keys(key,days,created) VALUES(?,?,?)",(key,days,datetime.datetime.now(datetime.timezone.utc).isoformat()));c.commit();c.close();return jsonify(key=key,days=days)

init()

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int(os.getenv("PORT","8080")))
