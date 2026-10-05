const modal=document.querySelector('#authModal');const form=document.querySelector('#authForm');const title=document.querySelector('#authTitle');const text=document.querySelector('#authText');const submit=form.querySelector('button[type=submit]');const switchBtn=document.querySelector('#switchAuth');const status=document.querySelector('#status');let register=false;
function openAuth(){modal.classList.add('open');modal.setAttribute('aria-hidden','false');setTimeout(()=>document.querySelector('#email').focus(),50)}
function closeAuth(){modal.classList.remove('open');modal.setAttribute('aria-hidden','true');status.textContent=''}
document.querySelectorAll('[data-open-auth]').forEach(b=>b.addEventListener('click',openAuth));
document.querySelector('[data-close-auth]').addEventListener('click',closeAuth);
modal.addEventListener('click',e=>{if(e.target===modal)closeAuth()});
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeAuth()});
switchBtn.addEventListener('click',()=>{register=!register;title.textContent=register?'Регистрация':'Вход в аккаунт';text.textContent=register?'Создай новый аккаунт.':'Войди, чтобы продолжить.';submit.textContent=register?'Зарегистрироваться':'Войти';switchBtn.textContent=register?'Уже есть аккаунт? Войти':'Нет аккаунта? Зарегистрироваться';status.textContent=''});
form.addEventListener('submit',e=>{e.preventDefault();const email=document.querySelector('#email').value.trim();status.textContent=register?`Аккаунт ${email} готов для подключения к серверу.`:`Добро пожаловать, ${email}!`;});
document.querySelector('#downloadBtn').addEventListener('click',()=>alert('Добавь файл клиента в проект и укажи ссылку на скачивание в script.js.'));
