$(function(){
$('#search').keyup(function(){
$.ajax({
        type:"GET",
        url:"/search/search/",
        contentType :'text/plain',
        data:{
            'search_text':$('#search').val(),
            'csrfmiddlewaretoken':$("input[name=csrfmiddlewaretoken]").val()
        },
        success:function(data,status){
                $('#search_items').html(data)
        },
        datatype:'html',
});
});
});

