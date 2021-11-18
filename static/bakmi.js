
submit = document.querySelector("#submitmixer");
console.log(submit);
legacy = document.getElementById("legacy").innerHTML;
mode = document.getElementById("mode");
submit.addEventListener('click', function(){
    console.log("pressed")
    if (mode.value != undefined || legacy.length >= 2){
        $.get('/combine?k='+legacy+'&c='+mode.value, function(message){
            html = document.getElementById("combineDisplay");
            display = ""
            message.forEach(element => {
                
                display += "<p>"+element+"</p>";
                console.log(display);
                
            });
            html.innerHTML = display
        })
    }
})