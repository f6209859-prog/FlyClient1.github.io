// ВАЖНО: после публикации backend замени эту строку на адрес своего API.
const API="https://YOUR-BACKEND-URL.example.com/api";
const $=s=>document.querySelector(s);
const tokenKey="fly_token";
const userKey="fly_user";

function toast(m){const t=$("#toast");t.textContent=m;t.classList.remove("hidden");setTimeout(()=>t.classList.add("hidden"),2800)}
function saveSession(data){localStorage.setItem(tokenKey,data.token);localStorage.setItem(userKey,JSON.stringify(data.user))}
function session(){try{return JSON.parse(localStorage.getItem(userKey)||"null")}catch{return null}}
function clearSession(){localStorage.removeItem(tokenKey);localStorage.removeItem(userKey)}
async function api(path,options={}){const headers={"Content-Type":"application/json",...(options.headers||{})};const token=localStorage.getItem(tokenKey);if(token)headers.Authorization="Bearer "+token;const r=await fetch(API+path,{...options,headers});let data={};try{data=await r.json()}catch{}if(!r.ok)throw new Error(data.error||"Ошибка сервера");return data}

function openAuth(mode){$("#authModal").classList.remove("hidden");$("#loginView").classList.toggle("hidden",mode!=="login");$("#registerView").classList.toggle("hidden",mode!=="register")}
function closeAuth(){$("#authModal").classList.add("hidden")}
function updateButton(){const u=session();$("#authBtn").textContent=u?u.username:"Войти"}
async function refreshAccount(){const u=session();if(!u)return;$("#accountName").textContent=u.username;$("#accountRole").textContent=u.is_admin?"Администратор":"Пользователь";$("#avatarLetter").textContent=(u.username||"F").charAt(0).toUpperCase();$("#adminBox").classList.toggle("hidden",!u.is_admin)}

$("#authBtn").onclick=async()=>{if(session()){$("#accountModal").classList.remove("hidden");await refreshAccount()}else openAuth("login")};
$("#registerHero").onclick=()=>openAuth("register");
$("#closeAuth").onclick=closeAuth;
$("#closeAccount").onclick=()=>$("#accountModal").classList.add("hidden");
$("#showRegister").onclick=()=>openAuth("register");
$("#showLogin").onclick=()=>openAuth("login");

$("#registerBtn").onclick=async()=>{
 const username=$("#regUser").value.trim(),password=$("#regPass").value,password2=$("#regPass2").value;
 if(username.length<3)return toast("Логин минимум 3 символа");
 if(password.length<8)return toast("Пароль минимум 8 символов");
 if(password!==password2)return toast("Пароли не совпадают");
 try{const d=await api("/register",{method:"POST",body:JSON.stringify({username,password})});saveSession(d);closeAuth();updateButton();toast("Регистрация успешна!")}catch(e){toast(e.message)}
};

$("#loginBtn").onclick=async()=>{
 const username=$("#loginUser").value.trim(),password=$("#loginPass").value;
 try{const d=await api("/login",{method:"POST",body:JSON.stringify({username,password})});saveSession(d);closeAuth();updateButton();toast("Вход выполнен!")}catch(e){toast(e.message)}
};

$("#makeKey").onclick=async()=>{
 try{const d=await api("/admin/keys",{method:"POST",body:JSON.stringify({days:$("#keyDays").value})});$("#keyResult").textContent=d.key;toast("Ключ создан")}catch(e){toast(e.message)}
};
$("#logoutBtn").onclick=()=>{clearSession();$("#accountModal").classList.add("hidden");updateButton();toast("Вы вышли")};

document.querySelectorAll(".buy").forEach(b=>b.onclick=()=>{if(!session())return openAuth("login");toast("Тариф выбран")});
$("#launcher").onclick=()=>toast("Ссылка на лаунчер будет добавлена после загрузки файла");
$("#mod").onclick=()=>toast("Ссылка на мод для ПК будет добавлена после загрузки файла");
updateButton();
