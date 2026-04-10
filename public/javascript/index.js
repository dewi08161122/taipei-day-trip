const category__menu = document.querySelector(".category__menu");
const attractions__group = document.querySelector(".attractions__group");
const listItem__container = document.querySelector(".listItem__container");
const list__button_left = document.querySelector('.list__button-left');
const list__button_right = document.querySelector('.list__button-right');
const selector__word = document.querySelector(".selector__word");
const input__word = document.querySelector(".input__word");
const searchbtn = document.querySelector(".btn");
const footer = document.querySelector(".footer");
const attraction = document.querySelector(".attraction");

async function getHomepage() {
    let responseCategories=await fetch("/api/categories",{
        method:"GET"
    });
    let resultCategories=await responseCategories.json();
    resultCategories.data.forEach(category => {
        let category_tag=document.createElement("div"); // 建立放入文字的div
        category_tag.textContent=category; // 加上文字元素來源
        category_tag.classList.add("category__word"); // 加上文字使用的CSS
        category__menu.appendChild(category_tag); // 放入文字
    });

    let responseMrts=await fetch("/api/mrts",{
        method:"GET"
    });
    let resultMrts=await responseMrts.json();
    resultMrts.data.forEach(mrt => {
        let listItem=document.createElement("div");
        listItem.textContent=mrt; 
        listItem.classList.add("listItem");
        listItem__container.appendChild(listItem);
    });   
}
getHomepage();

let nextpage = 0; 
let loading = false;  // 防止重複載入
let nowcategory = null;
let nowkeyword = null;
async function loadAttractions(page, category, keyword) {
    if (loading || nextpage === null){
        return;
    } 
    loading = true;
    let result
    if(category==null && keyword==null){
        let response = await fetch(`/api/attractions?page=${page||0}`)
        result = await response.json()
    }else if(keyword==null){
        let response = await fetch(`/api/attractions?page=${page}&category=${category}`)
        result = await response.json()
    }else if(category==null){
        let response = await fetch(`/api/attractions?page=${page}&keyword=${keyword}`)
        result = await response.json()
    }else{let response = await fetch(`/api/attractions?page=${page}&category=${category}&keyword=${keyword}`)
        result = await response.json()
    }
    result.data.forEach(attractions => {
        let attraction = document.createElement("a");
        attraction.href = `/attraction/${attractions.id}`
        attraction.classList.add("attraction");

        let attraction__container = document.createElement("div");
        attraction__container.classList.add("attraction__container");

        let attraction__image = document.createElement("img");
        attraction__image.src = attractions.images[0];
        attraction__image.classList.add("attraction__image");

        let attraction__word = document.createElement("div");
        attraction__word.textContent = attractions.name;
        attraction__word.classList.add("attraction__word");

        attraction__container.appendChild(attraction__image);
        attraction__container.appendChild(attraction__word);

        let attraction__detail = document.createElement("div");
        attraction__detail.classList.add("attraction__detail");

        let left = document.createElement("div");
        left.textContent = attractions.mrt;
        left.classList.add("attraction__detail-leftword");

        let right = document.createElement("div");
        right.textContent = attractions.category;
        right.classList.add("attraction__detail-rightword");

        attraction__detail.appendChild(left);
        attraction__detail.appendChild(right);

        attraction.appendChild(attraction__container);
        attraction.appendChild(attraction__detail);

        attractions__group.appendChild(attraction);
    });
    nextpage = result.nextPage;
    loading = false;
    if (
        nextpage !== null &&
        footer.getBoundingClientRect().top < window.innerHeight  
    ) {
        loadAttractions(nextpage, nowcategory, nowkeyword);
    }
}
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            loadAttractions(nextpage, nowcategory, nowkeyword);
        }
    });
}, {
    root: null, 
    rootMargin: "0px",
    threshold: 0, 
});
observer.observe(footer);

selector__word.addEventListener('click', () => {
    category__menu.classList.toggle("open");  
}); 
category__menu.addEventListener('click', (event) => {
    if (event.target.classList.contains('category__word')) {
        selector__word.textContent = event.target.textContent + " ▼";
        category__menu.classList.remove('open');
    }
});
document.addEventListener('click', (event) => {
    if (!category__menu.contains(event.target) && !selector__word.contains(event.target)){ 
        category__menu.classList.remove('open');
    }
}); 

list__button_left.addEventListener('click', () => {
    listItem__container.scrollBy({ left: -100, behavior: 'smooth' });  
});
list__button_right.addEventListener('click', () => {
    listItem__container.scrollBy({ left: 100, behavior: 'smooth' });
}); 

listItem__container.addEventListener('click', (event) => {
    if (event.target.classList.contains('listItem')) {
        input__word.value = event.target.textContent;
    }
});

searchbtn.addEventListener('click', () => {
    let category=selector__word.textContent.replace(/\s+▼/g, "")
    let keyword=input__word.value.replace(/\s+/g, "")
    let page=0
    if (category=="全部分類"){
        category=null
    }
    if (keyword==""){
        keyword=null
    }
    attractions__group.innerHTML = "";
    nextpage = 0;  
    nowcategory = category; 
    nowkeyword = keyword;
    loadAttractions(page, nowcategory, nowkeyword);

});