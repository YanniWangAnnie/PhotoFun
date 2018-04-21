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

var _validFileExtensions = [".jpg", ".jpeg"];    
function ValidateSingleInput(oInput) {
    if (oInput.type == "file") {
        var sFileName = oInput.value;
         if (sFileName.length > 0) {
            var blnValid = false;
            for (var j = 0; j < _validFileExtensions.length; j++) {
                var sCurExtension = _validFileExtensions[j];
                if (sFileName.substr(sFileName.length - sCurExtension.length, sCurExtension.length).toLowerCase() == sCurExtension.toLowerCase()) {
                    blnValid = true;
                    break;
                }
            }
             
            if (!blnValid) {
                alert("Sorry, " + sFileName + " is invalid, allowed extensions are: " + _validFileExtensions.join(", "));
                oInput.value = "";
                return false;
            }
        }
    }
    return true;
}
