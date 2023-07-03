console.log(location.search) // lee los argumentos pasados a este formulario
var id=location.search.substr(4)
console.log(id)
const { createApp } = Vue
createApp({
data() {
return {
id:0,
nombre:"",
apellido:"",
edad:0,
email:"",
foto:"",
url:'https://alzaidel.pythonanywhere.com/personas/'+id,
}
},
methods: {
fetchData(url) {
fetch(url)
.then(response => response.json())
.then(data => {

console.log(data)
this.id=data.id;
this.nombre = data.nombre;
this.apellido=data.apellido;
this.edad=data.edad;
this.email=data.email;
this.foto=data.foto;
})
.catch(err => {
console.error(err);
this.error=true
})
},
modificar() {
let persona = {
nombre: this.nombre,
apellido: this.apellido,
edad: this.edad,
email: this.email,
foto: this.foto
}
var options = {
body: JSON.stringify(persona),
method: 'PUT',
headers: { 'Content-Type': 'application/json' },
redirect: 'follow'
}
fetch(this.url, options)
.then(function () {
alert("Registro modificado")
window.location.href = "../templates/personas.html";
})
.catch(err => {
console.error(err);
alert("Error al Modificar")
})
}
},
created() {
this.fetchData(this.url)
},
}).mount('#app')