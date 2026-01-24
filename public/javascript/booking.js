const title__word = document.querySelector(".title__word");
const headline = document.querySelector(".headline");
const attraction__title = document.querySelector(".attraction__title");
const bookingDate = document.getElementById("bookingDate");
const bookingTime = document.getElementById("bookingTime");
const price = document.getElementById("price");
const address = document.getElementById("address");
const username = document.getElementById("username");
const useremail = document.getElementById("useremail");
const userphone = document.getElementById("userphone");
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
const order__button = document.querySelector(".order__button");

const token = localStorage.getItem("token");
let totalTrip = {};
let totalPrice = 0;

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
        totalPrice=resultBooking.data.price
        totalTrip={
            "attraction": {
                "id": resultBooking.data.attraction.id,
                "name": resultBooking.data.attraction.name,
                "address": resultBooking.data.attraction.address,
                "image": resultBooking.data.attraction.image
            },
            "date": resultBooking.data.date,
            "time": resultBooking.data.time
        }
        attraction__title.textContent="台北一日遊："+resultBooking.data.attraction.name
        bookingDate.textContent=resultBooking.data.date
        bookingTime.textContent=resultBooking.data.time
        price.textContent="新台幣 "+resultBooking.data.price+" 元"
        address.textContent=resultBooking.data.attraction.address
        order__price.textContent="總價：新台幣 "+totalPrice+" 元"
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

order__button.addEventListener('click',function (event){
    let order = {
        price: totalPrice,
        trip: totalTrip,
        contact: {
            name: username.value,
            email: useremail.value,
            phone: userphone.value,
        },
    };
    if(username.value=="" || useremail.value=="" || userphone.value==""){
        alert("請填寫聯絡資訊");
        return;
    }
    event.preventDefault();
    const tappayStatus = TPDirect.card.getTappayFieldsStatus();
    if (tappayStatus.canGetPrime === false) {
        alert("信用卡資訊尚未填寫完整或錯誤");
        return;
    }
    TPDirect.card.getPrime((result) => {
        if (result.status !== 0) {
            console.error("TapPay 原始結果:", result);
            alert("信用卡授權失敗");
            return;
        }
        payment(order, result.card.prime);
    });
})

async function payment(order, prime) {
    try{
        let response = await fetch("/api/orders", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                prime: prime,
                order: order,
            }),
        });
        let result=await response.json();
        if (result.error){
            alert(result.message);
        }else{
            window.location.href = `/thankyou?number=${result.data.number}`;
        }
    }catch(err){
        console.error("前端解析錯誤:", err);
    }
}

TPDirect.setupSDK(
    166475,
    "app_abv2gWk7YtYvhFeniubht01fXYHoXU3zJFNTTkK0w5QV9lGHl6iMgoKzrswA",
    "sandbox",
    "127.0.0.1"
);

let fields = {
    number: {
        element: '#card-number',
        placeholder: '**** **** **** ****'
    },
    expirationDate: {
        element: document.getElementById('card-expiration-date'),
        placeholder: 'MM / YY'
    },
    ccv: {
        element: '#card-ccv',
        placeholder: 'ccv'
    }
}
TPDirect.card.setup({
    fields: fields,
    styles: {
        'input': {
            'color': 'gray'
        },
        '.valid': {
            'color': 'green'
        },
        '.invalid': {
            'color': 'red'
        },
        '@media screen and (max-width: 400px)': {
            'input': {
                'color': 'orange'
            }
        }
    },
    // 此設定會顯示卡號輸入正確後，會顯示前六後四碼信用卡卡號
    isMaskCreditCardNumber: true,
    maskCreditCardNumberRange: {
        beginIndex: 6,
        endIndex: 11
    }
})