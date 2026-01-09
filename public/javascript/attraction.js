const image = document.querySelector(".image");
const profile__name = document.querySelector(".profile__name");
const profile__place = document.querySelector(".profile__place");
const description = document.querySelector(".description");
const address = document.querySelector(".address");
const transport = document.querySelector(".transport");
const input__word = document.querySelector(".input__word");
const date__img = document.querySelector(".date__img");
const title__word = document.querySelector(".title__word");
const morning = document.getElementById("morning");
const afternoon = document.getElementById("afternoon");
const price = document.querySelector(".price");
const attraction__image = document.querySelector(".attraction__image");
const indicator__bar = document.querySelector(".indicator__bar");
const image__button_left = document.querySelector(".image__button-left");
const image__button_right = document.querySelector(".image__button-right");
const booking__button = document.querySelector(".booking__button");


const id = window.location.pathname.split("/").pop(); 
let images = [];
let bars = [];
let currentIndex = 0;
async function getAttractionpage() {
    let response=await fetch(`/api/attraction/${id}`,{
        method:"GET"
    });
    let result=await response.json();
    profile__name.textContent=result.data["name"];
    profile__place.textContent=`${result.data["category"]} at ${result.data["mrt"]}`;
    description.textContent=result.data["description"];
    address.textContent=result.data["address"];
    transport.textContent=result.data["transport"];

    result.data.images.forEach((img, index) => {
        const image = document.createElement("img");
        const bar = document.createElement("div");
        image.src = img;
        image.classList.add("image");
        attraction__image.prepend(image);
        images.push(image);

        bar.classList.add("bar");
        indicator__bar.appendChild(bar);
        bars.push(bar);

        if (index == 0) {
            image.classList.add("active");
            bar.classList.add("active");
        }
    })
}
getAttractionpage();

image__button_right.addEventListener("click", () => {
    let next = (currentIndex + 1) % images.length;
    showImage(next);
});

image__button_left.addEventListener("click", () => {
    let prev = (currentIndex - 1 + images.length) % images.length;
    showImage(prev);
});
function showImage(index) {
    images[currentIndex].classList.remove("active");
    bars[currentIndex].classList.remove("active");

    currentIndex = index;

    images[currentIndex].classList.add("active");
    bars[currentIndex].classList.add("active");
}

date__img.addEventListener("click", () => {
  input__word.showPicker(); // 直接打開日期選擇器
});

title__word.addEventListener("click", ()=>{
    window.location.href = "/";
});

morning.addEventListener("click", ()=>{
    morning.classList.add("active");
    afternoon.classList.remove("active");
    price.textContent="新台幣 2000 元"
});
afternoon.addEventListener("click", ()=>{
    afternoon.classList.add("active");
    morning.classList.remove("active");
    price.textContent="新台幣 2500 元"
});
booking__button.addEventListener("click", async()=>{
    let attractionId=id
    let bookingDate=input__word.value
    let bookingTime=""
    let bookingPrice=""
    if (morning.classList.contains("active")) {
        bookingTime="morning"
        bookingPrice="2000"
    } else if (afternoon.classList.contains("active")) {
        bookingTime="afternoon"
        bookingPrice="2500"
    }
    if (token == "") {
        login.style.display="block";
        opacity.style.display="block";
        return
    }else if(bookingDate==""){
        alert("請選擇日期");
        return;
    }else{
        let response=await fetch("/api/booking",{
        method: "POST",
        headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
        },
        body:JSON.stringify({"attractionId":attractionId, "bookingDate":bookingDate, "bookingTime":bookingTime, "price":bookingPrice})
        })
        let result=await response.json();
        if (result.ok){
            window.location.href="/booking";
            return
        } else if(result.error){
            alert(result.message);
            return;
        }
    }
});