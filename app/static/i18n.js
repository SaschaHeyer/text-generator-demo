var languages = Array.from(document.getElementsByClassName('language'));
var xhttp = new XMLHttpRequest();
var langDocument = {};
 
languages.forEach(function(value, index){
    languages[index].addEventListener('click', function(){
        switchLanguage(this.dataset.lang);
    });
});

function switchLanguage(language){
    doc = document.getElementById("HTML");
    doc.setAttribute('lang', language);
    console.log("changing language");
    xhttp.open("GET", "../static/i18n/" + language + ".json", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send();
}

xhttp.onreadystatechange = function(){
    if (this.readyState === 4 && this.status === 200) {
        langDocument = JSON.parse(this.responseText);
        processLangDocument();
    }
};
function processLangDocument(){
    var tags = document.querySelectorAll('span,img,a,label,li,option,h1,h2,h3,h4,h5,h6,textarea');
    Array.from(tags).forEach(function(value, index){
        var key = value.dataset.langkey;
        if(langDocument[key]) {
            if(value.tagName === "TEXTAREA") value.placeholder = langDocument[key];
            else value.innerText = langDocument[key];
        }
    });
}