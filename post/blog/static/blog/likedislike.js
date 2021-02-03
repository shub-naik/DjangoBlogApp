function like(like_id){
    liked_id = like_id.split("+")[0];
    title = like_id.split("+")[1];
    $.ajax({
            url:'/like_dislike/',
            type:'GET',
            data:{"like_id":liked_id},
            datatype:"json"
    });
}

function dislike(dislike_id){
    disliked_id = dislike_id.split("+")[0];
    title = dislike_id.split("+")[1];
    $.ajax({
        url:'/like_dislike/',
        type:'GET',
        data:{"dislike_id":disliked_id},
        datatype:"json",
    });
}