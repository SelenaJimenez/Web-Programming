function setchannel(data){
    localStorage.setItem('channel', data); 
            
}
document.addEventListener('DOMContentLoaded', () => {
// Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    
    if (!localStorage.getItem('username')){
        document.querySelector('#tpname').innerHTML=`
        <input id="name" placeholder="Type your name">
        <button class="btn btn-danger" id="btn">Log in!</button>
        `; 
            document.querySelector('#btn').onclick = function() {	
            var name=document.getElementById("name").value	
            localStorage.setItem('username', name);
            window.location="/"   
            
        };
        }
    else {
            ///show name
            var username=localStorage.getItem('username');
		    document.getElementById("printname").innerHTML='Welcome '+username+'! Lets Start';
            //Add channel
            document.querySelector('#tpname').innerHTML=`
            <button class="btn btn-danger" id="btn">Create channel</button>
            <input id="name" placeholder="Create a name for ur channel">
        `; 
    
    socket.on('connect', () => {
    //click on add channel
    
    document.querySelector('#btn').onclick = function() {	
            var name=document.getElementById("name").value;
            socket.emit('vote', name);	
            };
  
        // Send a message
    document.querySelector('#btnSM').onclick = function() {	
        var today = new Date();
        var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate()+" at: "+today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();;
            var msg=document.getElementById("nameSM").value;
            var username=localStorage.getItem('username');
            var channel=localStorage.getItem('channel');
            socket.emit('SMsend', {"name":username,"mess":msg,"date":date,"channel":channel});	
        };
    document.querySelector('#wakebtn').onclick = function() {	
            socket.emit('wake', 0);	
            };    
      
    });
    }
    // When a new vote is announced, add to the unordered list
    socket.on('vote totals', data => {
        let txt='';
        for (let i=0; i<data.length; i++){
            txt= `
            <li>
            <a href="/channel`+data[i]+`"> `+data[i]+` </a>
            </li> ` +txt; 
        }
        document.querySelector('#yes').innerHTML = txt;
       
    });
    socket.on('alert', data => {
      alert('The channel exist, create a channel with a different name')
       
    });
   
    socket.on('wake amigo', data=> {
       alert("Hey you!, answer me !")
    });    
   
    socket.on('msg totals', data=> {
        var temp="";
        let txt="";
        for (let i in data ){
            txt= `
            <h4> `+data[i]["name"]+` </h4>  
            <p>`+data[i]["mess"]+` </p>
            <p style="textsize"> `+data[i]["date"] +` </p>` +txt;
            temp=data[i]["channel"];
        }
        let chan=localStorage.getItem('channel')
        if(chan==temp){
            document.getElementById(chan).innerHTML = txt;
        }
       
    });
    
    
}
);


