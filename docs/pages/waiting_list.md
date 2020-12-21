---
layout: page
title: "Waiting List Status"
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

Please enter the same email address you used for the contribution procedure contact form.
This should be the address that has received an automatic response from us to confirm the successful submission of the form.

<form id="waiting_list_form">
    <label for="email">Email address:</label>
    <input id="email" type="email" name="email" required/>
    <input type="submit" />
</form>

> **Note**
> <br>
> This page uses JavaScript to handle your input. Please make sure to enable client-side usage.<br>
> Additionally, if you experience issues and receive a "Sorry, unable to open the file at present." Google Drive error, either log out of all your Google Accounts or open this page in incognito mode.
<h3 id="loading_text" style="display:none;">Loading...</h3>
<h3 id="waiting_list_title" style="display:none;">Your waiting list position is in the following range: </h3><iframe id="waiting_list_position"></iframe>

<script>
document.forms[0].onsubmit = function(event){
    event.preventDefault();
    // Show loading text
    document.getElementById("loading_text").style.display = "block";
    var team_email = document.getElementById("email").value;
    var  url = "https://script.google.com/macros/s/AKfycbzXJ_Y-oeg4-j-N0OqnziNfwolcht42pKblNiUwXFuAhWDuA6Q/exec" + "?email=" + team_email;
    // Set iframe target to HTML waiting position web app response
    document.getElementById("waiting_list_position").src = url;
    document.getElementById("waiting_list_position").onload = function() {
        // Hide loading text
        document.getElementById("loading_text").style.display = "none";
        // Unhide position text
        document.getElementById("waiting_list_title").style.display = "block";
    };
};
</script>
