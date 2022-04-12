<<<<<<< HEAD
$( document ).ready(function() {
    // var myModal = document.getElementById('exampleModal')
    // var myInput = document.getElementById('modal_button')

    // myModal.addEventListener('shown.bs.modal', function () {
    //     myInput.focus()
    // })

    // var toastElList = [].slice.call(document.querySelectorAll('.toast'))
    // var toastList = toastElList.map(function (toastEl) {
    //     return new bootstrap.Toast(toastEl, option)
    // })
    $("div[id^='myModal']").each(function(){
  
        var currentModal = $(this);
        console.log(currentModal);
        
        //click next
        currentModal.find('.btn-next').click(function(){
          currentModal.modal('hide');
          currentModal.closest("div[id^='myModal']").nextAll("div[id^='myModal']").first().modal('show'); 
        });

        //click prev
        currentModal.find('.btn-prev').click(function(){
          currentModal.modal('hide');
          
          currentModal.closest("div[id^='myModal']").prevAll("div[id^='myModal']").first().modal('show'); 
        });
      
        

      });
      document.onkeydown = function(event) {
        if(isModalOpened()){
            const key = event.key;
            var openedModal = $(".modal.fade.show");
            switch (event.key) {
                case "ArrowLeft":
                    openedModal.find('.btn-prev').click();
                    break;
                case "ArrowRight":
                    openedModal.find('.btn-next').click();
                    break;                
            }
        }
        
    };
});

function SwitchClass(id, _class){
    document.getElementById(id).classList.toggle(_class);
}

function openModal(id){
    $("div[id^='"+id+"']").modal("show");
}

function isModalOpened(){
    var modals = $("div[id^='myModal']");
    for(var i = 0; i < modals.length; i++){
        if(modals[i].style.display == "block") return true;
    }
    return false;
}

function showMessage(id){
    var element = $("#"+id)[0];
    element.classList.toggle("hide");
    element.classList.toggle("show");
}
=======
// $( document ).ready(function() {
//     var myModal = document.getElementById('exampleModal')
//     var myInput = document.getElementById('modal_button')

//     myModal.addEventListener('shown.bs.modal', function () {
//     myInput.focus()
//     })
// });
>>>>>>> c61ef00f9701dd6b6857a4e8888640c85e0eaf5f
