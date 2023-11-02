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
  function add_chapter(id){
    const course_id = parseInt(id);
    let chapter_side = document.getElementById("cour-chap-side");
    const q_number = ++chapter_side.children.length;

    let accord_div = document.createElement("div");
    accord_div.className = "accordion accordion-flush";
    accord_div.setAttribute("style", "border-bottom: 1px solid #e4e4e4;");
    accord_div.setAttribute("id", "cour-chap-" + q_number);

    let item_div = document.createElement("div");
    item_div.className = "accordion-item";

    let accord_head = document.createElement("h2");
    accord_head.className = "accordion-header";

    let accord_btn = document.createElement("a");
    accord_btn.className = "accordion-button collapsed";
    accord_btn.setAttribute("data-bs-toggle", "collapse");
    accord_btn.setAttribute("data-bs-target", "#flush-collapse1-" + q_number);
    accord_btn.setAttribute("aria-controls", "#flush-collapse1-" + q_number);

    let accord_p = document.createElement("p");
    accord_p.innerHTML = q_number;

    accord_btn.appendChild(accord_p);
    accord_head.appendChild(accord_btn);

    let flush_div = document.createElement("div");
    flush_div.className = "accordion-collapse collapse";
    flush_div.setAttribute('id', 'flush-collapse1-' + q_number);

    let flush_body = document.createElement("div");
    flush_body.className = "accordion-body";
    flush_body.setAttribute("id", "accordion-body1-" + q_number);

    let q_label = document.createElement("label");
    q_label.innerHTML = "name";
    q_label.setAttribute("class", "me-3");

    let q_input = document.createElement("p");
    q_input.className = "form-control me-3";

    let del_btn = document.createElement("a");
    del_btn.className = "btn btn-light text-nowrap me-3";
    del_btn.setAttribute("onclick", "del_chapter(this.id)");
    del_btn.setAttribute("id", "del-chapter-" + q_number + '');
    del_btn.setAttribute("style", "width: max-content;");
    
    let del_i = document.createElement("i");
    del_i.className = "fa-solid fa-trash";

    let del_span = document.createElement("span");
    del_span.innerHTML = " Delete Chapter";

    del_btn.appendChild(del_i);
    del_btn.appendChild(del_span);

    let edit_btn = document.createElement("a");
    edit_btn.className = "btn btn-light text-nowrap";
    edit_btn.setAttribute("onclick", "edit_chapter(this.id)");
    edit_btn.setAttribute("id", "edit-chapter-" + '');
    edit_btn.setAttribute("style", "width: max-content;");
    
    let edit_i = document.createElement("i");
    edit_i.className = "fa-solid fa-trash";

    let edit_span = document.createElement("span");
    edit_span.innerHTML = "Edit Chapter";

    edit_btn.appendChild(edit_i);
    edit_btn.appendChild(edit_span);

    let top_div = document.createElement("div");
    top_div.setAttribute("style", "display: flex; flex-direction: row;");
    top_div.setAttribute("class", "mb-3");
    top_div.appendChild(q_label);
    top_div.appendChild(q_input);
    top_div.appendChild(del_btn);
    top_div.appendChild(edit_btn);

    let e_label = document.createElement("label");
    e_label.innerHTML = "body";
    e_label.setAttribute("class", "me-3");

    let e_input = document.createElement("p");
    e_input.className = "form-control";
    e_input.innerHTML = "None";

    let mid_div = document.createElement("div");
    mid_div.setAttribute("style", "display: flex;");
    mid_div.setAttribute("class", "mb-3");
    mid_div.appendChild(e_label);
    mid_div.appendChild(e_input);

    let w_label = document.createElement("label");
    w_label.innerHTML = "Quizes total:";
    w_label.setAttribute("class", "me-3");

    let w_input = document.createElement("p");
    w_input.className = "text-muted";

    let quizss_div = document.createElement("div");
    quizss_div.setAttribute("style", "display: flex;");
    quizss_div.setAttribute("class", "mb-3");
    quizss_div.appendChild(w_label);
    quizss_div.appendChild(w_input);

    let r_label = document.createElement("label");
    r_label.innerHTML = "Files total:";
    r_label.setAttribute("class", "me-3");

    let r_input = document.createElement("p");
    r_input.className = "text-muted";
    
    let btm_div = document.createElement("div");
    btm_div.setAttribute("style", "display: flex;");
    btm_div.setAttribute("class", "mb-3");
    btm_div.appendChild(e_label);
    btm_div.appendChild(e_input);

    flush_body.appendChild(top_div);
    flush_body.appendChild(mid_div);
    flush_body.appendChild(quizss_div);
    flush_body.appendChild(btm_div);
    flush_div.appendChild(flush_body);

    item_div.appendChild(accord_head);
    item_div.appendChild(flush_div);

    accord_div.appendChild(item_div);
    chapter_side.appendChild(accord_div);

    try {
    htmx.ajax('GET', '/course/' + course_id + '/edit/chapter/create', {target:'#success-chapter', swap:'innerHTML'}).then(() => {
      let chapter_btn = document.getElementById(id);
      chapter_btn.setAttribute("style", "pointer-events: none; width: 100%;");

      let timer2;
      timer2 = setTimeout(() => {
        chapter_btn.setAttribute("style", "pointer-events: all; width: 100%;");
      }, 1250);

      let chapter_id = document.getElementById('success-chapter');
      chapter_id = chapter_id.innerHTML;
      chapter_id = parseInt(chapter_id);
      console.log(chapter_id);

      if(chapter_id == "NaN") {
        chapter_side.removeChild(chapter_side.lastChild);
        console.log("Removed last chapter");
      }
      else {
        edit_btn.setAttribute("href", "/course/" + course_id + "/edit/chapter/" + chapter_id + '/edit');
        edit_btn.setAttribute("target", "_blank");
        del_btn.setAttribute("id", "del-chapter-" + q_number + "-" + chapter_id);
  
        let toast = document.getElementById("toast");
        toast.setAttribute("style", "border: 2px solid #46f440;");
        toast.children[0].children[0].setAttribute("style", "background-color: #46f440;");
        let current_pos = window.scrollY + 25;
        toast.setAttribute("style", `display: block; top: ${current_pos}px;`);
        let text1 = document.getElementById("text-1");
        text1.innerHTML = "Success";
        let text2 = document.getElementById("text-2");
        text2.innerHTML = "Chapter has been successfully created";
        let timer1;
        toast.className = "custom-toast active";
      
        timer1 = setTimeout(() => {
            toast.className = "custom-toast";
            toast.setAttribute("style", "display: none;");
        }, 1250); //1s = 1000 milliseconds
      }

    });
    }
    catch (error) {
      chapter_side.removeChild(chapter_side.lastChild);      

      let toast = document.getElementById("toast");
      toast.setAttribute("style", "border: 2px solid red;");
      toast.children[0].children[0].setAttribute("style", "background-color: red;");
      let current_pos = window.scrollY + 25;
      toast.setAttribute("style", `display: block; top: ${current_pos}px;`);
      let text1 = document.getElementById("text-1");
      text1.innerHTML = "Success";
      let text2 = document.getElementById("text-2");
      text2.innerHTML = "Chapter is not created succesfully";
      let timer1;
      toast.className = "custom-toast active";
    
      timer1 = setTimeout(() => {
          toast.className = "custom-toast";
          toast.setAttribute("style", "display: none;");
      }, 1250); //1s = 1000 milliseconds
    }

  }
  function del_chapter(id) {
    const number = id.split("-");
    const q_number = parseInt(number[2]);
    const chap_id = parseInt(number[3]);
    const chapter_div = document.getElementById('cour-chap-' + q_number);

    try {
      htmx.ajax('GET', '/course/edit/chapter/' + chap_id + '/delete', '#success-chapter');
      chapter_div.remove();

      let toast = document.getElementById("toast");
      toast.setAttribute("style", "border: 2px solid #46f440;");
      toast.children[0].children[0].setAttribute("style", "background-color: #46f440;");
      let current_pos = window.scrollY + 25;
      toast.setAttribute("style", `display: block; top: ${current_pos}px;`);
      let text1 = document.getElementById("text-1");
      text1.innerHTML = "Success";
      let text2 = document.getElementById("text-2");
      text2.innerHTML = "Chapter has been successfully deleted";
      let timer1;
      toast.className = "custom-toast active";
    
      timer1 = setTimeout(() => {
          toast.className = "custom-toast";
          toast.setAttribute("style", "display: none;");
      }, 1250); //1s = 1000 milliseconds

      const chapters = document.getElementById('cour-chap-side');

      for (let i = 0; i < chapters.children.length; i++) {
        let j = i + 1;
        chapters.children[i].setAttribute('id', 'cour-chap-' + j);
        chapters.children[i].children[0].children[0].children[0].setAttribute('data-bs-target', '#flush-collapse1-' + j);
        chapters.children[i].children[0].children[0].children[0].setAttribute('aria-controls', '#flush-collapse1-' + j);
        chapters.children[i].children[0].children[0].children[0].children[0].innerHTML = j;
  
        chapters.children[i].children[0].children[1].setAttribute('id', 'flush-collapse1-' + j);
        chapters.children[i].children[0].children[1].children[0].setAttribute('id', 'accordion-body1-' + j);
  
        let chapter_id = chapters.children[i].children[0].children[1].children[0].children[0].children[2].id.split("-")[3];
        chapter_id = parseInt(chapter_id);
        chapters.children[i].children[0].children[1].children[0].children[0].children[2].setAttribute('id', 'del-chapter-' + j + '-' + chapter_id);
      }
    }
    catch (error) {
      let toast = document.getElementById("toast");
      toast.setAttribute("style", "border: 2px solid red;");
      toast.children[0].children[0].setAttribute("style", "background-color: red;");
      let current_pos = window.scrollY + 25;
      toast.setAttribute("style", `display: block; top: ${current_pos}px;`);
      let text1 = document.getElementById("text-1");
      text1.innerHTML = "Success";
      let text2 = document.getElementById("text-2");
      text2.innerHTML = "Chapter is not deleted successfully";
      let timer1;
      toast.className = "custom-toast active";
    
      timer1 = setTimeout(() => {
          toast.className = "custom-toast";
          toast.setAttribute("style", "display: none;");
      }, 1250); //1s = 1000 milliseconds
    }
  }

  function add_file() {
    let chapter_side = document.getElementById("cour-file-side");
    const q_number = ++chapter_side.children.length;

    let accord_div = document.createElement("div");
    accord_div.className = "accordion accordion-flush";
    accord_div.setAttribute("style", "border-bottom: 1px solid #e4e4e4;");
    accord_div.setAttribute("id", "cour-file-" + q_number);

    let item_div = document.createElement("div");
    item_div.className = "accordion-item";

    let accord_head = document.createElement("h2");
    accord_head.className = "accordion-header";

    let accord_btn = document.createElement("a");
    accord_btn.className = "accordion-button collapsed";
    accord_btn.setAttribute("data-bs-toggle", "collapse");
    accord_btn.setAttribute("data-bs-target", "#flush-collapse2-" + q_number);
    accord_btn.setAttribute("aria-controls", "#flush-collapse2-" + q_number);

    let accord_p = document.createElement("p");
    accord_p.innerHTML = q_number;

    accord_btn.appendChild(accord_p);
    accord_head.appendChild(accord_btn);

    let flush_div = document.createElement("div");
    flush_div.className = "accordion-collapse collapse";
    flush_div.setAttribute('id', 'flush-collapse2-' + q_number);

    let flush_body = document.createElement("div");
    flush_body.className = "accordion-body";
    flush_body.setAttribute("id", "accordion-body2-" + q_number);

    let q_label = document.createElement("label");
    q_label.innerHTML = "Description";
    q_label.setAttribute("class", "me-3");

    let q_input = document.createElement("input");
    q_input.className = "form-control me-3";
    q_input.setAttribute("type", "text");
    q_input.setAttribute("placeholder", "Description here...");
    q_input.setAttribute("name", "cour-file-desc-" + q_number);
    q_input.setAttribute("required", "");

    let del_btn = document.createElement("a");
    del_btn.className = "btn btn-light";
    del_btn.setAttribute("onclick", "del_cour_file(this.id)");
    del_btn.setAttribute("id", "del-cour-file-" + q_number);
    del_btn.setAttribute("style", "width: 250px;");
    
    let del_i = document.createElement("i");
    del_i.className = "fa-solid fa-trash";

    let del_span = document.createElement("span");
    del_span.innerHTML = " Delete file";

    del_btn.appendChild(del_i);
    del_btn.appendChild(del_span);

    let top_div = document.createElement("div");
    top_div.setAttribute("style", "display: flex; flex-direction: row;");
    top_div.setAttribute("class", "mb-3");
    top_div.appendChild(q_label);
    top_div.appendChild(q_input);
    top_div.appendChild(del_btn);

    let e_label = document.createElement("label");
    e_label.innerHTML = "File here";
    e_label.setAttribute("class", "mb-3 me-3 text-nowrap");

    let e_input = document.createElement("input");
    e_input.className = "mb-3 form-control";
    e_input.setAttribute("type", "file");
    e_input.setAttribute("style", "width: 100%");
    e_input.setAttribute("name", "cour-file-" + q_number);

    let mid_div = document.createElement("div");
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
  function add_quiz(id) {
    let quiz_side = document.getElementById("cour-quiz-side");
    const q_number = ++quiz_side.children.length;
    const course_id = parseInt(id);

    let accord_div = document.createElement("div");
    accord_div.className = "accordion accordion-flush";
    accord_div.setAttribute("style", "border-bottom: 1px solid #e4e4e4;");
    accord_div.setAttribute("id", "cour-quiz-" + q_number);

    let item_div = document.createElement("div");
    item_div.className = "accordion-item";

    let accord_head = document.createElement("h2");
    accord_head.className = "accordion-header";

    let accord_btn = document.createElement("a");
    accord_btn.className = "accordion-button collapsed";
    accord_btn.setAttribute("data-bs-toggle", "collapse");
    accord_btn.setAttribute("data-bs-target", "#flush-collapse3-" + q_number);
    accord_btn.setAttribute("aria-controls", "#flush-collapse3-" + q_number);

    let accord_p = document.createElement("p");
    accord_p.innerHTML = q_number;

    accord_btn.appendChild(accord_p);
    accord_head.appendChild(accord_btn);

    let flush_div = document.createElement("div");
    flush_div.className = "accordion-collapse collapse";
    flush_div.setAttribute('id', 'flush-collapse3-' + q_number);

    let flush_body = document.createElement("div");
    flush_body.className = "accordion-body";
    flush_body.setAttribute("id", "accordion-body3-" + q_number);

    let q_label = document.createElement("label");
    q_label.innerHTML = "name";
    q_label.setAttribute("class", "me-3");

    let q_input = document.createElement("p");
    q_input.className = "form-control me-3";

    let del_btn = document.createElement("a");
    del_btn.className = "btn btn-light me-3 text-nowrap";
    del_btn.setAttribute("onclick", "del_quiz(this.id)");
    del_btn.setAttribute("style", "width: max-content;");
    
    let del_i = document.createElement("i");
    del_i.className = "fa-solid fa-trash";

    let del_span = document.createElement("span");
    del_span.innerHTML = " Delete quiz";

    del_btn.appendChild(del_i);
    del_btn.appendChild(del_span);

    let edit_btn = document.createElement("a");
    edit_btn.className = "btn btn-light text-nowrap";
    edit_btn.setAttribute("target", "_blank");
    edit_btn.setAttribute("style", "width: max-content;");
    
    let edit_i = document.createElement("i");
    edit_i.className = "fa-solid fa-trash";

    let edit_span = document.createElement("span");
    edit_span.innerHTML = " Edit quiz";

    edit_btn.appendChild(edit_i);
    edit_btn.appendChild(edit_span);

    let top_div = document.createElement("div");
    top_div.setAttribute("style", "display: flex; flex-direction: row;");
    top_div.setAttribute("class", "mb-3");
    top_div.appendChild(q_label);
    top_div.appendChild(q_input);
    top_div.appendChild(del_btn);
    top_div.appendChild(edit_btn);

    let e_label = document.createElement("label");
    e_label.innerHTML = "Number of Questions";
    e_label.setAttribute("class", "me-3");

    let e_input = document.createElement("p");
    e_input.className = "form-control";

    let mid_div = document.createElement("div");
    mid_div.setAttribute("style", "display: flex;");
    mid_div.setAttribute("class", "mb-3");
    mid_div.appendChild(e_label);
    mid_div.appendChild(e_input);

    flush_body.appendChild(top_div);
    flush_body.appendChild(mid_div);
    flush_div.appendChild(flush_body);

    item_div.appendChild(accord_head);
    item_div.appendChild(flush_div);

    accord_div.appendChild(item_div);
    quiz_side.appendChild(accord_div);

    try {
      htmx.ajax('GET', '/course/' + course_id + '/edit/quiz/create', {target:'#success-quiz', swap:'innerHTML'}).then(() => {
        let quiz_id = document.getElementById('success-quiz');
        quiz_id = quiz_id.innerHTML;
        quiz_id = parseInt(quiz_id);

        let chapter_btn = document.getElementById(id);
        chapter_btn.setAttribute("style", "pointer-events: none;");
  
        let timer2;
        timer2 = setTimeout(() => {
          chapter_btn.setAttribute("style", "pointer-events: all;");
        }, 1250);

        let toast = document.getElementById("toast");
        toast.setAttribute("style", "border: 2px solid #46f440;");
        toast.children[0].children[0].setAttribute("style", "background-color: #46f440;");
        let current_pos = window.scrollY + 25;
        toast.setAttribute("style", `display: block; top: ${current_pos}px;`);
        let text1 = document.getElementById("text-1");
        text1.innerHTML = "Success";
        let text2 = document.getElementById("text-2");
        text2.innerHTML = "Quiz has been successfully created";
        let timer1;
        toast.className = "custom-toast active";
      
        timer1 = setTimeout(() => {
            toast.className = "custom-toast";
            toast.setAttribute("style", "display: none;");
        }, 1250); //1s = 1000 milliseconds

        if (quiz_id == "NaN") {
          quiz_side.removeChild(quiz_side.lastChild);
          console.log("Removed last quiz");
        }
        else {
          edit_btn.setAttribute("href", "/quiz/each/" + quiz_id + '/edit');
          del_btn.setAttribute("id", "del-quiz-" + q_number + "-" + quiz_id);
        }
      });
    }
    catch (error) {
      let toast = document.getElementById("toast");
      toast.setAttribute("style", "border: 2px solid red;");
      toast.children[0].children[0].setAttribute("style", "background-color: red;");
      let current_pos = window.scrollY + 25;
      toast.setAttribute("style", `display: block; top: ${current_pos}px;`);
      let text1 = document.getElementById("text-1");
      text1.innerHTML = "Success";
      let text2 = document.getElementById("text-2");
      text2.innerHTML = "Chapter is not deleted successfully";
      let timer1;
      toast.className = "custom-toast active";
    
      timer1 = setTimeout(() => {
          toast.className = "custom-toast";
          toast.setAttribute("style", "display: none;");
      }, 1250); //1s = 1000 milliseconds
    }

  }
  function del_quiz(id) {
    const number = id.split("-");
    const div_id = parseInt(number[2]);
    const quiz_id = parseInt(number[3]);
    let remove_div = document.getElementById("cour-quiz-" + div_id);
    
    try {
      htmx.ajax('GET', '/course/edit/quiz/' + quiz_id + '/delete', '#success-quiz');
      remove_div.remove();

      let toast = document.getElementById("toast");
      toast.setAttribute("style", "border: 2px solid #46f440;");
      toast.children[0].children[0].setAttribute("style", "background-color: #46f440;");
      let current_pos = window.scrollY + 25;
      toast.setAttribute("style", `display: block; top: ${current_pos}px;`);
      let text1 = document.getElementById("text-1");
      text1.innerHTML = "Success";
      let text2 = document.getElementById("text-2");
      text2.innerHTML = "Quiz has been successfully created";
      let timer1;
      toast.className = "custom-toast active";
    
      timer1 = setTimeout(() => {
          toast.className = "custom-toast";
          toast.setAttribute("style", "display: none;");
      }, 1250); //1s = 1000 milliseconds

      let quiz_div = document.getElementById('cour-quiz-side');
      for (let i = 0; i < quiz_div.children.length; i++) {
        let j = i + 1;
        quiz_div.children[i].id = 'cour-quiz-' + j;
        quiz_div.children[i].children[0].children[0].children[0].setAttribute('data-bs-target', '#flush-collapse3-' + j);
        quiz_div.children[i].children[0].children[0].children[0].setAttribute('aria-controls', '#flush-collapse3-' + j);
        quiz_div.children[i].children[0].children[0].children[0].children[0].innerHTML = j;
  
        quiz_div.children[i].children[0].children[1].setAttribute('id', 'flush-collapse3-' + j);
        quiz_div.children[i].children[0].children[1].children[0].setAttribute('id', 'accordion-body3-' + j);
  
        let each_quiz_id = quiz_div.children[i].children[0].children[1].children[0].children[0].children[2].id;
        each_quiz_id = parseInt(each_quiz_id.split('-')[3]);
        quiz_div.children[i].children[0].children[1].children[0].children[0].children[2].setAttribute('id', 'del-quiz-' + j + '-' + each_quiz_id);
      }

      console.log("Quiz deleted successfully");
    }
    catch (error) {
      let toast = document.getElementById("toast");
      toast.setAttribute("style", "border: 2px solid #46f440;");
      toast.children[0].children[0].setAttribute("style", "background-color: #46f440;");
      let current_pos = window.scrollY + 25;
      toast.setAttribute("style", `display: block; top: ${current_pos}px;`);
      let text1 = document.getElementById("text-1");
      text1.innerHTML = "Success";
      let text2 = document.getElementById("text-2");
      text2.innerHTML = "Quiz has been successfully created";
      let timer1;
      toast.className = "custom-toast active";
    
      timer1 = setTimeout(() => {
          toast.className = "custom-toast";
          toast.setAttribute("style", "display: none;");
      }, 1250); //1s = 1000 milliseconds

      console.log("Quiz is not deleted");
    }
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

  function add_chap_quiz(id) {
    quiz_side = document.getElementById("chap-quiz-side");
    const q_number = ++quiz_side.children.length;
    const content_id = parseInt(id);

    accord_div = document.createElement("div");
    accord_div.className = "accordion accordion-flush";
    accord_div.setAttribute("style", "border-bottom: 1px solid #e4e4e4;");
    accord_div.setAttribute("id", "chap-quiz-" + q_number);

    item_div = document.createElement("div");
    item_div.className = "accordion-item";

    accord_head = document.createElement("h2");
    accord_head.className = "accordion-header";

    accord_btn = document.createElement("a");
    accord_btn.className = "accordion-button collapsed";
    accord_btn.setAttribute("data-bs-toggle", "collapse");
    accord_btn.setAttribute("data-bs-target", "#flush-collapse1-" + q_number);
    accord_btn.setAttribute("aria-controls", "#flush-collapse1-" + q_number);

    accord_p = document.createElement("p");
    accord_p.innerHTML = q_number;

    accord_btn.appendChild(accord_p);
    accord_head.appendChild(accord_btn);

    flush_div = document.createElement("div");
    flush_div.className = "accordion-collapse collapse";
    flush_div.setAttribute('id', 'flush-collapse1-' + q_number);

    flush_body = document.createElement("div");
    flush_body.className = "accordion-body";
    flush_body.setAttribute("id", "accordion-body1-" + q_number);

    q_label = document.createElement("label");
    q_label.innerHTML = "name";
    q_label.setAttribute("class", "me-3");

    q_input = document.createElement("p");
    q_input.className = "form-control me-3";

    del_btn = document.createElement("a");
    del_btn.className = "btn btn-light me-3 text-nowrap";
    del_btn.setAttribute("onclick", "del_chap_quiz(this.id)");
    del_btn.setAttribute("style", "width: max-content;");
    
    del_i = document.createElement("i");
    del_i.className = "fa-solid fa-trash";

    del_span = document.createElement("span");
    del_span.innerHTML = " Delete quiz";

    del_btn.appendChild(del_i);
    del_btn.appendChild(del_span);

    edit_btn = document.createElement("a");
    edit_btn.className = "btn btn-light text-nowrap";
    edit_btn.setAttribute("target", "_blank");
    edit_btn.setAttribute("style", "width: max-content;");
    
    edit_i = document.createElement("i");
    edit_i.className = "fa-solid fa-trash";

    edit_span = document.createElement("span");
    edit_span.innerHTML = " Edit quiz";

    edit_btn.appendChild(edit_i);
    edit_btn.appendChild(edit_span);

    top_div = document.createElement("div");
    top_div.setAttribute("style", "display: flex; flex-direction: row;");
    top_div.setAttribute("class", "mb-3");
    top_div.appendChild(q_label);
    top_div.appendChild(q_input);
    top_div.appendChild(del_btn);
    top_div.appendChild(edit_btn);

    e_label = document.createElement("label");
    e_label.innerHTML = "Number of Questions";
    e_label.setAttribute("class", "me-3");

    e_input = document.createElement("p");
    e_input.className = "form-control";

    mid_div = document.createElement("div");
    mid_div.setAttribute("style", "display: flex;");
    mid_div.setAttribute("class", "mb-3");
    mid_div.appendChild(e_label);
    mid_div.appendChild(e_input);

    flush_body.appendChild(top_div);
    flush_body.appendChild(mid_div);
    flush_div.appendChild(flush_body);

    item_div.appendChild(accord_head);
    item_div.appendChild(flush_div);

    accord_div.appendChild(item_div);
    quiz_side.appendChild(accord_div);

    htmx.ajax('GET', '/course/chapter/' + content_id + '/edit/quiz/create', {target:'#chapter-quiz', swap:'innerHTML'}).then(() => {
      let quiz_id = document.getElementById('chapter-quiz');
      quiz_id = quiz_id.innerHTML;
      quiz_id = parseInt(quiz_id);
      edit_btn.setAttribute("href", "/quiz/each/" + quiz_id + '/edit');
      del_btn.setAttribute("id", "del-quiz-" + q_number + "-" + quiz_id);
    });

  }

  function del_chap_quiz(id) {
    const number = id.split("-");
    const div_id = parseInt(number[2]);
    const quiz_id = parseInt(number[3]);
    console.log(div_id);
    let remove_div = document.getElementById("chap-quiz-" + div_id);
    remove_div.remove();
    htmx.ajax('GET', '/course/chapter/edit/quiz/' + quiz_id + '/delete', '#chapter-quiz');

    let quiz_div = document.getElementById('chap-quiz-side');

    for (let i = 0; i < quiz_div.children.length; i++) {
      let j = i + 1;
      quiz_div.children[i].id = 'chap-quiz-' + j;
      quiz_div.children[i].children[0].children[0].children[0].setAttribute('data-bs-target', '#flush-collapse1-' + j);
      quiz_div.children[i].children[0].children[0].children[0].setAttribute('aria-controls', '#flush-collapse1-' + j);
      quiz_div.children[i].children[0].children[0].children[0].children[0].innerHTML = j;

      quiz_div.children[i].children[0].children[1].setAttribute('id', 'flush-collapse1-' + j);
      quiz_div.children[i].children[0].children[1].children[0].setAttribute('id', 'accordion-body1-' + j);

      let each_quiz_id = quiz_div.children[i].children[0].children[1].children[0].children[0].children[2].id;
      each_quiz_id = parseInt(each_quiz_id.split('-')[3]);
      quiz_div.children[i].children[0].children[1].children[0].children[0].children[2].setAttribute('id', 'del-quiz-' + j + '-' + each_quiz_id);
    }
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

  let countdown = JSON.parse(document.getElementById('json-minute').textContent);
  countdown = countdown * 60;
  console.log(countdown);
  let x = setInterval(function() {
    countdown--;

    let minutes = Math.floor((countdown % (60 * 60)) / (60));
    let seconds = Math.floor((countdown % (60)));

    if (countdown >= 0) {
      document.getElementById("minutes").innerHTML = minutes;
      document.getElementById("seconds").innerHTML = seconds;
    }
    if (countdown == 0) {
      document.getElementById("finish-quiz").click();
    }
  }, 1000);

}

// quiz-edit.html
if (current_url.split('/').find((element) => element == 'quiz') == 'quiz' && current_url.split('/').length == 4) {
  function add_question(id){
    let question_side = document.getElementById("question-side");
    const q_number = ++question_side.children.length;

    let accord_div = document.createElement("div");
    accord_div.className = "accordion accordion-flush";
    accord_div.setAttribute("style", "border-bottom: 1px solid #e4e4e4;");
    accord_div.setAttribute("id", "question-" + q_number);

    let item_div = document.createElement("div");
    item_div.className = "accordion-item";

    let accord_head = document.createElement("h2");
    accord_head.className = "accordion-header";

    let accord_btn = document.createElement("a");
    accord_btn.className = "accordion-button collapsed";
    accord_btn.setAttribute("data-bs-toggle", "collapse");
    accord_btn.setAttribute("data-bs-target", "#flush-collapse-" + q_number);
    accord_btn.setAttribute("aria-controls", "#flush-collapse-" + q_number);

    let accord_p = document.createElement("p");
    accord_p.innerHTML = q_number;

    accord_btn.appendChild(accord_p);
    accord_head.appendChild(accord_btn);

    let flush_div = document.createElement("div");
    flush_div.className = "accordion-collapse collapse";
    flush_div.setAttribute('id', 'flush-collapse-' + q_number);

    let flush_body = document.createElement("div");
    flush_body.className = "accordion-body";
    flush_body.setAttribute("id", "accordion-body-" + q_number);

    let q_label = document.createElement("label");
    q_label.innerHTML = "question";
    q_label.className = "form-label me-3";

    let q_hidden = document.createElement("input");
    q_hidden.setAttribute("type", "hidden");
    q_hidden.setAttribute("id", "question-id-" + q_number);
    q_hidden.setAttribute("name", "question-id-" + q_number);

    let q_input = document.createElement("input");
    q_input.className = "form-control mb-2";
    q_input.setAttribute("type", "text");
    q_input.setAttribute("placeholder", "Question here...");
    q_input.setAttribute("name", "question-" + q_number);
    q_input.setAttribute("required", "");

    let wrap_1 = document.createElement("div");
    wrap_1.className = "mb-2";
    wrap_1.setAttribute("style", "display: flex; align-items: center;");
    wrap_1.appendChild(q_label);
    wrap_1.appendChild(q_hidden);
    wrap_1.appendChild(q_input);

    let e_label = document.createElement("label");
    e_label.innerHTML = "explanation";
    e_label.className = "form-label me-3";

    let e_input = document.createElement("input");
    e_input.className = "form-control mb-2";
    e_input.setAttribute("type", "text");
    e_input.setAttribute("placeholder", "Explanation here...");
    e_input.setAttribute("name", "explanation-" + q_number);

    let wrap_2 = document.createElement("div");
    wrap_2.className = "mb-2";
    wrap_2.setAttribute("style", "display: flex; align-items: center;");
    wrap_2.appendChild(e_label);
    wrap_2.appendChild(e_input);

    let wrap_3 = document.createElement("div");
    wrap_3.setAttribute("style", "display:flex; align-items: center; justify-content: space-between;");

    let ans_btn = document.createElement("a");
    ans_btn.className = "btn btn-light mb-2";
    ans_btn.setAttribute("onclick", "add_answer(this.id)");
    ans_btn.setAttribute("id", "add-answer-" + q_number);
    let ans_i = document.createElement("i");
    ans_i.className = "fa-solid fa-plus";

    let ans_span = document.createElement("span");
    ans_span.innerHTML = " Add answer";

    ans_btn.appendChild(ans_i);
    ans_btn.appendChild(ans_span);

    let del_btn = document.createElement("a");
    del_btn.className = "btn btn-light mb-2";
    del_btn.setAttribute("onclick", "del_question(this.id)");
    del_btn.setAttribute("id", "del-question-" + q_number);
    let del_i = document.createElement("i");
    del_i.className = "fa-solid fa-trash";

    let del_span = document.createElement("span");
    del_span.innerHTML = " Delete question";

    del_btn.appendChild(del_i);
    del_btn.appendChild(del_span);
    
    let ans_ul = document.createElement("ul");
    ans_ul.setAttribute('id', 'answer-ul-' + q_number);

    wrap_3.appendChild(ans_btn);
    wrap_3.appendChild(del_btn);

    let question_id = document.createElement("p");
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
    try {
      htmx.ajax('GET', '/quiz/' + quiz_id + '/add-question', {target:'#question_id-' + q_number, swap:'innerHTML'}).then(() => {
        let question_btn = document.getElementById('quiz-1');
        question_btn.setAttribute("style", "pointer-events: none; width: 100%;");
  
        let timer2;
        timer2 = setTimeout(() => {
          question_btn.setAttribute("style", "pointer-events: all; width: 100%;");
        }, 1000);

        question_id = question_id.innerHTML;
        question_id = parseInt(question_id);
  
        q_hidden.value = question_id;

        if(question_id == "NaN") {
          question_side.removeChild(question_side.lastChild);
          console.log("last question is deleted.");
        }

        else {
          ans_btn.setAttribute("id", "add-answer-" + q_number + "-" + question_id);
          del_btn.setAttribute("id", "del-question-" + q_number + "-" + question_id);
    
          let toast = document.getElementById("toast");
          toast.setAttribute("style", "border: 2px solid #46f440;");
          toast.children[0].children[0].setAttribute("style", "background-color: #46f440;");
          let current_pos = window.scrollY + 25;
          toast.setAttribute("style", `display: block; top: ${current_pos}px;`);
          let text1 = document.getElementById("text-1");
          text1.innerHTML = "Success";
          let text2 = document.getElementById("text-2");
          text2.innerHTML = "Question has been successfully created";
          let timer1;
          toast.className = "custom-toast active";
        
          timer1 = setTimeout(() => {
              toast.className = "custom-toast";
              toast.setAttribute("style", "display: none;");
          }, 1000); //1s = 1000 milliseconds
  
        }
      });
    }
    catch (error) {
      let toast = document.getElementById("toast");
      toast.setAttribute("style", "border: 2px solid red;");
      toast.children[0].children[0].setAttribute("style", "background-color: red;");
      let current_pos = window.scrollY + 25;
      toast.setAttribute("style", `display: block; top: ${current_pos}px;`);
      let text1 = document.getElementById("text-1");
      text1.innerHTML = "Error";
      let text2 = document.getElementById("text-2");
      text2.innerHTML = "Question is not successfully created";
      let timer1;
      toast.className = "custom-toast active";
    
      timer1 = setTimeout(() => {
          toast.className = "custom-toast";
          toast.setAttribute("style", "display: none;");
      }, 1000); //1s = 1000 milliseconds

      question_side.removeChild(question_side.lastChild);
      console.log(error);
    }

  }

  function add_answer(id) {
    const q_number = id.match(/\d+/)[0];
    let answer_ul = document.getElementById('answer-ul-' + q_number);
    let a_number = ++document.getElementsByClassName("answer-div").length;

    let answer_div = document.createElement("div");
    answer_div.className = "m-2 me-0 answer-div";
    answer_div.setAttribute("style", "display: flex; align-items: center;");
    answer_div.setAttribute("id", "answer-" + q_number + "-" + a_number);

    let cor_input = document.createElement("input");
    cor_input.className = "me-3 form-check-input";
    cor_input.setAttribute("type", "checkbox");
    cor_input.setAttribute("name", "answer-cor-" + q_number + "-" + a_number);

    let hidden_input = document.createElement("input");
    hidden_input.setAttribute("type", "hidden");
    hidden_input.setAttribute("id", "answer-id-" + q_number + "-" + a_number);
    hidden_input.setAttribute("name", "answer-id-" + q_number + "-" + a_number);

    let answer_input = document.createElement("input");
    answer_input.className = "form-control";
    answer_input.setAttribute("type", "text");
    answer_input.setAttribute("name", "answer-body-" + q_number + "-" + a_number);
    answer_input.setAttribute("required", "");

    let delete_btn = document.createElement("a");
    delete_btn.setAttribute("id", "answer-del-" + q_number + "-" + a_number);
    delete_btn.setAttribute("onclick", "del_answer(this.id)");

    let delete_btn_icon = document.createElement("i");
    delete_btn_icon.className = "fa-solid fa-x ms-3";
    delete_btn_icon.setAttribute("style", "cursor: pointer;");

    answer_id_backend = document.createElement("p");
    answer_id_backend.setAttribute("id", "answer_id-" + q_number + "-" + a_number);
    answer_id_backend.setAttribute("style", "display: none;");

    delete_btn.appendChild(delete_btn_icon);

    answer_div.appendChild(cor_input);
    answer_div.appendChild(hidden_input);
    answer_div.appendChild(answer_input);
    answer_div.appendChild(delete_btn);
    answer_div.appendChild(answer_id_backend);
    answer_ul.appendChild(answer_div);

    const question_id = parseInt(id.split("-")[3]);
    try {
    htmx.ajax('GET', '/quiz/' + question_id + '/add-answer', {target:'#answer_id-' + q_number + "-" + a_number, swap:'innerHTML'}).then(() => {
      let answer_btn = document.getElementById(id);
      answer_btn.setAttribute("style", "pointer-events: none;");

      let timer2;
      timer2 = setTimeout(() => {
        answer_btn.setAttribute("style", "pointer-events: all;");
      }, 1000);
      
      let answer_id = document.getElementById("answer_id-" + q_number + "-" + a_number);
      answer_id = answer_id.innerHTML;
      answer_id = parseInt(answer_id);

      if(answer_id == "NaN") {
        answer_ul.removeChild(answer_ul.lastChild);
      }
      else {
        hidden_input.setAttribute("value", answer_id);  
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
              answers.children[k].children[1].setAttribute("value", hidden_id);
              answers.children[k].children[3].setAttribute("id", "answer-del-" + pk + '-' + hidden_id);
              answers.children[k].children[4].setAttribute("id", "answer_id-" + pk);
            }
            const answer_del_id = parseInt(answers.children[k].children[3].id.split("-")[4]);
            answers.children[k].children[3].setAttribute("id", "answer-del-" + pk + '-' + answer_del_id);          
            answer_number++;
          }
        }
  
        let toast = document.getElementById("toast");
        toast.setAttribute("style", "border: 2px solid #46f440;");
        toast.children[0].children[0].setAttribute("style", "background-color: #46f440;");
        let text1 = document.getElementById("text-1");
        text1.innerHTML = "Success";
        let text2 = document.getElementById("text-2");
        text2.innerHTML = "Answer has been successfully created";
        let timer1;
        toast.className = "custom-toast active";
        let current_pos = window.scrollY + 25;
        console.log(current_pos);
        toast.setAttribute("style", `display: block; top: ${current_pos}px;`);
      
        timer1 = setTimeout(() => {
            toast.className = "custom-toast";
            toast.setAttribute("style", "display: none;");
        }, 1000); //1s = 1000 milliseconds
      }
    });
    }
    catch (error) {
      answer_ul.removeChild(answer_ul.lastChild);
      console.log("deleted last child");
    }
  }

  function del_answer(id) {
    const number = id.match(/(\d+)-(\d+)/)[0];
    answer_div = document.getElementById("answer-" + number);

    try {
      htmx.ajax('GET', '/quiz/' + parseInt(id.split("-")[4]) + '/delete-answer', '#success');
      answer_div.remove();
      let toast = document.getElementById("toast");
      toast.setAttribute("style", "border: 2px solid #46f440;");
      toast.children[0].children[0].setAttribute("style", "background-color: #46f440;");
      let current_pos = window.scrollY + 25;
      toast.setAttribute("style", `display: block; top: ${current_pos}px;`);
      let text1 = document.getElementById("text-1");
      text1.innerHTML = "Success";
      let text2 = document.getElementById("text-2");
      text2.innerHTML = "Answer has been successfully deleted";
      let timer1;
      toast.className = "custom-toast active";
    
      timer1 = setTimeout(() => {
          toast.className = "custom-toast";
          toast.setAttribute("style", "display: none;");
      }, 1500); //1s = 1000 milliseconds
    }
    catch (error) {
      let toast = document.getElementById("toast");
      toast.setAttribute("style", "border: 2px solid red;");
      toast.children[0].children[0].setAttribute("style", "background-color: red;");
      let current_pos = window.scrollY + 25;
      toast.setAttribute("style", `display: block; top: ${current_pos}px;`);
      let text1 = document.getElementById("text-1");
      text1.innerHTML = "Error";
      let text2 = document.getElementById("text-2");
      text2.innerHTML = "Answer is not deleted successfully";
      let timer1;
      toast.className = "custom-toast active";
    
      timer1 = setTimeout(() => {
          toast.className = "custom-toast";
          toast.setAttribute("style", "display: none;");
      }, 1500); //1s = 1000 milliseconds
    }

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
    try {
      htmx.ajax('GET', '/quiz/' + parseInt(id.split("-")[3]) + '/delete-question', '#success');
      question_div.remove();
      let toast = document.getElementById("toast");
      toast.setAttribute("style", "border: 2px solid #46f440;");
      toast.children[0].children[0].setAttribute("style", "background-color: #46f440;");
      let current_pos = window.scrollY + 25;
      toast.setAttribute("style", `display: block; top: ${current_pos}px;`);
      let text1 = document.getElementById("text-1");
      text1.innerHTML = "Success";
      let text2 = document.getElementById("text-2");
      text2.innerHTML = "Question has been successfully deleted";
      let timer1;
      toast.className = "custom-toast active";
    
      timer1 = setTimeout(() => {
          toast.className = "custom-toast";
          toast.setAttribute("style", "display: none;");
      }, 1500); //1s = 1000 milliseconds
    }

    catch (error) {
      let toast = document.getElementById("toast");
      toast.setAttribute("style", "border: 2px solid red;");
      toast.children[0].children[0].setAttribute("style", "background-color: red;");
      let current_pos = window.scrollY + 25;
      toast.setAttribute("style", `display: block; top: ${current_pos}px;`);
      let text1 = document.getElementById("text-1");
      text1.innerHTML = "Error";
      let text2 = document.getElementById("text-2");
      text2.innerHTML = "Question is not successfully deleted";
      let timer1;
      toast.className = "custom-toast active";
    
      timer1 = setTimeout(() => {
          toast.className = "custom-toast";
          toast.setAttribute("style", "display: none;");
      }, 1500); //1s = 1000 milliseconds
    }

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
