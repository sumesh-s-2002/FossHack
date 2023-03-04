const buttons = document.querySelectorAll('.js');

for(let i = 0; i<buttons.length; i++){
    buttons[i].addEventListener("click", ()=>{
        let id = buttons[i].dataset["id"];
        let action = buttons[i].dataset["action"]
        if (user === "AnonymousUser"){
            window.alert("user is not logged in")
        }else{
            addToCart(id, action);
        }
    })
}
function addToCart(id , action){
    let url = "/addtocart/"
    fetch(url, {
        method: 'POST',
        headers: {'Content-Type' : 'application/json' ,
        'X-CSRFToken': csrftoken},
        body : JSON.stringify({'id' : id, 'action' : action})
    }).then(res=> {
        return res.json()
    }).then(data =>{
        console.log(data);
    })
}
