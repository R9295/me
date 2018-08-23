var preview = $("#preview")
preview.on('click', function(event){
	event.preventDefault()
	image = $("input[type=file]")[0].files[0]
	if (image !== undefined){
	form = new FormData()
	form.append('image', image)
	form.append('csrfmiddlewaretoken', document.getElementsByName('csrfmiddlewaretoken')[0].value)
	$.ajax({
		url:'/theme/preview/image',
		type: 'POST',
		data: form,
    contentType: false,
    processData: false,
		success: function(data){
			if (data.error){
					alert('Please make sure your file is an image')
			} else {
				form_data = $('form').serialize()
				form_data = form_data + '&image='+ data.url
			  window.open('/theme/'+$("#id_theme").val()+'?'+form_data)
			}
		}
	})
} else {
	form_data = $('form').serialize()
	if ($("#image-clear_id").prop('checked')){
		form_data = form_data + '&image=clear'
	} else {
		form_data = form_data + '&image=none'
	}
	window.open('/theme/'+$("#id_theme").val()+'?'+form_data)
}
})
