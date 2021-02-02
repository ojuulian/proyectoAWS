/*console.log*/
const nombre= document.getElementById("name")
const username= document.getElementById("usuario")
const correo= document.getElementById("email")
const contraseña= document.getElementById("password")
const form= document.getElementById("form")
const parraf= document.getElementById("warnings")

form.addEventListener("submit", e=>{
    e.preventDefault()
    let warnings =""
    let entrar= false
    let regexEmail= /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/
    parraf.innerHTML=""
    if(nombre.value.length <6){
        warnings+='Escriba su nombre Completo <br>'
        entrar= true
    }
    if(username.value.length <8){
        warnings+='El usuario no es valido. Minimo 8 caracteres  <br>'
        entrar= true
    }
    console.log()
    if(regexEmail.test(correo.value)){
        warnings+='El email no es valido <br>'
        entrar= true
    }
    if(contraseña.value.length <8){
        warnings+='La contraseña no es valida. Minimo 8 caracteres  <br>'
        entrar= true
    }
    if (entrar){
        parraf.innerHTML= warnings
    }else {
        parraf.innerHTML= "Enviado"
    }    
})