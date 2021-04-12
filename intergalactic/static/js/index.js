function toggle_comments(el){
    $this = $(el)
    var form = $this.parent().find('form')
    if (form.is(':visible')){
        form.addClass('hide')
    }
    else{
        form.removeClass('hide')
    }
}
