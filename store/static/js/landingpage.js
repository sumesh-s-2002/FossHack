//ui elements
const rightFeaturedUI = document.querySelector(".featured-product .scroll-right"),
    leftFeaturedtUI = document.querySelector(".featured-product .scroll-left"),
    rightLatestUI = document.querySelector(".latest-product .scroll-right"),
    leftLatestUI = document.querySelector(".latest-product .scroll-left"),
    containerUI = document.querySelectorAll(".product-container")

rightFeaturedUI.addEventListener("click",()=>{
    containerUI[0].scrollBy({
        top: 0,
        left: 250,
        behavior: 'smooth'
    });
})
leftFeaturedtUI.addEventListener("click",()=>{
    containerUI[0].scrollBy({
        top: 0,
        left: -250,
        behavior: 'smooth'
    });
})
rightLatestUI.addEventListener("click",()=>{
    containerUI[1].scrollBy({
        top: 0,
        left: 250,
        behavior: 'smooth'
    });
})
leftLatestUI.addEventListener("click",()=>{
    containerUI[1].scrollBy({
        top: 0,
        left: -250,
        behavior: 'smooth'
    });
})