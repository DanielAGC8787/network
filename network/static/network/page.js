document.addEventListener('DOMContentLoaded', function(){
    fetch('/posts')
    .then(response => response.json())
    .then(posts => {
        page_num = document.querySelector("#page_num").innerHTML
        pagePosts = []
        if (isNaN(page_num)){
            page_num = 1 
        } 
        for (let i = (page_num*10)-10; i < page_num*10; i++){
            pagePosts.push(posts[i])
        }
        var liked_post
        pagePosts.forEach(function callback(value, index){
            const heart = document.createElement('div')
            heart.setAttribute("class", "heart-like-button");
            heart.setAttribute("id", "heart"+index);
            document.querySelector('#container'+(index+1)).append(heart)

            heart.addEventListener("click", () => {
                if (heart.classList.contains("liked")) {
                    heart.classList.remove("liked")
                    dislikePost(posts[index].id, index);  
                } else {
                    heart.classList.add("liked")
                    likePost(posts[index].id, index);
                }
            });
        
            liked_post = pagePosts[index].liked
            if(liked_post){
                document.querySelector('#heart'+index).classList.add('liked');
            }

            if(pagePosts[index].currentUser == pagePosts[index].creator){
                const editButton = document.createElement('button')
                editButton.setAttribute('class', 'edit');
                document.querySelector('#edit'+(index+1)).append(editButton);
                editButton.innerHTML = "Edit"
                editButton.addEventListener('click', event => {
                    const input = document.createElement("input")
                    const save = document.createElement("button")
                    save.innerHTML = "Save"
                    input.setAttribute("type", "text");
                    input.setAttribute("class", "inputBox")
                    postBodyTag = editButton.parentElement.parentElement.nextSibling.nextSibling
                    console.log(postBodyTag)
                    wholePost = postBodyTag.parentElement
                    wholePost.append(save)
                    postBody = postBodyTag.innerHTML
                    postBodyTag.innerHTML = ""
                    editButton.style.display = "none"
                    postBodyTag.append(input)
                    input.value = postBody
                    save.addEventListener('click', event => {
                        editPost(input.value, posts[index].id)
                        save.remove()
                        editButton.style.display = "block"
                        postBodyTag.innerHTML = input.value
                        input.remove()

                    })
                })
            }

        })
    })
}); 

function unfollow(user){
    fetch('/get_user/' + user)
    .then(response => response.json())
    .then(logUser => {
        var followNum = logUser.followers.length
        followNum--
        fetch('/unfollow/' + logUser.username, {
            method: 'DELETE'
        })
        document.querySelector('#followNum').innerHTML = followNum
    })
}

function likePost(postID, index){
    var postLikes;
    fetch('/posts/' + postID)
    .then(response => response.json())
    .then(post => {
        postLikes = post.likes;
        postLikes++;
        fetch('/posts/'+postID, {
            method: 'PUT',
                body: JSON.stringify({
                    likes: postLikes,
                    liked: true
                })
        })
        document.querySelector('#like'+(index+1)).innerHTML = postLikes;
    });
}

function dislikePost(postID, index){
    var postLikes
    fetch('/posts/' + postID)
    .then(response => response.json())
    .then(post => {
        postLikes = post.likes;
        postLikes--;
        fetch('/posts/'+postID, {  
            method: 'PUT',
                body: JSON.stringify({
                    likes: postLikes,
                    liked: false
                })
        })
        document.querySelector('#like'+(index+1)).innerHTML = postLikes;
    });
}

function follow(followedUser){
    fetch('/get_user/' + followedUser)
    .then(response => response.json())
    .then(logUser => {
        var followNum = logUser.followers.length
        followNum++;
        fetch('/follow', {
            method: 'POST',
            body: JSON.stringify({
                following : followedUser
            })
        });
        document.querySelector('#followNum').innerHTML = followNum
    })
}

function editPost(newPost, postID){
    fetch('/posts/'+postID, {  
        method: 'PUT',
            body: JSON.stringify({
                body: newPost
            })
    })
}