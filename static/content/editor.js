var edit  = document.querySelector('.edit')
var db_contents = document.querySelectorAll('.db_content');


function show(show_block){
    show_block.style.display = "block";
    show_block.style.opacity = "1";
    show_block.style.visibility = "visible";

}

function hide(show_block){
    show_block.style.display = 'none';
    show_block.style.opacity = "0"; 
    show_block.style.visibility = "hidden";
}


db_contents.forEach(function(db_content){
    db_content.insertAdjacentHTML('afterend', `
    <div class="show">
        <a href="${db_content.dataset.admin_url}" target="_blank">Редагувати</a>
    </div>
    `
    );
    var show_block = db_content.nextElementSibling
    show_block.addEventListener('mouseover', function(){
        show(show_block)
    })
    show_block.addEventListener('mouseout', function(){
        hide(show_block)
    })
    db_content.addEventListener('mouseover', function(){
        show(show_block)        
    })
    db_content.addEventListener('mouseout', function(e){
        hide(show_block)
    })
})


