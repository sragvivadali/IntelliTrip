function unhideGroupForm(formNum) {
    if(formNum != 0) {
        document.getElementById("create-group-div").style.display = "none";
        document.getElementById("join-group-div").style.display = "block";
    } else {
        document.getElementById("create-group-div").style.display = "block";
        document.getElementById("join-group-div").style.display = "none";
    }
}