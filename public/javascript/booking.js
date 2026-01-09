const title__word = document.querySelector(".title__word");
const headline = document.querySelector(".headline");
const attraction__title = document.querySelector(".attraction__title");
const bookingDate = document.getElementById("bookingDate");
const bookingTime = document.getElementById("bookingTime");
const price = document.getElementById("price");
const address = document.getElementById("address");
const username = document.getElementById("username");
const useremail = document.getElementById("useremail");
const account = document.getElementById("account");
const order__price = document.querySelector(".order__price");
const attraction__image = document.querySelector(".attraction__image");
const bookingDelete = document.querySelector(".delete");
const attraction = document.querySelector(".attraction");
const information = document.querySelector(".information");
const creditCard = document.querySelector(".creditCard");
const order = document.querySelector(".order");
const hrs = document.querySelectorAll("hr");
const footer = document.querySelectorAll(".footer");
const nobooking = document.querySelector(".nobooking");

const token = localStorage.getItem("token");

async function getBooking() {
    let responseUser=await fetch("/api/user/auth",{
        method:"GET",
        headers: {
        "Authorization": `Bearer ${token}`
        }
    });
    let responseBooking=await fetch("/api/booking",{
        method:"GET",
        headers: {
        "Authorization": `Bearer ${token}`
        }
    });
    let resultUser=await responseUser.json();
    let resultBooking=await responseBooking.json();
    if (resultUser.error){
        window.location.href = "/";
        return
    }else{
        headline.textContent="您好，"+resultUser.data.name+"，待預訂的行程如下："
        username.value=resultUser.data.name
        useremail.value=resultUser.data.email
    }
    if (resultBooking.data==null){
        attraction.classList.add("none");
        information.classList.add("none");
        creditCard.classList.add("none");
        order.classList.add("none");
        hrs.forEach(hr=>{
            hr.classList.add("none");
        })
        headline.classList.add("wide");
        nobooking.classList.remove("none");
    }else{
        attraction__title.textContent="台北一日遊："+resultBooking.data.attraction.name
        bookingDate.textContent=resultBooking.data.date
        bookingTime.textContent=resultBooking.data.time
        price.textContent="新台幣 "+resultBooking.data.price+" 元"
        address.textContent=resultBooking.data.attraction.address
        order__price.textContent="總價：新台幣 "+resultBooking.data.price+" 元"
        attraction__image.src = resultBooking.data.attraction.image;
    }
}
getBooking()

title__word.addEventListener("click", ()=>{
    window.location.href = "/";
});
bookingDelete.addEventListener("click", async()=>{
    let response= await fetch("/api/booking",{
        method:"DELETE",
        headers: {
        "Authorization": `Bearer ${token}`
        }
    })
    result=await response.json();
    if (result.ok){
        getBooking()
    }
})
account.addEventListener('click', ()=>{
    if (account.textContent.includes('登出系統')) {
        localStorage.setItem("token", "");
        window.location.reload();
        return
    }
})