---
layout: page
title: "Contribution Procedure Status"
permalink: /contribution_status
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
        height: 700px;
    }
</style>

<h1>Contribution Procedure Status Form</h1>

Please enter the same email address you used for the contribution procedure contact form.
This should be the address that has received an automatic response from us to confirm the successful submission of the form.

<form id="contrib_status_form">
    <label for="email">Email address:</label>
    <input id="email" type="email" name="email" required/>
    <input type="submit" />
</form>

> **Note**
> <br>
> This page uses JavaScript to handle your input. Please make sure to enable client-side usage.<br>
> Additionally, if you experience issues and receive a "Sorry, unable to open the file at present." Google Drive error, either log out of all your Google Accounts or open this page in incognito mode.
<h3 id="loading_text" style="display:none;">Loading...</h3>
<div id="contrib_procedure_container" style="display:none;">
  <iframe id="contribution_procedure_status"></iframe>
  <h3>Job Status Legend</h3>
  <table id="job_status_legend">
      <thead>
      <tr>
        <th>Status</th>
        <th>Description</th>
      </tr>
        <td><font color="orange">Pending</font></td>
        <td>The labeling job has been created but the annotator hasn't started it yet.</td>
      <tr>
        <td><font color="blue">In progress</font></td>
        <td>The labeling job is currently being annotated. Note that you need to submit a job for us to be able to review it.</td>
      </tr>
      <tr>
        <td><font color="red">To be reviewed</font></td>
        <td>The labeling job has been submitted for review. We will allocate time to review it as soon as possible.</td>
      </tr>
      <tr>
        <td><font color="green">On review</font></td>
        <td>The labeling job is currently being reviewed.</td>
      </tr>
      </thead>
      <tbody>
      </tbody>
    </table>
</div>
<script>
document.forms[0].onsubmit = function(event){
    event.preventDefault();
    // Hide position container
    document.getElementById("contrib_procedure_container").style.display = "none";
    // Show loading text
    document.getElementById("loading_text").style.display = "block";
    var team_email = document.getElementById("email").value;
    var  url = "https://script.google.com/macros/s/AKfycbwe9WgdWy_nsfyk1zC13pGc-ZnoJ4iRGvvJyIXZ2h4buI5MWLTL/exec" + "?email=" + team_email;
    // Set iframe target to HTML waiting position web app response
    var iframe = document.getElementById("contribution_procedure_status")
    iframe.src = url;
    iframe.onload = function() {
        //iframe.style.height = iframe.contentWindow.document.body.offsetHeight + 'px';
        // Hide loading text
        document.getElementById("loading_text").style.display = "none";
        // Unhide position container
        document.getElementById("contrib_procedure_container").style.display = "block";
    };
};
</script>
