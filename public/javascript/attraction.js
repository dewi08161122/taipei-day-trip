const image = document.querySelector(".image");
const profile__name = document.querySelector(".profile__name");
const profile__place = document.querySelector(".profile__place");
const description = document.querySelector(".description");
const address = document.querySelector(".address");
const transport = document.querySelector(".transport");
const input__word = document.querySelector(".input__word");
const date__img = document.querySelector(".date__img");
const title__word = document.querySelector(".title__word");
const time__button_up = document.querySelector(".time__button-up");
const time__button_down = document.querySelector(".time__button-down");
const price = document.querySelector(".price");
const attraction__image = document.querySelector(".attraction__image");
const indicator__bar = document.querySelector(".indicator__bar");
const image__button_left = document.querySelector(".image__button-left");
const image__button_right = document.querySelector(".image__button-right");

const id=window.location.pathname;
let images = [];
let bars = [];
let currentIndex = 0;
async function getAttractionpage() {
    let response=await fetch(`/api${id}`,{
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
    location.href = "/";
});

time__button_up.addEventListener("click", ()=>{
    time__button_up.style.backgroundColor="#448899";
    time__button_down.style.backgroundColor="#FFFFFF";
    price.textContent="新台幣 2000 元"
});
time__button_down.addEventListener("click", ()=>{
    time__button_up.style.backgroundColor="#FFFFFF";
    time__button_down.style.backgroundColor="#448899";
    price.textContent="新台幣 2500 元"
});