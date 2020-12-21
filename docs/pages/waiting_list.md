---
layout: page
title: "Contribution Procedure Waiting List"
permalink: /waiting_list
feature-img: assets/img/fsg/HD/fsg_laptop.jpg
feature-img-credits: Photo ©FSG Sturm
slides: false
hide: true
bootstrap: false
---
<style>
    iframe{
        border-style: none;
        width: 100%;
    }
</style>

<h1>Waiting List Position Display</h1>
Please input the e-mail address you used for the contribution procedure contact form.
This should be the address that received an automatic response from us to confirm your application for contribution.
<form id="waiting_list_form">
    <label for="email">E-Mail Address:</label>
    <input id="email" type="email" name="email" required/>
    <input type="submit" />
</form>
<h3>Your waiting list position is: </h3><iframe id="waiting_list_position"></iframe>

<script>
document.forms[0].onsubmit = function(event){
    event.preventDefault();
    var team_email = document.getElementById("email").value;
    var  url = "https://script.google.com/macros/s/AKfycbzXJ_Y-oeg4-j-N0OqnziNfwolcht42pKblNiUwXFuAhWDuA6Q/exec" + "?email=" + team_email;
    console.log(team_email);
    document.getElementById("waiting_list_position").src = url;
};
</script>

