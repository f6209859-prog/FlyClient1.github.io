const API="https://YOUR-BACKEND-URL.example.com/api";
const $=s=>document.querySelector(s), $$=s=>document.querySelectorAll(s);
function modal(id,on=true){$("#"+id).classList.toggle("hide",!on)}
function toast(t){let x=$("#toast");x.textContent=t;x.classList.add("show");setTimeout(()=>x.classList.remove("show"),2500)}
function token(){return localStorage.getItem("fly_token")}
function setSession(data){localStorage.setItem("fly_token",data.token);localStorage.setItem("fly_user",JSON.stringify(data.user));refresh()}
function refresh(){let u=JSON.parse(localStorage.getItem("fly_user")||"null");$("#loginBtn").classList.toggle("hide",!!u);$("#accountBtn").classList.toggle("hide",!u)}
async function api(path,options={}){let r=await fetch(API+path,{...options,headers:{"Content-Type":"application/json",...(token()?{"Authorization":"Bearer "+token()}:{}),...(options.headers||{})}});let d=await r.json().catch(()=>({}));if(!r.ok)throw Error(d.error||"Ошибка сервера");return d}
$("#loginBtn").onclick=$("#heroLogin").onclick=()=>modal("auth");
$$("[data-close]").forEach(x=>x.onclick=()=>modal(x.dataset.close,false));
$$(".tabs button").forEach(b=>b.onclick=()=>{$$(".tabs button").forEach(x=>x.classList.remove("active"));b.classList.add("active");$("#login").classList.toggle("hide",b.dataset.tab!=="login");$("#register").classList.toggle("hide",b.dataset.tab!=="register")});
$("#login").onsubmit=async e=>{e.preventDefault();try{let d=await api("/login",{method:"POST",body:JSON.stringify({username:$("#loginUser").value,password:$("#loginPass").value})});setSession(d);modal("auth",false);toast("Вход выполнен")}catch(x){$("#loginError").textContent=x.message)}};
$("#register").onsubmit=async e=>{e.preventDefault();$("#regError").textContent="";if($("#regPass").value!==$("#regPass2").value){$("#regError").textContent="Пароли не совпадают";return}try{let d=await api("/register",{method:"POST",body:JSON.stringify({username:$("#regUser").value,password:$("#regPass").value})});setSession(d);modal("auth",false);toast("Аккаунт создан")}catch(x){$("#regError").textContent=x.message)}};
$("#accountBtn").onclick=async()=>{let u=JSON.parse(localStorage.getItem("fly_user")||"{}");$("#who").textContent=u.username||"Аккаунт";$("#role").textContent=u.isAdmin?"Администратор":"Пользователь";$("#admin").classList.toggle("hide",!u.isAdmin);modal("account")};
$("#logout").onclick=()=>{localStorage.clear();refresh();modal("account",false);toast("Вы вышли")};
$("#admin").onclick=()=>{modal("account",false);modal("adminPanel")};
$("#makeKey").onclick=async()=>{try{let d=await api("/admin/keys",{method:"POST",body:JSON.stringify({duration:$("#duration").value})});$("#key").textContent=d.key;toast("Ключ создан")}catch(x){toast(x.message)}};
$("#launcher").onclick=()=>toast("Ссылка на лаунчер будет добавлена после загрузки файла");
$("#mod").onclick=()=>toast("Ссылка на мод для ПК будет добавлена после загрузки файла");
refresh();