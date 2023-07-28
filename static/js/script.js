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

// quiz create html

function quiz_create_list_answer_btn(id) {
  id = id[id.length - 1];
  answer_ul = document.getElementById('quiz-create-list-answer-' + id);
  answer_div = document.createElement('div');
  answer_div.className = 'mb-3 col-6';

  children = answer_ul.children;
  quiz_create_answer_input_count = 1;

  for(i = 0; i < children.length; i++){
    quiz_create_answer_input_count++;
  }

  answer_div.id = 'create-answer-' + id + '-' + quiz_create_answer_input_count;

  space = document.createElement('br');

  answer_label = document.createElement('label');
  answer_label.className = 'form-label answer-label';
  answer_label.innerHTML = 'Answer';

  answer_delete = document.createElement('a');
  answer_delete.className = 'btn btn-danger m-2';
  answer_delete.innerHTML = 'remove';
  answer_delete.id = 'quiz-create-answer-delete-btn-' + id + '-' + quiz_create_answer_input_count;
  answer_delete.addEventListener("click", function() {
    quiz_create_answer_delete_btn(this.id);
  });

  answer_input = document.createElement('input');
  answer_input.className = 'form-control';
  answer_input.type = 'text';
  answer_input.name = 'answer-body-' + id + '-' + quiz_create_answer_input_count;
  answer_input.required = true

  answer_label2 = document.createElement('label');
  answer_label2.className = 'form-label answer-label';
  answer_label2.innerHTML = 'Answer ';

  answer_input2 = document.createElement('input');
  answer_input2.className = '';
  answer_input2.type = 'checkbox';
  answer_input2.name = 'answer-correct-' + id + '-' + quiz_create_answer_input_count;

  answer_div.append(answer_label, answer_delete, answer_input,
                   answer_label2, answer_input2);
  answer_ul.append(answer_div);

}

function quiz_create_question_btn() {
  question_ul = document.getElementById('quiz-create-list-question');
  question_div = document.createElement('div');
  question_div.className = 'mb-3 col-6 quiz-create-page-question';

  children = question_ul.children;
  quiz_create_question_input_count = ++children.length;

  question_div.id = 'create-question-' + quiz_create_question_input_count;

  question_label = document.createElement('label');
  question_label.className = "form-label question-label";
  question_label.innerHTML = "Question " + quiz_create_question_input_count;

  space = document.createElement('br');
  question_delete = document.createElement('a');
  question_delete.innerHTML = 'remove';
  question_delete.className = 'btn btn-danger m-2 delete-question-btn';
  question_delete.id = 'quiz-create-question-delete-btn-' + quiz_create_question_input_count;
  question_delete.addEventListener("click", function() {
    quiz_create_question_delete_btn(this.id);
  });

  document.getElementById('quiz-number-of-question').value = quiz_create_question_input_count;

  question_input = document.createElement('input');
  question_input.className = 'form-control';
  question_input.type = 'text';
  question_input.name = 'question-body-' + quiz_create_question_input_count;
  question_input.required = true

  // nested answer of question

  answer_ul = document.createElement('div');
  answer_ul.id = 'quiz-create-list-answer-' + quiz_create_question_input_count;
  answer_ul.className = 'row quiz-create-list-answer';
  answer_div = document.createElement('div');
  answer_div.className = 'mb-3 col-6';

  answer_label = document.createElement('label');
  answer_label.className = 'form-label answer-label';
  answer_label.innerHTML = 'Answer';

  answer_btn = document.createElement('a');
  answer_btn.className = 'btn btn-primary m-2';
  answer_btn.innerHTML = 'Add';
  answer_btn.id = 'quiz-create-list-btn-' + quiz_create_question_input_count;
  // answer_btn.addEventListener("click", quiz_create_list_answer_btn);
  answer_btn.addEventListener("click", function() {
    quiz_create_list_answer_btn(this.id);
  });

  answer_input_body = document.createElement('input');
  answer_input_body.className = 'form-control';
  answer_input_body.type = 'text';
  answer_input_body.name = 'answer-body-' + quiz_create_question_input_count + '-1';
  answer_input_body.required = true

  answer_label2 = document.createElement('label');
  answer_label2.className = 'form-label answer-label';
  answer_label2.innerHTML = 'Answer';
  
  answer_input_check = document.createElement('input');
  answer_input_check.type = 'checkbox';
  answer_input_check.className = '';
  answer_input_check.name = 'answer-body-' + quiz_create_question_input_count + '-1';

  answer_div.append(answer_label, answer_btn, answer_input_body,
                    answer_label2, answer_input_check)
  
  answer_ul.append(answer_div);


  question_div.append(question_label, question_delete,
    question_input, answer_ul);
  question_ul.append(question_div);

  quiz_create_question_input_count++;
}

function quiz_create_answer_delete_btn(id) {
  id = id.slice(29, id.length);
  create_answer_div = document.getElementById('create-answer' + id);
  create_answer_div.remove();
}

function quiz_create_question_delete_btn(id) {
  id = id[id.length - 1];
  create_question_div = document.getElementById('create-question-' + id);
  create_question_div.remove();

  question_labels = [...document.getElementsByClassName('question-label')];

  for(let [index, label] of question_labels.entries()) {
    index = index + 2;
    label.innerHTML = 'Question ' + index;
  }

}
