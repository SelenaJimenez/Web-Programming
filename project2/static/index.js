function setchannel(data){
    localStorage.setItem('channel', data);          
}

//Personal Touch
function sadM(num){
    var eWind = window.open("", "MsgWindow", "width=275,height=275");
    if (num==1){            //Sad
        eWind.document.write("<p>Why u saaaaad?</p> <img src='https://vignette.wikia.nocookie.net/mystic-messenger/images/d/d8/Ray_Emoji4.gif/revision/latest/scale-to-width-down/185?cb=20170918131327&path-prefix=es'>");
    }
    if(num==2){
        eWind.document.write("<p>I'm Happy too!</p> <img src='https://vignette.wikia.nocookie.net/mystic-messenger/images/5/57/Ray_Emoji2.gif/revision/latest/scale-to-width-down/183?cb=20170918131306&path-prefix=es'>");

    }
    if(num==3){
        eWind.document.write("<p>NO BAD WORDSSS!</p> <img src='https://66.media.tumblr.com/edfbf7bd07db5055856af88ee806d836/tumblr_p499jmaF9L1w611n8o2_400.gif'>");
    }

    if(num==4){
        eWind.document.write("<p>LOOOOOVEVEEEVEE!</p> <img src='https://media.tenor.com/images/47507646dff9f149e35afd759bc7653a/tenor.gif'>");
    }
}

document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);      //Connect to the socket!!

    
    if (!localStorage.getItem('username')){         //Calling to insert a name
        document.querySelector('#tpname').innerHTML=`
        <input id="name" placeholder="Insert your name">
        <button class="btn btn-danger" id="btn">Log in!</button>
        `;             
        document.querySelector('#btn').onclick = function() {	
        var name=document.getElementById("name").value	            //We save the names
        localStorage.setItem('username', name);
        window.location="/"   
            
        };
    }

    else {
        var username=localStorage.getItem('username');          //If there is already a name, we print it
        document.getElementById("printname").innerHTML='Welcome '+username+', start a channel!' ;
            
        document.querySelector('#tpname').innerHTML=`
        <button id="btn" class="btn btn-danger">Create channel</button>
        <input id="name" placeholder="Insert channel name">
        `; 
        
        socket.on('connect', () => {            //click on add channel
            document.querySelector('#btn').onclick = function() {	
            var name=document.getElementById("name").value;
            socket.emit('vote', name);	
        };
  
        //Write a message----------------------------------
        document.querySelector('#btnSM').onclick = function() {	
            var today = new Date();
            var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate()+" at: "+today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();;
            var msg=document.getElementById("nameSM").value;
            alert(msg);

            if(msg.indexOf(':c') != -1){
                num=1;
                sadM(num);
            }

            if(msg.indexOf(':D') != -1){
                num=2;
                sadM(num);
            }

            if(msg.indexOf('shit') != -1){
                num=3;
                sadM(num);
            }

            if(msg.indexOf('<3') != -1){
                num=4;
                sadM(num);
            }
            
            var username=localStorage.getItem('username');
            var channel=localStorage.getItem('channel');
            socket.emit('SMsend', {"name":username,"mess":msg,"date":date,"channel":channel});	
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
        document.querySelector('#yes').innerHTML = txt;             //If we want to go back to the active channel
       
    });
    
    socket.on('alert', data => {
      alert('This channel already exists, try again please')
       
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


