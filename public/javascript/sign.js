const account = document.getElementById("account"); // 抓id專用
const opacity = document.querySelector(".opacity");
const login = document.querySelector(".login");
const sgin = document.querySelector(".sgin");
const closes = document.querySelectorAll(".close");
const login__email = document.getElementById("login__email");
const login__password = document.getElementById("login__password");
const login__button = document.getElementById("login__button");
const login__word = document.getElementById("login__word");
const sgin__name = document.getElementById("sgin__name");
const sgin__email = document.getElementById("sgin__email");
const sgin__password = document.getElementById("sgin__password");
const sgin__button = document.getElementById("sgin__button");
const sgin__word = document.getElementById("sgin__word");
const token = localStorage.getItem("token");



login__button.addEventListener('click', async ()=>{
    let email=login__email.value
    let password=login__password.value
    if(email=="" || password==""){
        login__word.textContent="請輸入信箱和密碼，點此註冊"
        return;
    }
    let response=await fetch("/api/user/auth",{
        method:"PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body:JSON.stringify({"email":email, "password":password})
    });
    let result=await response.json();
    if (result.error){
        login__word.textContent=result.message + "，點此註冊";
        return;
    }
    localStorage.setItem("token", result.token);  // 儲存token到瀏覽器的LocalStorage
    window.location.reload();
})

sgin__button.addEventListener('click', async ()=>{
    let name=sgin__name.value
    let email=sgin__email.value
    let password=sgin__password.value
    if(name=="" || email=="" || password==""){
        sgin__word.textContent="請輸入完整資料，空白處都要填寫"
        return;
    }
    let response=await fetch("/api/user",{
        method:"POST",
        headers: {
            "Content-Type": "application/json"
        },
        body:JSON.stringify({"name":name, "email":email, "password":password})
    });
    let result=await response.json();
    if (result.error){
        sgin__word.textContent=result.message + "，點此登入"
    }else if(result.ok){
        sgin__word.textContent="註冊成功，點此登入"
    }
})

async function check() {
    const token = localStorage.getItem("token");
    let response=await fetch("/api/user/auth",{
        method: "GET",
        headers: {
        "Authorization": `Bearer ${token}`
        }
    })
    let result=await response.json();
    if (result.error){
        localStorage.setItem("token", "");
    }else if(result.ok){
        account.textContent="登出系統"
    }
}
check()

account.addEventListener('click', ()=>{
    if (account.textContent.includes('登出系統')) {
        localStorage.setItem("token", "");
        window.location.reload();
        return
    }
    login.style.display="block";
    opacity.style.display="block";
})
closes.forEach(close => {
    close.addEventListener("click", () => {
        login.style.display="none";
        sgin.style.display="none";
        opacity.style.display="none";
    });
});
login__word.addEventListener('click', ()=>{
    if (login__word.textContent.includes('點此註冊')) {
        login.style.display = "none";
        sgin.style.display = "block";
    }
});
sgin__word.addEventListener('click', ()=>{
    if (sgin__word.textContent.includes('點此登入')) {
        login.style.display = "block";
        sgin.style.display = "none";
    }
});




