const total_pages = document.getElementById('total_pages').getAttribute('data-folder-id');
const page = document.getElementById('page').getAttribute('data-folder-id');
const folder_id = document.getElementById('folder_id').getAttribute('data-folder-id');
const actionButton = document.getElementById('actionButton');
const myContainer = document.getElementById('files-container');


if(parseInt(total_pages) > 1 && parseInt(page) < parseInt(total_pages)){
        actionButton.innerHTML = '<i class="fa-solid fa-play"></i>';
    } else {
        actionButton.innerHTML = '<i class="fa-solid fa-location-arrow"></i>';
    }

actionButton.onclick = () => {
    if(parseInt(total_pages) > 1 && parseInt(page) < parseInt(total_pages)){
        window.location.href = '/folders?id=' + folder_id + '&page=' + (parseInt(page) + 1);
    } else {
        myContainer.scrollTo({ top: 0, behavior: 'smooth' });
    }
};