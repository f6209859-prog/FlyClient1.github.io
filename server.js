require("dotenv").config?.();
const express=require("express"),cors=require("cors"),bcrypt=require("bcryptjs"),jwt=require("jsonwebtoken"),Database=require("better-sqlite3"),crypto=require("crypto");
const app=express(),db=new Database(process.env.DB_PATH||"flyclient.db");
const PORT=process.env.PORT||3000, SECRET=process.env.JWT_SECRET;
if(!SECRET||SECRET==="CHANGE_THIS_TO_A_LONG_RANDOM_SECRET") throw new Error("Set a strong JWT_SECRET in .env");
app.use(cors({origin:process.env.FRONTEND_ORIGIN==="*"||!process.env.FRONTEND_ORIGIN?true:process.env.FRONTEND_ORIGIN}));
app.use(express.json({limit:"20kb"}));
db.exec(`CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT UNIQUE NOT NULL,password_hash TEXT NOT NULL,role TEXT NOT NULL DEFAULT 'user',created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS keys(id INTEGER PRIMARY KEY AUTOINCREMENT,key TEXT UNIQUE NOT NULL,days INTEGER NOT NULL,created_at TEXT NOT NULL);`);
const adminUser=process.env.ADMIN_USERNAME||"noabot5", adminPass=process.env.ADMIN_PASSWORD;
if(!adminPass||adminPass.startsWith("CHANGE_")) console.warn("WARNING: set ADMIN_PASSWORD in .env");
if(adminPass&&!db.prepare("SELECT id FROM users WHERE username=?").get(adminUser)){
 const hash=bcrypt.hashSync(adminPass,12);db.prepare("INSERT INTO users(username,password_hash,role,created_at) VALUES(?,?,?,?)").run(adminUser,hash,"admin",new Date().toISOString());
}
function auth(req,res,next){try{const h=req.headers.authorization||"";if(!h.startsWith("Bearer "))throw 0;req.user=jwt.verify(h.slice(7),SECRET);next()}catch(e){res.status(401).json({message:"Требуется вход"})}}
function admin(req,res,next){if(req.user.role!=="admin")return res.status(403).json({message:"Нет доступа"});next()}
app.get("/api/health",(req,res)=>res.json({ok:true}));
app.post("/api/auth/register",(req,res)=>{
 const {username,password}=req.body||{};
 if(!/^[A-Za-z0-9_]{3,32}$/.test(username||""))return res.status(400).json({message:"Логин: 3–32 символа, только A-Z, 0-9 и _"});
 if(typeof password!=="string"||password.length<8)return res.status(400).json({message:"Пароль должен быть не короче 8 символов"});
 if(db.prepare("SELECT id FROM users WHERE username=?").get(username))return res.status(409).json({message:"Такой логин уже существует"});
 db.prepare("INSERT INTO users(username,password_hash,role,created_at) VALUES(?,?,?,?)").run(username,bcrypt.hashSync(password,12),"user",new Date().toISOString());
 res.json({ok:true});
});
app.post("/api/auth/login",(req,res)=>{
 const {username,password}=req.body||{},u=db.prepare("SELECT * FROM users WHERE username=?").get(username||"");
 if(!u||!bcrypt.compareSync(password||"",u.password_hash))return res.status(401).json({message:"Неверный логин или пароль"});
 const token=jwt.sign({id:u.id,username:u.username,role:u.role},SECRET,{expiresIn:"7d"});res.json({token});
});
app.get("/api/auth/me",auth,(req,res)=>res.json({user:{username:req.user.username,role:req.user.role}}));
app.get("/api/admin/keys",auth,admin,(req,res)=>res.json({keys:db.prepare("SELECT key,days,created_at FROM keys ORDER BY id DESC").all()}));
app.post("/api/admin/keys",auth,admin,(req,res)=>{
 const days=Number(req.body.days);if(![0,30,180,365].includes(days))return res.status(400).json({message:"Недопустимый срок"});
 let key;do{key="FLY-"+crypto.randomBytes(8).toString("hex").toUpperCase()}while(db.prepare("SELECT id FROM keys WHERE key=?").get(key));
 db.prepare("INSERT INTO keys(key,days,created_at) VALUES(?,?,?)").run(key,days,new Date().toISOString());res.json({key,days});
});
app.listen(PORT,()=>console.log(`Fly Client API: http://localhost:${PORT}`));