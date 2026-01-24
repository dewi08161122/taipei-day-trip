const title__word = document.querySelector(".title__word");
const planning = document.getElementById("booking");
const bookingTime = document.getElementById("account");
const headline = document.querySelector(".headline");
const order__status = document.querySelector(".order__status");

const token = localStorage.getItem("token");

let path = location.href;
orderId = path.split("=")[1];

async function getOrder() {
    try {
        let response = await fetch(`/api/order/${orderId}`,{
            method:"GET",
            headers: {
            "Authorization": `Bearer ${token}`
            }
        });
        let result=await response.json();
        if (result.data.status == "paid") {
        headline.textContent = "您好，"+result.data.contact.name+"，行程訂購成功：";
        order__status.textContent = `訂單編號：${orderId}`;
        } else {
        headline.textContent = "您好，"+result.data.contact.name+"，行程訂購失敗：";
        order__status.textContent = `訂單編號：${orderId}`;;
        }
    } catch (error) {
        console.log("error", error);
    }
}
getOrder()


title__word.addEventListener("click", ()=>{
    window.location.href = "/";
});
booking.addEventListener('click', ()=>{
    if (token == "") {
        window.location.href = "/";
    }else{
        window.location.href="/booking";
    }
})
account.addEventListener('click', ()=>{
    if (account.textContent.includes('登出系統')) {
        localStorage.setItem("token", "");
        window.location.href = "/";
        return
    }
})