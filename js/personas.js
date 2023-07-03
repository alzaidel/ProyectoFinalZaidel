const { createApp } = Vue
createApp({
data() {
return {
personas:[],
//url:'http://localhost:5000/productos',
// si el backend esta corriendo local usar localhost 5000(si no lo subieron a pythonanywhere)
url:'https://alzaidel.pythonanywhere.com/personas', // si ya lo subieron a pythonanywhere
error:false,
cargando:true,
/*atributos para el guardar los valores del formulario */
id:0,
nombre:"",
apellido:"",
edad:0,
email:"",
foto:"",
}
},
methods: {
fetchData(url) {
fetch(url)
.then(response => response.json())
.then(data => {
this.personas = data;
this.cargando=false
})
.catch(err => {
console.error(err);
this.error=true
})
},
eliminar(persona) {
const url = this.url+'/' + persona;
var options = {
method: 'DELETE',
}
fetch(url, options)
.then(res => res.text()) // or res.json()
.then(res => {
location.reload();
})
},
grabar(){
let persona = {
nombre: this.nombre,
apellido: this.apellido,
edad: this.edad,
email: this.email,
foto:this.foto
}
var options = {
body:JSON.stringify(persona),
method: 'POST',
headers: { 'Content-Type': 'application/json' },
redirect: 'follow'
}
fetch(this.url, options)
.then(function () {
alert("Registro grabado")
window.location.href = "../templates/personas.html";
})
.catch(err => {
console.error(err);
alert("Error al Grabar")
})
}
},
created() {
this.fetchData(this.url)
},
}).mount('#app')