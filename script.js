const $=s=>document.querySelector(s);
const usersKey="fly_client_users";
const currentKey="fly_client_current";

function users(){try{return JSON.parse(localStorage.getItem(usersKey)||"[]")}catch{return[]}}
function saveUsers(v){localStorage.setItem(usersKey,JSON.stringify(v))}
function toast(msg){const t=$("#toast");t.textContent=msg;t.classList.remove("hidden");setTimeout(()=>t.classList.add("hidden"),2600)}
function openAuth(mode="login"){$("#authModal").classList.remove("hidden");showAuth(mode)}
function closeAuth(){$("#authModal").classList.add("hidden")}
function showAuth(mode){$("#loginView").classList.toggle("hidden",mode!=="login");$("#registerView").classList.toggle("hidden",mode!=="register")}
function currentUser(){return localStorage.getItem(currentKey)}

function updateAuthButton(){
  const u=currentUser();
  $("#authBtn").textContent=u?u:"Войти";
}

$("#authBtn").onclick=()=>{
  if(currentUser()){
    $("#accountName").textContent=currentUser();
    $("#accountModal").classList.remove("hidden");
  }else openAuth("login");
};
$("#registerHero").onclick=()=>openAuth("register");
$("#closeAuth").onclick=closeAuth;
$("#closeAccount").onclick=()=>$("#accountModal").classList.add("hidden");
$("#showRegister").onclick=()=>showAuth("register");
$("#showLogin").onclick=()=>showAuth("login");

$("#registerBtn").onclick=()=>{
  const username=$("#regUser").value.trim();
  const password=$("#regPass").value;
  const password2=$("#regPass2").value;
  if(username.length<3)return toast("Логин должен быть минимум 3 символа");
  if(password.length<8)return toast("Пароль должен быть минимум 8 символов");
  if(password!==password2)return toast("Пароли не совпадают");
  const list=users();
  if(list.some(x=>x.username.toLowerCase()===username.toLowerCase()))return toast("Такой логин уже занят");
  list.push({username,password,created:new Date().toISOString()});
  saveUsers(list);
  localStorage.setItem(currentKey,username);
  closeAuth();
  updateAuthButton();
  toast("Регистрация успешна!");
};

$("#loginBtn").onclick=()=>{
  const username=$("#loginUser").value.trim();
  const password=$("#loginPass").value;
  const u=users().find(x=>x.username.toLowerCase()===username.toLowerCase()&&x.password===password);
  if(!u)return toast("Неверный логин или пароль");
  localStorage.setItem(currentKey,u.username);
  closeAuth();
  updateAuthButton();
  toast("Вы вошли в аккаунт!");
};

$("#logoutBtn").onclick=()=>{
  localStorage.removeItem(currentKey);
  $("#accountModal").classList.add("hidden");
  updateAuthButton();
  toast("Вы вышли из аккаунта");
};

document.querySelectorAll(".buy").forEach(btn=>btn.onclick=()=>{
  if(!currentUser())return openAuth("login");
  toast("Тариф выбран. Подключение оплаты можно добавить позже.");
});

$("#launcher").onclick=()=>toast("Ссылка на лаунчер будет добавлена после загрузки файла");
$("#mod").onclick=()=>toast("Ссылка на мод для ПК будет добавлена после загрузки файла");

updateAuthButton();
