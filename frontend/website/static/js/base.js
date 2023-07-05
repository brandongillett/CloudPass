console.log('Javascript linked')

// Flash message
function showFlashMessage(message, type) {
  const flashMessage = document.createElement('div');
  flashMessage.className = `alert ${type}`;
  flashMessage.innerHTML = `<span class="alert-closebtn">&times;</span>` +
    `<strong><i class="fa-solid fa-circle-${type === 'success' ? 'check' : 'exclamation'}"></i> ${type === 'success' ? 'Success' : 'Error'}!</strong> ${message}`;
  
  const closeButton = flashMessage.querySelector('.alert-closebtn');
  closeButton.addEventListener('click', function() {
    flashMessage.remove();
  });

  document.body.appendChild(flashMessage);

  setTimeout(function () {
    flashMessage.remove();
  }, 3000);
}

//dropdown content
document.addEventListener('DOMContentLoaded', function() {
  var dropdownBtn = document.querySelector('.dropdown-btn');
  var dropdownContent = document.querySelector('.dropdown-content');

  dropdownBtn.addEventListener('click', function() {
    dropdownContent.style.display = (dropdownContent.style.display === 'block') ? 'none' : 'block';
  });

  document.addEventListener('click', function(event) {
    if (!dropdownBtn.contains(event.target) && !dropdownContent.contains(event.target)) {
      dropdownContent.style.display = 'none';
    }
  });
});

//Alert notifications
var close = document.getElementsByClassName("alert-closebtn");
var i;

for (i = 0; i < close.length; i++) {
  close[i].onclick = function(){
    var div = this.parentElement;
    div.style.opacity = "0";
    setTimeout(function(){ div.style.display = "none"; }, 600);
  }
}

var alerts = document.getElementsByClassName("alert");
var j;

for (j = 0; j < alerts.length; j++) {
  var alert = alerts[j];
  setTimeout(function(){ alert.style.display = "none"; }, 3000);
}