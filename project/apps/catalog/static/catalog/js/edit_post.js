function toggleEdit(postId){
    const viewDiv = document.getElementById(`cabeza-${postId}`).querySelector('.post-text.view');
    const editDiv = document.getElementById(`cabeza-${postId}`).querySelector('.post-text.edit');
    const button = document.getElementById(`EPBB-${postId}`);
    if(viewDiv.style.display === 'none'){
        viewDiv.style.display = 'block';
        editDiv.style.display = 'none';
    }
    else{
        viewDiv.style.display = 'none';
        editDiv.style.display = 'block';
    }

}
