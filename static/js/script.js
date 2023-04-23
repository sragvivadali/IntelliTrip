function unhideGroupForm(formNum) {
    if(formNum != 0) {
        document.getElementById("create-group-div").style.display = "none";
        document.getElementById("join-group-div").style.display = "block";
    } else {
        document.getElementById("create-group-div").style.display = "block";
        document.getElementById("join-group-div").style.display = "none";
    }
}

function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
  }
  
  // Close the dropdown if the user clicks outside of it
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }

var data = 0;
  
//printing default value of data that is 0 in h2 tag
document.getElementById("counting").innerText = data;
  
//creation of increment function
function increment() {
    data = data + 1;
    document.getElementById("counting").innerText = data;
}
//creation of decrement function
function decrement() {
    if (data == 1)
        data = 1;
    else
        data = data - 1;
    document.getElementById("counting").innerText = data;
}

function searchDestination() {
  window.open('/visit:' + document.getElementById("searchBar").value + ',' + document.getElementById('counting').innerHTML, "_self");
}