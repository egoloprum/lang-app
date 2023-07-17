console.log("hello world");

  
const button = document.querySelector(".register-button");
const pass1 = document.querySelector(".register-password"),
pass2 = document.querySelector(".register-password2");

if(pass2){
  pass2.addEventListener("keyup", (e) => {
    if(pass1.value === pass2.value){
      button.removeAttribute("disabled");
    }
    else {
      button.setAttribute("disabled", "");
    }
  });
}

const profile_update_password = document.querySelector("#profile-update-password");
const profile_update_length = document.querySelector(".profile-update-requirement-1");
const profile_update_letters = document.querySelector(".profile-update-requirement-2");
const profile_update_cap_letters = document.querySelector(".profile-update-requirement-3");
const profile_update_numbers = document.querySelector(".profile-update-requirement-4");

profile_update_password.addEventListener("keyup", (e) => {
  var lowerCaseLetters = /[a-z]/g;
  var upperCaseLetters = /[A-Z]/g;
  var numbers = /[0-9]/g;
  var password = profile_update_password.value;

  if(password.length >= 8) {
    profile_update_length.style.color = "green";
    profile_update_length.style.fontWeight = 500;
  }
  else {
    profile_update_length.style.color = "grey";
    profile_update_length.style.fontWeight = 400;
  }

  if(password.match(lowerCaseLetters)) {
    profile_update_letters.style.color = "green";
    profile_update_letters.style.fontWeight = 500;
  }
  else {
    profile_update_letters.style.color = "grey";
    profile_update_letters.style.fontWeight = 400;
  }

  if(password.match(upperCaseLetters)) {
    profile_update_cap_letters.style.color = "green";
    profile_update_cap_letters.style.fontWeight = 500;
  }
  else {
    profile_update_cap_letters.style.color = "grey";
    profile_update_cap_letters.style.fontWeight = 400;
  }

  if(password.match(numbers)) {
    profile_update_numbers.style.color = "green";
    profile_update_numbers.style.fontWeight = 500;
  }
  else {
    profile_update_numbers.style.color = "grey";
    profile_update_numbers.style.fontWeight = 400;
  }

});
