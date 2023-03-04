const  numberInputs = document.querySelectorAll(".qty")

numberInputs.forEach(element =>{
    element.addEventListener("change", (e)=>{
        let id = element.dataset['cartid']
        updateCart(id , e.target.value)
    })
})

function updateCart(id , value){
    url = "/updatecart/"
    fetch(url, {
        method : "POST",
        headers : {
            "Content-Type" : "application/json",
            "X-CSRFToken" : csrftoken,
        },
        body : JSON.stringify({'id' : id, 'value' : value})
    }).then(res => res.json()).then(data =>{
        console.log(data);
    })
    if(+value <= 0){
        location.reload()
    }
}