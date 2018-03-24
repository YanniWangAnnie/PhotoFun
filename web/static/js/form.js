document.addEventListener('DOMContentLoaded',() =>{

   document.querySelector('#submit').disabled = true;

   document.querySelector('#exampleInputEmail1').onkeyup = () => {
    if(document.querySelector('#exampleInputEmail1').value.length > 0){
            document.querySelector('#submit').disabled = false;
    }
    else{
            document.querySelector('#submit').disabled = true;
    }
    };

   document.querySelector('#form').onsubmit =() =>{

        return true
   };
});