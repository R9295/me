window.addEventListener('load', function(){
    fetch(window.profile_inc_url)
})
document.getElementById('description').innerHTML =
    marked(document.getElementById('description').innerHTML.trim())
