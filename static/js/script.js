let current_url = window.location.href;
current_url = current_url.replace('http://127.0.0.1:8000/', '');
console.log(current_url);

let sidebar_scroll = localStorage.getItem('sidebarScroll');
const sidebar = document.getElementById("sidebar");
const sidebar_tags = document.getElementsByClassName("sidebar-tags");
const main_page = document.getElementById("main-page");
const sidebar_toggle = document.querySelector('#sidebar-toggle');

const enableScroll = () => {
  localStorage.setItem('sidebarScroll', 'enable');
  sidebar.style.width = '70px';
  main_page.style.marginLeft = '70px';
  for (let tag of sidebar_tags) {
    tag.style.display = 'None';
  }
}

const disableScroll = () => {
  localStorage.setItem('sidebarScroll', 'disable');
  sidebar.style.width = '250px';
  main_page.style.marginLeft = '250px';
  for (let tag of sidebar_tags) {
    tag.style.display = 'block';
  }
}

if (sidebar_scroll == 'enable') {
  enableScroll();
}

sidebar_toggle.addEventListener('click', () => {
  sidebar_scroll = localStorage.getItem('sidebarScroll');
  if (sidebar_scroll != 'enable') {
    enableScroll();
    console.log(sidebar_scroll);
  }
  else {
    disableScroll();
    console.log(sidebar_scroll);
  }
});

// course-edit.html
if (current_url.split('/').find((element) => element == 'course') == 'course') {
  function load_everyting() {
    tinymce.init({
      selector: 'textarea',
      plugins: 'ai tinycomments mentions anchor autolink charmap codesample emoticons image link lists media searchreplace table visualblocks wordcount checklist mediaembed casechange export formatpainter pageembed permanentpen footnotes advtemplate advtable advcode editimage tableofcontents mergetags powerpaste tinymcespellchecker autocorrect a11ychecker typography inlinecss',
      toolbar: 'undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | link image media table mergetags | align lineheight | tinycomments | checklist numlist bullist indent outdent | emoticons charmap | removeformat',
      tinycomments_mode: 'embedded',
      tinycomments_author: 'Author name',
      mergetags_list: [
        { value: 'First.Name', title: 'First Name' },
        { value: 'Email', title: 'Email' },
      ],
      ai_request: (request, respondWith) => respondWith.string(() => Promise.reject("See docs to implement AI Assistant"))
    });
  }
  function add_chapter(){
    chapter_side = document.getElementById("cour-chap-side");
    const q_number = ++chapter_side.children.length;

    accord_div = document.createElement("div");
    accord_div.className = "accordion accordion-flush";
    accord_div.setAttribute("style", "border-bottom: 1px solid #e4e4e4;");
    accord_div.setAttribute("id", "cour-chap-" + q_number);

    item_div = document.createElement("div");
    item_div.className = "accordion-item";

    accord_head = document.createElement("h2");
    accord_head.className = "accordion-header";

    accord_btn = document.createElement("a");
    accord_btn.className = "accordion-button collapsed";
    accord_btn.setAttribute("data-bs-toggle", "collapse");
    accord_btn.setAttribute("data-bs-target", "#cour-chap-" + q_number);
    accord_btn.setAttribute("aria-controls", "#cour-chap-" + q_number);

    accord_p = document.createElement("p");
    accord_p.innerHTML = q_number;

    accord_btn.appendChild(accord_p);
    accord_head.appendChild(accord_btn);

    flush_div = document.createElement("div");
    flush_div.className = "accordion-collapse collapse";
    flush_div.setAttribute('id', 'cour-chap-' + q_number);

    flush_body = document.createElement("div");
    flush_body.className = "accordion-body";
    flush_body.setAttribute("id", "cour-chap-" + q_number);

    q_label = document.createElement("label");
    q_label.innerHTML = "name";
    q_label.setAttribute("class", "me-3");

    q_input = document.createElement("p");
    q_input.className = "form-control me-3";
    q_input.setAttribute("name", "chap-name-" + q_number);

    del_btn = document.createElement("a");
    del_btn.className = "btn btn-light";
    del_btn.setAttribute("onclick", "del_chapter(this.id)");
    del_btn.setAttribute("id", "del-chapter-" + q_number);
    del_btn.setAttribute("style", "width: 250px;");
    
    del_i = document.createElement("i");
    del_i.className = "fa-solid fa-trash";

    del_span = document.createElement("span");
    del_span.innerHTML = " Delete Chapter";

    del_btn.appendChild(del_i);
    del_btn.appendChild(del_span);

    top_div = document.createElement("div");
    top_div.setAttribute("style", "display: flex; flex-direction: row;");
    top_div.setAttribute("class", "mb-3");
    top_div.appendChild(q_label);
    top_div.appendChild(q_input);
    top_div.appendChild(del_btn);

    e_label = document.createElement("label");
    e_label.innerHTML = "body";
    e_label.setAttribute("class", "mb-3 me-3");

    e_input = document.createElement("p");
    e_input.className = "mb-3 form-control";
    e_input.setAttribute("style", "width: 100%");
    e_input.setAttribute("name", "chap-body-" + q_number);

    mid_div = document.createElement("div");
    mid_div.setAttribute("style", "display: flex; flex-direction: row;");
    mid_div.setAttribute("class", "mb-3");
    mid_div.appendChild(e_label);
    mid_div.appendChild(e_input);

    flush_body.appendChild(top_div);
    flush_body.appendChild(mid_div);
    flush_div.appendChild(flush_body);

    item_div.appendChild(accord_head);
    item_div.appendChild(flush_div);

    accord_div.appendChild(item_div);
    chapter_side.appendChild(accord_div);
  }
  function del_chapter(id) {
    console.log(id);
  }
  function add_file() {
    chapter_side = document.getElementById("cour-file-side");
    const q_number = ++chapter_side.children.length;

    accord_div = document.createElement("div");
    accord_div.className = "accordion accordion-flush";
    accord_div.setAttribute("style", "border-bottom: 1px solid #e4e4e4;");
    accord_div.setAttribute("id", "cour-file-" + q_number);

    item_div = document.createElement("div");
    item_div.className = "accordion-item";

    accord_head = document.createElement("h2");
    accord_head.className = "accordion-header";

    accord_btn = document.createElement("a");
    accord_btn.className = "accordion-button collapsed";
    accord_btn.setAttribute("data-bs-toggle", "collapse");
    accord_btn.setAttribute("data-bs-target", "#flush-collapse2-" + q_number);
    accord_btn.setAttribute("aria-controls", "#flush-collapse2-" + q_number);

    accord_p = document.createElement("p");
    accord_p.innerHTML = q_number;

    accord_btn.appendChild(accord_p);
    accord_head.appendChild(accord_btn);

    flush_div = document.createElement("div");
    flush_div.className = "accordion-collapse collapse";
    flush_div.setAttribute('id', 'flush-collapse2-' + q_number);

    flush_body = document.createElement("div");
    flush_body.className = "accordion-body";
    flush_body.setAttribute("id", "accordion-body2-" + q_number);

    q_label = document.createElement("label");
    q_label.innerHTML = "Description";
    q_label.setAttribute("class", "me-3");

    q_input = document.createElement("input");
    q_input.className = "form-control me-3";
    q_input.setAttribute("type", "text");
    q_input.setAttribute("placeholder", "Description here...");
    q_input.setAttribute("name", "cour-file-desc-" + q_number);
    q_input.setAttribute("required", "");

    del_btn = document.createElement("a");
    del_btn.className = "btn btn-light";
    del_btn.setAttribute("onclick", "del_cour_file(this.id)");
    del_btn.setAttribute("id", "del-cour-file-" + q_number);
    del_btn.setAttribute("style", "width: 250px;");
    
    del_i = document.createElement("i");
    del_i.className = "fa-solid fa-trash";

    del_span = document.createElement("span");
    del_span.innerHTML = " Delete file";

    del_btn.appendChild(del_i);
    del_btn.appendChild(del_span);

    top_div = document.createElement("div");
    top_div.setAttribute("style", "display: flex; flex-direction: row;");
    top_div.setAttribute("class", "mb-3");
    top_div.appendChild(q_label);
    top_div.appendChild(q_input);
    top_div.appendChild(del_btn);

    e_label = document.createElement("label");
    e_label.innerHTML = "File here";
    e_label.setAttribute("class", "mb-3 me-3 text-nowrap");

    e_input = document.createElement("input");
    e_input.className = "mb-3 form-control";
    e_input.setAttribute("type", "file");
    e_input.setAttribute("style", "width: 100%");
    e_input.setAttribute("name", "cour-file-" + q_number);

    mid_div = document.createElement("div");
    mid_div.setAttribute("style", "display: flex; flex-direction: row;");
    mid_div.setAttribute("class", "mb-3");
    mid_div.appendChild(e_label);
    mid_div.appendChild(e_input);

    flush_body.appendChild(top_div);
    flush_body.appendChild(mid_div);
    flush_div.appendChild(flush_body);

    item_div.appendChild(accord_head);
    item_div.appendChild(flush_div);

    accord_div.appendChild(item_div);
    chapter_side.appendChild(accord_div);
  }
  function del_file(id) {
    console.log(id);
  }
  function add_quiz() {
    console.log('add quiz');
  }
  function del_quiz(id) {
    console.log('id');
  }
}

// chapter-edit.html
if (current_url.split('/').find((element) => element == 'chapter') == 'chapter') {
  function load_everyting() {
    tinymce.init({
      selector: 'textarea',
      plugins: 'ai tinycomments mentions anchor autolink charmap codesample emoticons image link lists media searchreplace table visualblocks wordcount checklist mediaembed casechange export formatpainter pageembed permanentpen footnotes advtemplate advtable advcode editimage tableofcontents mergetags powerpaste tinymcespellchecker autocorrect a11ychecker typography inlinecss',
      toolbar: 'undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | link image media table mergetags | align lineheight | tinycomments | checklist numlist bullist indent outdent | emoticons charmap | removeformat',
      tinycomments_mode: 'embedded',
      tinycomments_author: 'Author name',
      mergetags_list: [
        { value: 'First.Name', title: 'First Name' },
        { value: 'Email', title: 'Email' },
      ],
      ai_request: (request, respondWith) => respondWith.string(() => Promise.reject("See docs to implement AI Assistant"))
    });
  }
  function add_chap_video() {
    chapter_side = document.getElementById("chap-video-side");
    const q_number = ++chapter_side.children.length;

    accord_div = document.createElement("div");
    accord_div.className = "accordion accordion-flush";
    accord_div.setAttribute("style", "border-bottom: 1px solid #e4e4e4;");
    accord_div.setAttribute("id", "chap-video-" + q_number);

    item_div = document.createElement("div");
    item_div.className = "accordion-item";

    accord_head = document.createElement("h2");
    accord_head.className = "accordion-header";

    accord_btn = document.createElement("a");
    accord_btn.className = "accordion-button collapsed";
    accord_btn.setAttribute("data-bs-toggle", "collapse");
    accord_btn.setAttribute("data-bs-target", "#flush-collapse2-" + q_number);
    accord_btn.setAttribute("aria-controls", "#flush-collapse2-" + q_number);

    accord_p = document.createElement("p");
    accord_p.innerHTML = q_number;

    accord_btn.appendChild(accord_p);
    accord_head.appendChild(accord_btn);

    flush_div = document.createElement("div");
    flush_div.className = "accordion-collapse collapse";
    flush_div.setAttribute('id', 'flush-collapse2-' + q_number);

    flush_body = document.createElement("div");
    flush_body.className = "accordion-body";
    flush_body.setAttribute("id", "accordion-body2-" + q_number);

    q_label = document.createElement("label");
    q_label.innerHTML = "Description";
    q_label.setAttribute("class", "me-3");

    q_input = document.createElement("input");
    q_input.className = "form-control me-3";
    q_input.setAttribute("type", "text");
    q_input.setAttribute("placeholder", "Description here...");
    q_input.setAttribute("name", "chap-vid-desc-" + q_number);
    q_input.setAttribute("required", "");

    del_btn = document.createElement("a");
    del_btn.className = "btn btn-light";
    del_btn.setAttribute("onclick", "del_chap_vid(this.id)");
    del_btn.setAttribute("id", "del-chap-vid-" + q_number);
    del_btn.setAttribute("style", "width: 250px;");
    
    del_i = document.createElement("i");
    del_i.className = "fa-solid fa-trash";

    del_span = document.createElement("span");
    del_span.innerHTML = " Delete video";

    del_btn.appendChild(del_i);
    del_btn.appendChild(del_span);

    top_div = document.createElement("div");
    top_div.setAttribute("style", "display: flex; flex-direction: row;");
    top_div.setAttribute("class", "mb-3");
    top_div.appendChild(q_label);
    top_div.appendChild(q_input);
    top_div.appendChild(del_btn);

    e_label = document.createElement("label");
    e_label.innerHTML = "Video here";
    e_label.setAttribute("class", "mb-3 me-3 text-nowrap");

    e_input = document.createElement("input");
    e_input.className = "mb-3 form-control";
    e_input.setAttribute("type", "file");
    e_input.setAttribute("style", "width: 100%");
    e_input.setAttribute("name", "chap-file-" + q_number);

    mid_div = document.createElement("div");
    mid_div.setAttribute("style", "display: flex; flex-direction: row;");
    mid_div.setAttribute("class", "mb-3");
    mid_div.appendChild(e_label);
    mid_div.appendChild(e_input);

    flush_body.appendChild(top_div);
    flush_body.appendChild(mid_div);
    flush_div.appendChild(flush_body);

    item_div.appendChild(accord_head);
    item_div.appendChild(flush_div);

    accord_div.appendChild(item_div);
    chapter_side.appendChild(accord_div);
  }
  function del_chap_vid(id) {
    console.log(id);
  }
  function add_chap_file() {
    chapter_side = document.getElementById("chap-file-side");
    const q_number = ++chapter_side.children.length;

    accord_div = document.createElement("div");
    accord_div.className = "accordion accordion-flush";
    accord_div.setAttribute("style", "border-bottom: 1px solid #e4e4e4;");
    accord_div.setAttribute("id", "chap-file-" + q_number);

    item_div = document.createElement("div");
    item_div.className = "accordion-item";

    accord_head = document.createElement("h2");
    accord_head.className = "accordion-header";

    accord_btn = document.createElement("a");
    accord_btn.className = "accordion-button collapsed";
    accord_btn.setAttribute("data-bs-toggle", "collapse");
    accord_btn.setAttribute("data-bs-target", "#flush-collapse3-" + q_number);
    accord_btn.setAttribute("aria-controls", "#flush-collapse3-" + q_number);

    accord_p = document.createElement("p");
    accord_p.innerHTML = q_number;

    accord_btn.appendChild(accord_p);
    accord_head.appendChild(accord_btn);

    flush_div = document.createElement("div");
    flush_div.className = "accordion-collapse collapse";
    flush_div.setAttribute('id', 'flush-collapse3-' + q_number);

    flush_body = document.createElement("div");
    flush_body.className = "accordion-body";
    flush_body.setAttribute("id", "accordion-body3-" + q_number);

    q_label = document.createElement("label");
    q_label.innerHTML = "Description";
    q_label.setAttribute("class", "me-3");

    q_input = document.createElement("input");
    q_input.className = "form-control me-3";
    q_input.setAttribute("type", "text");
    q_input.setAttribute("placeholder", "Description here...");
    q_input.setAttribute("name", "chap-file-desc-" + q_number);
    q_input.setAttribute("required", "");

    del_btn = document.createElement("a");
    del_btn.className = "btn btn-light";
    del_btn.setAttribute("onclick", "del_chap_file(this.id)");
    del_btn.setAttribute("id", "del-chap-file-" + q_number);
    del_btn.setAttribute("style", "width: 250px;");
    
    del_i = document.createElement("i");
    del_i.className = "fa-solid fa-trash";

    del_span = document.createElement("span");
    del_span.innerHTML = " Delete file";

    del_btn.appendChild(del_i);
    del_btn.appendChild(del_span);

    top_div = document.createElement("div");
    top_div.setAttribute("style", "display: flex; flex-direction: row;");
    top_div.setAttribute("class", "mb-3");
    top_div.appendChild(q_label);
    top_div.appendChild(q_input);
    top_div.appendChild(del_btn);

    e_label = document.createElement("label");
    e_label.innerHTML = "File here";
    e_label.setAttribute("class", "mb-3 me-3");

    e_input = document.createElement("input");
    e_input.className = "mb-3 form-control";
    e_input.setAttribute("type", "file");
    e_input.setAttribute("style", "width: 100%");
    e_input.setAttribute("name", "chap-file-" + q_number);

    mid_div = document.createElement("div");
    mid_div.setAttribute("style", "display: flex; flex-direction: row;");
    mid_div.setAttribute("class", "mb-3");
    mid_div.appendChild(e_label);
    mid_div.appendChild(e_input);

    flush_body.appendChild(top_div);
    flush_body.appendChild(mid_div);
    flush_div.appendChild(flush_body);

    item_div.appendChild(accord_head);
    item_div.appendChild(flush_div);

    accord_div.appendChild(item_div);
    chapter_side.appendChild(accord_div);
  }
  function del_chap_file(id) {
    console.log(id);
  }
  function chapter_close() {
    window.close();
  }
}

// quiz-each.html
if (current_url.split('/').find((element) => element == 'quiz') == 'quiz' && current_url.split('/').length == 2 && 
  current_url.split('/')[1] != '') {

  function answer_check(id) {
    const answer = document.getElementById(id);
    const answers = document.getElementById("answers-" + id.match(/\d+/)[0]);
    const question = document.getElementById("question-num-" + id.match(/\d+/)[0]);

    if (answer.children[0].checked) {
      answer.children[0].checked = false;
      answer.children[0].removeAttribute("checked");
      answer.children[0].removeAttribute("name");
      answer.children[2].removeAttribute("name");
      answer.setAttribute("style", "display: flex; align-items: center; background: #f4f4f4;");
      check = true;

      let answers_checked = document.getElementsByClassName("answer_cor");
      let answers_checked_id = document.getElementsByClassName("answer_id");
      
      let checked_answers = [];
      let checked_id = [];
      for (let i = 0; i < answers_checked.length; i++) {
        if (answers_checked[i].checked) {
          checked_answers.push(answers_checked[i]);
          checked_id.push(answers_checked_id[i]);
        }
      }

      for (let i = 0; i < checked_answers.length; i++) {
        let j = i + 1;
        checked_answers[i].setAttribute("name", "answer-cor-" + j);
        checked_id[i].setAttribute("name", "answer-id-" + j);
      }

      for (let i = 0; i < answers.children.length; i++) {
        if (answers.children[i].style.background == "rgb(109, 216, 121)") {
          check = false;
        }
      }

      if (check) {
        question.className = "btn btn-info me-1 ms-1";
      }
    }
    else {
      answer.children[0].checked = true;
      answer.children[0].setAttribute("checked", "");
      let answers_checked = document.getElementsByClassName("answer_cor");
      let answers_checked_id = document.getElementsByClassName("answer_id");
      
      let checked_answers = [];
      let checked_id = [];
      for (let i = 0; i < answers_checked.length; i++) {
        if (answers_checked[i].checked) {
          checked_answers.push(answers_checked[i]);
          checked_id.push(answers_checked_id[i]);
        }
      }

      for (let i = 0; i < checked_answers.length; i++) {
        let j = i + 1;
        checked_answers[i].setAttribute("name", "answer-cor-" + j);
        checked_id[i].setAttribute("name", "answer-id-" + j);
      }

      answer.setAttribute("style", "display: flex; align-items: center; background: #6dd879;");
      let check = [];

      for (let i = 0; i < answers.children.length; i++) {
        if(answers.children[i].style.background == "rgb(244, 244, 244)") {
          check[i] = false;
        }
        else {
          check[i] = true;
        }
      }

      if (check.includes(true)) {
        question.className = "btn btn-warning me-1 ms-1";
      }
    }
  }

  let countdown = 10;
  let x = setInterval(function() {
    countdown--;

    let minutes = Math.floor((countdown % (60 * 60)) / (60));
    let seconds = Math.floor((countdown % (60)));

    if (countdown >= 0) {
      document.getElementById("minutes").innerHTML = minutes;
      document.getElementById("seconds").innerHTML = seconds;
    }
    if (countdown == 0) {
      // document.getElementById("suka").click();
    }
  }, 1000);

}

// quiz-edit.html
if (current_url.split('/').find((element) => element == 'quiz') == 'quiz' && current_url.split('/').length == 4) {
  function add_question(id){
    question_side = document.getElementById("question-side");
    const q_number = ++question_side.children.length;

    accord_div = document.createElement("div");
    accord_div.className = "accordion accordion-flush";
    accord_div.setAttribute("style", "border-bottom: 1px solid #e4e4e4;");
    accord_div.setAttribute("id", "question-" + q_number);

    item_div = document.createElement("div");
    item_div.className = "accordion-item";

    accord_head = document.createElement("h2");
    accord_head.className = "accordion-header";

    accord_btn = document.createElement("a");
    accord_btn.className = "accordion-button collapsed";
    accord_btn.setAttribute("data-bs-toggle", "collapse");
    accord_btn.setAttribute("data-bs-target", "#flush-collapse-" + q_number);
    accord_btn.setAttribute("aria-controls", "#flush-collapse-" + q_number);

    accord_p = document.createElement("p");
    accord_p.innerHTML = q_number;

    accord_btn.appendChild(accord_p);
    accord_head.appendChild(accord_btn);

    flush_div = document.createElement("div");
    flush_div.className = "accordion-collapse collapse";
    flush_div.setAttribute('id', 'flush-collapse-' + q_number);

    flush_body = document.createElement("div");
    flush_body.className = "accordion-body";
    flush_body.setAttribute("id", "accordion-body-" + q_number);

    q_label = document.createElement("label");
    q_label.innerHTML = "question";
    q_label.className = "form-label me-3";

    q_hidden = document.createElement("input");
    q_hidden.setAttribute("type", "hidden");
    q_hidden.setAttribute("id", "question-id-" + q_number);
    q_hidden.setAttribute("name", "question-id-" + q_number);

    q_input = document.createElement("input");
    q_input.className = "form-control mb-2";
    q_input.setAttribute("type", "text");
    q_input.setAttribute("placeholder", "Question here...");
    q_input.setAttribute("name", "question-" + q_number);
    q_input.setAttribute("required", "");

    wrap_1 = document.createElement("div");
    wrap_1.className = "mb-2";
    wrap_1.setAttribute("style", "display: flex; align-items: center;");
    wrap_1.appendChild(q_label);
    wrap_1.appendChild(q_hidden);
    wrap_1.appendChild(q_input);

    e_label = document.createElement("label");
    e_label.innerHTML = "explanation";
    e_label.className = "form-label me-3";

    e_input = document.createElement("input");
    e_input.className = "form-control mb-2";
    e_input.setAttribute("type", "text");
    e_input.setAttribute("placeholder", "Explanation here...");
    e_input.setAttribute("name", "explanation-" + q_number);

    wrap_2 = document.createElement("div");
    wrap_2.className = "mb-2";
    wrap_2.setAttribute("style", "display: flex; align-items: center;");
    wrap_2.appendChild(e_label);
    wrap_2.appendChild(e_input);

    wrap_3 = document.createElement("div");
    wrap_3.setAttribute("style", "display:flex; align-items: center; justify-content: space-between;");

    ans_btn = document.createElement("a");
    ans_btn.className = "btn btn-light mb-2";
    ans_btn.setAttribute("onclick", "add_answer(this.id)");
    // here add question id
    ans_btn.setAttribute("id", "add-answer-" + q_number);
    ans_i = document.createElement("i");
    ans_i.className = "fa-solid fa-plus";

    ans_span = document.createElement("span");
    ans_span.innerHTML = " Add answer";

    ans_btn.appendChild(ans_i);
    ans_btn.appendChild(ans_span);

    del_btn = document.createElement("a");
    del_btn.className = "btn btn-light mb-2";
    del_btn.setAttribute("onclick", "del_question(this.id)");
    // here add question id
    del_btn.setAttribute("id", "del-question-" + q_number);
    del_i = document.createElement("i");
    del_i.className = "fa-solid fa-trash";

    del_span = document.createElement("span");
    del_span.innerHTML = " Delete question";

    del_btn.appendChild(del_i);
    del_btn.appendChild(del_span);
    
    ans_ul = document.createElement("ul");
    ans_ul.setAttribute('id', 'answer-ul-' + q_number);

    wrap_3.appendChild(ans_btn);
    wrap_3.appendChild(del_btn);

    question_id = document.createElement("p");
    question_id.setAttribute("id", "question_id-" + q_number);
    question_id.setAttribute("style", "display: none;");

    flush_body.appendChild(wrap_1);
    flush_body.appendChild(wrap_2);
    flush_body.appendChild(wrap_3);
    flush_body.appendChild(ans_ul);
    flush_body.appendChild(question_id);
    flush_div.appendChild(flush_body);

    item_div.appendChild(accord_head);
    item_div.appendChild(flush_div);

    accord_div.appendChild(item_div);
    question_side.appendChild(accord_div);

    const quiz_id = parseInt(id.split("-")[1]);
    htmx.ajax('GET', '/quiz/' + quiz_id + '/add-question', {target:'#question_id-' + q_number, swap:'innerHTML'}).then(() => {
      question_id = document.getElementById("question_id-" + q_number);
      question_id = question_id.innerHTML;
      question_id = parseInt(question_id);

      q_hidden = document.getElementById("question-id-" + q_number);
      q_hidden.value = question_id;
      ans_btn = document.getElementById("add-answer-" + q_number);
      ans_btn.setAttribute("id", "add-answer-" + q_number + "-" + question_id);
      del_btn = document.getElementById("del-question-" + q_number);
      del_btn.setAttribute("id", "del-question-" + q_number + "-" + question_id);
    });
  }

  function add_answer(id) {
    const q_number = id.match(/\d+/)[0];
    answer_ul = document.getElementById('answer-ul-' + q_number);
    a_number = ++document.getElementsByClassName("answer-div").length;

    answer_div = document.createElement("div");
    answer_div.className = "m-2 me-0 answer-div";
    answer_div.setAttribute("style", "display: flex; align-items: center;");
    answer_div.setAttribute("id", "answer-" + q_number + "-" + a_number);

    r_input = document.createElement("input");
    r_input.className = "me-3";
    r_input.setAttribute("type", "checkbox");
    r_input.setAttribute("name", "answer-cor-" + q_number + "-" + a_number);

    ans_id = document.createElement("input");
    ans_id.setAttribute("type", "hidden");
    ans_id.setAttribute("id", "answer-id-" + q_number + "-" + a_number);
    ans_id.setAttribute("name", "answer-id-" + q_number + "-" + a_number);

    t_input = document.createElement("input");
    t_input.className = "form-control";
    t_input.setAttribute("type", "text");
    t_input.setAttribute("name", "answer-body-" + q_number + "-" + a_number);
    t_input.setAttribute("required", "");

    ans_a = document.createElement("a");
    ans_a.setAttribute("id", "answer-del-" + q_number + "-" + a_number);
    ans_a.setAttribute("onclick", "del_answer(this.id)");

    ans_i = document.createElement("i");
    ans_i.className = "fa-solid fa-x ms-3";
    ans_i.setAttribute("style", "cursor: pointer;");

    answer_id_backend = document.createElement("p");
    answer_id_backend.setAttribute("id", "answer_id-" + q_number + "-" + a_number);
    answer_id_backend.setAttribute("style", "display: none;");

    ans_a.appendChild(ans_i);
    answer_div.appendChild(r_input);
    answer_div.appendChild(ans_id);
    answer_div.appendChild(t_input);
    answer_div.appendChild(ans_a);
    answer_div.appendChild(answer_id_backend);
    answer_ul.appendChild(answer_div);

    const question_id = parseInt(id.split("-")[3]);
    htmx.ajax('GET', '/quiz/' + question_id + '/add-answer', {target:'#answer_id-' + q_number + "-" + a_number, swap:'innerHTML'}).then(() => {
      answer_id = document.getElementById("answer_id-" + q_number + "-" + a_number);
      answer_id = answer_id.innerHTML;
      answer_id = parseInt(answer_id);
      answer_del = document.getElementById("answer-del-" + q_number + '-' + a_number);
      hidden_input = document.getElementById("answer-id-" + q_number + '-' + a_number);
      hidden_input.value = answer_id;

      questions = document.getElementsByClassName("accordion accordion-flush");
      let answer_number = 1;

      for (let i = 0; i < questions.length; i++) {
        let question_number = i + 1;
        let answers = document.getElementById("answer-ul-" + question_number);
        for (let k = 0; k < answers.children.length; k++) {
          let pk = question_number + "-" + answer_number;
          answers.children[k].setAttribute("id", "answer-" + pk);
          answers.children[k].setAttribute("name", "answer-" + pk);
          answers.children[k].children[0].setAttribute("name", "answer-cor-" + pk);
          answers.children[k].children[1].setAttribute("id", "answer-id-" + pk);
          answers.children[k].children[1].setAttribute("name", "answer-id-" + pk);
          answers.children[k].children[2].setAttribute("name", "answer-body-" + pk);
          if (typeof answers.children[k].children[4]?.innerHTML != 'undefined') {
            hidden_id = answers.children[k].children[4].innerHTML;
            hidden_id = parseInt(hidden_id);
            answers.children[k].children[3].setAttribute("id", "answer-del-" + pk + '-' + hidden_id);
            answers.children[k].children[4].setAttribute("id", "answer_id-" + pk);
          }
          const answer_del_id = parseInt(answers.children[k].children[3].id.split("-")[4]);
          answers.children[k].children[3].setAttribute("id", "answer-del-" + pk + '-' + answer_del_id);          
          answer_number++;
        }
      }
    });
  }

  function del_answer(id) {
    const number = id.match(/(\d+)-(\d+)/)[0];
    answer_div = document.getElementById("answer-" + number);
    answer_div.remove();
    htmx.ajax('GET', '/quiz/' + parseInt(id.split("-")[4]) + '/delete-answer', '#success');

    questions = document.getElementsByClassName("accordion accordion-flush");
    let answer_number = 1;

    for (let i = 0; i < questions.length; i++) {
      let question_number = i + 1;
      let answers = document.getElementById("answer-ul-" + question_number);
      for (let k = 0; k < answers.children.length; k++) {
        let pk = question_number + "-" + answer_number;
        answers.children[k].setAttribute("id", "answer-" + pk);
        answers.children[k].setAttribute("name", "answer-" + pk);
        answers.children[k].children[0].setAttribute("name", "answer-cor-" + pk);
        answers.children[k].children[1].setAttribute("id", "answer-id-" + pk);
        answers.children[k].children[1].setAttribute("name", "answer-id-" + pk);
        answers.children[k].children[2].setAttribute("name", "answer-body-" + pk);
        if (typeof answers.children[k].children[4]?.innerHTML != 'undefined') {
          hidden_id = answers.children[k].children[4].innerHTML;
          hidden_id = parseInt(hidden_id);
          answers.children[k].children[3].setAttribute("id", "answer-del-" + pk + '-' + hidden_id);
          answers.children[k].children[4].setAttribute("id", "answer_id-" + pk);
        }
        const answer_del_id = parseInt(answers.children[k].children[3].id.split("-")[4]);
        answers.children[k].children[3].setAttribute("id", "answer-del-" + pk + '-' + answer_del_id);                  
        answer_number++;
      }
    }
  }

  function del_question(id) {
    const q_number = id.match(/\d+/)[0];
    question_div = document.getElementById("question-" + q_number);
    question_div.remove();
    htmx.ajax('GET', '/quiz/' + parseInt(id.split("-")[3]) + '/delete-question', '#success');

    questions = document.getElementsByClassName("accordion accordion-flush");
    let answer_number = 1;

    for (let i = 0; i < questions.length; i++) {
      let j = i + 1;
      questions[i].setAttribute("id", "question-" + j);
      // question > div > h2 > button > p
      questions[i].children[0].children[0].children[0].children[0].innerHTML = j;

      questions[i].children[0].children[0].children[0].setAttribute("data-bs-target", "#flush-collapse-" + j);
      questions[i].children[0].children[0].children[0].setAttribute("aria-controls", "#flush-collapse-" + j);
      // question > div > div
      questions[i].children[0].children[1].setAttribute("id", "flush-collapse-" + j);
      // question > div > div > div
      questions[i].children[0].children[1].children[0].setAttribute("id", "accordion-body-" + j);
      // question > div > div > div > input
      questions[i].children[0].children[1].children[0].children[0].children[1].setAttribute("name", "question-id-" + j);
      questions[i].children[0].children[1].children[0].children[0].children[2].setAttribute("name", "question-" + j);
      questions[i].children[0].children[1].children[0].children[1].children[1].setAttribute("name", "explanation-" + j);
      questions[i].children[0].children[1].children[0].children[3].setAttribute("id", "answer-ul-" + j);

      const id_num = parseInt(questions[i].children[0].children[1].children[0].children[2].children[1].id.split("-")[3]);
      questions[i].children[0].children[1].children[0].children[2].children[1].setAttribute("id", "del-question-" + j + "-" + id_num);
      // question > div > div > div > div > btns
      questions[i].children[0].children[1].children[0].children[2].children[0].setAttribute("id", "answer-btn-" + j + "-" + id_num);

      let answers = document.getElementById("answer-ul-" + j);

      for (let k = 0; k < answers.children.length; k++) {
        let pk = j + "-" + answer_number;
        answers.children[k].setAttribute("id", "answer-" + pk);
        answers.children[k].setAttribute("name", "answer-" + pk);
        answers.children[k].children[0].setAttribute("name", "answer-cor-" + pk);
        answers.children[k].children[1].setAttribute("id", "answer-id-" + pk);
        answers.children[k].children[1].setAttribute("name", "answer-id-" + pk);
        answers.children[k].children[2].setAttribute("name", "answer-body-" + pk);
        if (typeof answers.children[k].children[4]?.innerHTML != 'undefined') {
          hidden_id = answers.children[k].children[4].innerHTML;
          hidden_id = parseInt(hidden_id);
          answers.children[k].children[3].setAttribute("id", "answer-del-" + pk + '-' + hidden_id);
          answers.children[k].children[4].setAttribute("id", "answer_id-" + pk);
        }
        const answer_del_id = parseInt(answers.children[k].children[3].id.split("-")[4]);
        answers.children[k].children[3].setAttribute("id", "answer-del-" + pk + '-' + answer_del_id);          
        answer_number++;
      }
    }
  }
}

// profile-update.html
if (current_url == 'user/profile-update/account') {
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

}

if (current_url.split('/').length == 3 && current_url.split('/').find((element) => element == 'contest') == 'contest' &&
    current_url.split('/').find((element) => element == 'edit') == 'edit') {
      function contest_add_quiz(id) {
        let contest_side = document.getElementById('contest-quiz-side');
        const q_number = ++contest_side.children.length;

        let accord_div = document.createElement("div");
        accord_div.className = "accordion accordion-flush";
        accord_div.setAttribute("style", "border-bottom: 1px solid #e4e4e4;");
        accord_div.setAttribute("id", "quiz-" + q_number);

        item_div = document.createElement("div");
        item_div.className = "accordion-item";

        accord_head = document.createElement("h2");
        accord_head.className = "accordion-header";

        accord_btn = document.createElement("a");
        accord_btn.className = "accordion-button collapsed";
        accord_btn.setAttribute("data-bs-toggle", "collapse");
        accord_btn.setAttribute("data-bs-target", "#flush-collapse-" + q_number);
        accord_btn.setAttribute("aria-controls", "#flush-collapse-" + q_number);

        accord_p = document.createElement("p");
        accord_p.innerHTML = q_number;

        accord_btn.appendChild(accord_p);
        accord_head.appendChild(accord_btn);

        flush_div = document.createElement("div");
        flush_div.className = "accordion-collapse collapse";
        flush_div.setAttribute('id', 'flush-collapse-' + q_number);

        flush_body = document.createElement("div");
        flush_body.className = "accordion-body";
        flush_body.setAttribute("style", "display: flex; align-items: center;");
        flush_body.setAttribute("id", "accordion-body-" + q_number);

        wrap_1 = document.createElement("div");
        wrap_1.className = "me-2";
        wrap_1.setAttribute("style", "display: flex; align-items: center; width: 100%;");

        q_label = document.createElement("label");
        q_label.innerHTML = "Quiz";
        q_label.className = "form-label";
        q_label.setAttribute("style", "margin-top: auto; margin-bottom: auto;");

        q_p = document.createElement("p");
        q_p.innerHTML = 0;
        q_p.className = "form-control ms-2";

        wrap_1.appendChild(q_label);
        wrap_1.appendChild(q_p);

        wrap_2 = document.createElement("div");
        wrap_2.className = "ms-2";
        wrap_2.setAttribute("style", "display: flex; align-items: center; width: 100%;");

        e_label = document.createElement("label");
        e_label.innerHTML = "Question";
        e_label.className = "form-label";
        e_label.setAttribute("style", "margin-top: auto; margin-bottom: auto;");

        e_p = document.createElement("p");
        e_p.innerHTML = 0;
        e_p.className = "form-control ms-2";

        wrap_2.appendChild(e_label);
        wrap_2.appendChild(e_p);

        wrap_3 = document.createElement("div");
        wrap_3.className = "ms-2";
        wrap_3.setAttribute("style", "display: flex; align-items: center; justify-content: end;");
        wrap_3.setAttribute("id", "delete-btn-" + q_number);

        del_btn = document.createElement("a");
        del_btn.className = "btn btn-light ms-2 text-nowrap";
        del_btn.innerHTML = "Delete quiz";

        wrap_3.appendChild(del_btn);

        flush_body.appendChild(wrap_1);
        flush_body.appendChild(wrap_2);
        flush_body.appendChild(wrap_3);

        flush_div.appendChild(flush_body);

        item_div.appendChild(accord_head);
        item_div.appendChild(flush_div);

        accord_div.appendChild(item_div);
        contest_side.appendChild(accord_div);

        htmx.ajax('GET', '/contest/' + id + '/edit/quiz/create', {target:'#contest-success', swap:'innerHTML'}).then(() => {
          let success = document.getElementById('contest-success');
          success = success.innerHTML;
          success = parseInt(success);
          let delete_btn = document.getElementById('delete-btn-' + q_number);
          delete_btn.children[0].setAttribute("id", `${q_number}` + '-' + success);
        });
      }

      function contest_delete_quiz(id) {
        let q_number = parseInt(id.split("-")[0]);
        let quiz = parseInt(id.split('-')[1]);
        let contest_div = document.getElementById("quiz-" + q_number);
        contest_div.remove();

        htmx.ajax('GET', '/contest/' + quiz + '/edit/quiz/delete', '#contest-success');

        let quizs = document.getElementsByClassName("accordion accordion-flush");

        for (let i = 0; i < quizs.length; i++) {
          let j = i + 1;
          quizs[i].setAttribute("id", "quiz-" + j);
          // question > div > h2 > button > p
          quizs[i].children[0].children[0].children[0].children[0].innerHTML = j;

          quizs[i].children[0].children[0].children[0].setAttribute("data-bs-target", "#flush-collapse-" + j);
          quizs[i].children[0].children[0].children[0].setAttribute("aria-controls", "#flush-collapse-" + j);
          // question > div > div
          quizs[i].children[0].children[1].setAttribute("id", "flush-collapse-" + j);
          // question > div > div > div
          quizs[i].children[0].children[1].children[0].setAttribute("id", "accordion-body-" + j);

          let quiz_id = quizs[i].children[0].children[1].children[0].children[2].children[0].id;
          quiz_id = quiz_id.split('-')[1];
          
          quizs[i].children[0].children[1].children[0].children[2].children[0].setAttribute("id", `${j}` + '-' + quiz_id);
        }    
      } 
}

// calendar.html
if (current_url == 'calendar') {
  
  const daysTag = document.querySelector(".days"),
  currentDate = document.querySelector(".current-date"),
  prevNextIcon = document.querySelectorAll(".icons span");
  // getting new date, current year and month
  let date = new Date(),
  currYear = date.getFullYear(),
  currMonth = date.getMonth();
  // storing full name of all months in array
  const months = ["January", "February", "March", "April", "May", "June", "July",
                "August", "September", "October", "November", "December"];
  const renderCalendar = () => {
      let firstDayofMonth = new Date(currYear, currMonth, 1).getDay(), // getting first day of month
      lastDateofMonth = new Date(currYear, currMonth + 1, 0).getDate(), // getting last date of month
      lastDayofMonth = new Date(currYear, currMonth, lastDateofMonth).getDay(), // getting last day of month
      lastDateofLastMonth = new Date(currYear, currMonth, 0).getDate(); // getting last date of previous month
      let liTag = "";
      for (let i = firstDayofMonth; i > 0; i--) { // creating li of previous month last days
          liTag += `<li class="inactive">${lastDateofLastMonth - i + 1}</li>`;
      }
      for (let i = 1; i <= lastDateofMonth; i++) { // creating li of all days of current month
          // adding active class to li if the current day, month, and year matched
          let isToday = i === date.getDate() && currMonth === new Date().getMonth() 
                      && currYear === new Date().getFullYear() ? "active" : "";
          if(isToday == 'active'){
            liTag += `<li class="${isToday}" style="background: #be76db;">${i}</li>`;
          }
          else {
            liTag += `<li class="${isToday}">${i}</li>`;
          }
      }
      for (let i = lastDayofMonth; i < 6; i++) { // creating li of next month first days
          liTag += `<li class="inactive">${i - lastDayofMonth + 1}</li>`
      }
      currentDate.innerText = `${months[currMonth]} ${currYear}`; // passing current mon and yr as currentDate text
      daysTag.innerHTML = liTag;
  }
  renderCalendar();
  prevNextIcon.forEach(icon => { // getting prev and next icons
      icon.addEventListener("click", () => { // adding click event on both icons
          // if clicked icon is previous icon then decrement current month by 1 else increment it by 1
          currMonth = icon.id === "prev" ? currMonth - 1 : currMonth + 1;
          if(currMonth < 0 || currMonth > 11) { // if current month is less than 0 or greater than 11
              // creating a new date of current year & month and pass it as date value
              date = new Date(currYear, currMonth, new Date().getDate());
              currYear = date.getFullYear(); // updating current year with new date year
              currMonth = date.getMonth(); // updating current month with new date month
          } else {
              date = new Date(); // pass the current date as date value
          }
          renderCalendar(); // calling renderCalendar function
      });
  });
}
