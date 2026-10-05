const $=s=>document.querySelector(s);
const $$=s=>document.querySelectorAll(s);
const toast=(m)=>{const t=$("#toast");t.textContent=m;t.classList.add("show");setTimeout(()=>t.classList.remove("show"),2400)};

const translations={
ru:{navFeatures:"Возможности",navDownload:"Скачать",navPricing:"Тарифы",login:"Войти",register:"Регистрация",heroTitle:"Fly Client — новый уровень Minecraft",heroText:"Современный клиент с удобным лаунчером, модом и личным кабинетом. Работает на компьютере и телефоне.",downloadNow:"Скачать сейчас",viewPlans:"Посмотреть тарифы",support:"Поддержка",access:"Доступ",featuresTitle:"Всё нужное в одном клиенте",featuresText:"Сделано просто: установил, вошёл и играешь.",f1:"Быстрый запуск",f1t:"Удобный лаунчер и быстрый доступ к игре.",f2:"Minecraft 1.21.11",f2t:"Основная версия клиента — 1.21.11.",f3:"PC + Mobile",f3t:"Адаптивный сайт для компьютера и телефона.",f4:"Личный кабинет",f4t:"Регистрация, вход и информация о подписке.",downloadTitle:"Два способа запуска",downloadText:"Выбирай вариант под своё устройство.",launcher:"Fly Launcher",launcherText:"Отдельный лаунчер клиента для Windows.",mod:"Обычный мод",modText:"Файл мода для установки в Minecraft.",download:"Скачать",pricingTitle:"Подписка Fly Client",pricingText:"Покупка будет подключена после настройки платёжной системы.",p30:"30 дней подписки",p180:"180 дней подписки",p1y:"1 год подписки",pLife:"Навсегда",soon:"Скоро",popular:"ПОПУЛЯРНО"},
en:{navFeatures:"Features",navDownload:"Download",navPricing:"Pricing",login:"Login",register:"Register",heroTitle:"Fly Client — a new level of Minecraft",heroText:"A modern client with a convenient launcher, mod and personal account. Works on PC and mobile.",downloadNow:"Download now",viewPlans:"View plans",support:"Support",access:"Access",featuresTitle:"Everything you need in one client",featuresText:"Simple: install, sign in and play.",f1:"Fast launch",f1t:"Convenient launcher and quick access to the game.",f2:"Minecraft 1.21.11",f2t:"Main supported client version — 1.21.11.",f3:"PC + Mobile",f3t:"Responsive website for computer and phone.",f4:"Personal account",f4t:"Registration, login and subscription information.",downloadTitle:"Two launch methods",downloadText:"Choose an option for your device.",launcher:"Fly Launcher",launcherText:"Standalone client launcher for Windows.",mod:"Regular mod",modText:"Mod file for installation in Minecraft.",download:"Download",pricingTitle:"Fly Client subscription",pricingText:"Purchasing will be connected after payment setup.",p30:"30 days",p180:"180 days",p1y:"1 year",pLife:"Lifetime",soon:"Soon",popular:"POPULAR"}};

let lang=localStorage.getItem("fly_lang")||"ru";
function applyLang(){
  document.documentElement.lang=lang; $("#langBtn").textContent=lang.toUpperCase();
  $$("[data-i18n]").forEach(e=>{const k=e.dataset.i18n;if(translations[lang][k])e.textContent=translations[lang][k]});
}
$("#langBtn").onclick=()=>{lang=lang==="ru"?"en":"ru";localStorage.setItem("fly_lang",lang);applyLang()};

const authModal=$("#authModal"), accountModal=$("#accountModal");
let authMode="login";
function openAuth(mode){authMode=mode;authModal.classList.remove("hidden");$("#authTitle").textContent=mode==="login"?"Войти":"Создать аккаунт";$("#authSubtitle").textContent=mode==="login"?"Войдите в аккаунт Fly Client":"Регистрация в Fly Client";$("#authSubmit").textContent=mode==="login"?"Войти":"Зарегистрироваться";$("#switchAuth").textContent=mode==="login"?"Нет аккаунта? Зарегистрироваться":"Уже есть аккаунт? Войти"}
$("#loginOpen").onclick=()=>openAuth("login");$("#registerOpen").onclick=()=>openAuth("register");$("#authClose").onclick=()=>authModal.classList.add("hidden");$("#accountClose").onclick=()=>accountModal.classList.add("hidden");
$("#switchAuth").onclick=()=>openAuth(authMode==="login"?"register":"login");

function getUsers(){return JSON.parse(localStorage.getItem("fly_users")||"[]")}
function saveUsers(u){localStorage.setItem("fly_users",JSON.stringify(u))}
function showAccount(nick){
  $("#accountNick").textContent=nick;
  const u=getUsers().find(x=>x.nick===nick);
  $("#accountPlan").textContent=u?.plan||"Нет подписки";
  $("#adminArea").classList.toggle("hidden",nick.toLowerCase()!=="noabot5");
  accountModal.classList.remove("hidden");
}
$("#authForm").onsubmit=e=>{
  e.preventDefault(); const nick=$("#authNick").value.trim(), pass=$("#authPass").value;
  const users=getUsers(), found=users.find(x=>x.nick.toLowerCase()===nick.toLowerCase());
  if(authMode==="register"){
    if(found)return toast("Такой никнейм уже зарегистрирован");
    users.push({nick,pass,plan:"Нет подписки"});saveUsers(users);localStorage.setItem("fly_current",nick);authModal.classList.add("hidden");toast("Аккаунт создан!");showAccount(nick);
  }else{
    if(!found||found.pass!==pass)return toast("Неверный никнейм или пароль");
    localStorage.setItem("fly_current",found.nick);authModal.classList.add("hidden");toast("Вы вошли в аккаунт");showAccount(found.nick);
  }
};
$("#logout").onclick=()=>{localStorage.removeItem("fly_current");accountModal.classList.add("hidden");toast("Вы вышли из аккаунта")};

$("#makeKey").onclick=()=>{
  const days=$("#keyDays").value;
  const chars="ABCDEFGHJKLMNPQRSTUVWXYZ23456789";let key="FLY-";
  for(let i=0;i<16;i++)key+=chars[Math.floor(Math.random()*chars.length)];
  const label=days==="life"?"Навсегда":days+" дней";
  $("#keyOutput").insertAdjacentHTML("afterbegin",`<div class="key-item">${key} — ${label}</div>`);
  toast("Ключ создан");
};

$$("[data-download]").forEach(b=>b.onclick=()=>{
  toast(b.dataset.download==="launcher"?"Файл лаунчера будет добавлен после публикации сборки.":"Файл мода будет добавлен после публикации сборки.");
});
$$(".buy").forEach(b=>b.onclick=()=>toast("Покупка пока недоступна — скоро будет подключена."));
const current=localStorage.getItem("fly_current"); if(current) $("#loginOpen").textContent=current;
applyLang();
