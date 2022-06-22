const hD = '0123456789abcdef';

function dec2hex(d) {
    let h = hD.substr(d & 15, 1);
    while (d > 15) {
        d >>= 4;
        h = hD.substr(d & 15, 1) + h;
    }
    return h;
}

let uint8View;

function Convert() {
    let hexText = "";
    const separator1 = "", separator2 = "";
    const newline = false;
    for (let i = 0; i < uint8View.length; i++) {
        const charVal = uint8View[i];
        hexText = hexText + separator1 + (charVal < 16 ? "0" : "") + dec2hex(charVal);
        if (i < uint8View.length - 1) {
            hexText += separator2;
        }
        if (newline) {
            if ((i % 16) === 15) {
                hexText += "\n";
            }
        }
    }
    document.forms["new-note"]["hex"].value = hexToText(hexText);
    create_note();

}

function readFileAsArray(file) {
    const reader = new FileReader();
    reader.onload = function () {
        const arr = reader.result;
        uint8View = new Uint8Array(arr);
        Convert();
    };
    reader.readAsArrayBuffer(file);
}

const openFile = function (input) {
    document.forms["new-note"]["ext"].value = input.files[0].type;
    readFileAsArray(input.files[0]);
};

const fileInput = document.getElementById('file');
fileInput.onchange = () => {
    openFile(fileInput);
}

function create_note() {
    let btn = document.getElementById("submit-btn");
    btn.style.backgroundColor = "transparent";
    btn.style.border = "1px solid white";
    btn.style.color = "white";
    btn.innerHTML = "<div class=\"spinner-border text-light\" style='width: 25px; height: 25px' role=\"status\">" +
        "<span class=\"visually-hidden\">Loading...</span>" +
        "</div>";

    let content_f = document.forms["new-note"]["content"].value;
    let hex = document.forms["new-note"]["hex"].value;
    let ext = document.forms["new-note"]["ext"].value;
    let deletein = document.forms["new-note"]["deleteIn"].value;
    let res;
    let doc;
    if (!(hex === "empty")) {
        res = encrypt(hex);
        doc = true;
    } else {
        if (!(0 < content_f.length && content_f.length < 5001)) {
            alert("{{ data['Некорректная длина записки!'] }}");
            let btn = document.getElementById("submit-btn");
            btn.style.backgroundColor = "";
            btn.style.border = "";
            btn.style.color = "";
            btn.innerHTML = "{{ _('create note btn') }}";
            return;
        }
        res = encrypt(content_f);
        doc = false;
    }
    let key = res[0];
    let counter = res[1];
    let content = res[2];
    $.ajax({
        url: "/api/note",
        method: "POST",
        data: {"content": content, "counter": counter, "deletein": deletein, "doc": doc, "ext": ext},
        success: function (data) {
            let note_id = data["id"];
            document.getElementById("form").innerHTML = "" +
                "<p style='margin-top: 20px; margin-bottom: 10px;'>{{ data['link info'] }}</p>" +
                "<div style=\"text-align: center; margin-top: 10px;\">" +
                "  <input id=\"tocopy\" " +
                "         class=\"form-control\" onclick=\"copy_link()\" " +
                "         value=\"https://pn" + "n.im/" + note_id + "#" + key + "\" readonly>" +
                "  <div style=\"margin-top: 10px\" id=\"copy-btn\">" +
                "    <button onclick=\"copy_link()\" class=\"btn btn-primary\" " +
                "            style=\"width: 100%\">{{ data['Скопировать'] }}</button>" +
                "  </div>" +
                "</div>";
        }, error: function (xhr, ajaxOptions, thrownError) {
            let btn = document.getElementById("submit-btn");
            btn.style.backgroundColor = "";
            btn.style.border = "";
            btn.style.color = "";
            btn.innerHTML = "{{ _('create note btn') }}";
            if ((xhr.status === 400) || (xhr.status === 413)) {
                if (doc) {
                    alert("{{ data['heavy doc'] }}");
                } else {
                    alert("{{ data['heavy content'] }}");
                }
            } else {
                if (xhr.status === 500) {
                    alert("{{ data['js 500 error'] }}");
                } else {
                    alert("{{ data['js unknown error'] }}");
                }
            }
        }
    });
}

function copy_link() {
    const copyText = document.getElementById("tocopy");
    copyText.select();
    document.execCommand("copy");
    let btn = document.getElementById("copy-btn");
    btn.innerHTML = "<button onclick=\"copy_link()\" class=\"btn btn-secondary\" " +
        "                    style=\"width: 100%\" disabled>{{ data['Скопировано'] }}</button>";
}

function advancedMenu() {
    const collapse = document.getElementById("collapse");
    const icon1 = document.getElementById("advancedIcon1");
    const icon2 = document.getElementById("advancedIcon2");
    if (collapse.style.display === "none") {
        collapse.style.display = "block";
        icon1.src = "/static/svg/angle-double-up.svg";
        icon2.src = "/static/svg/angle-double-up.svg";
    } else {
        collapse.style.display = "none";
        icon1.src = "/static/svg/angle-double-down.svg";
        icon2.src = "/static/svg/angle-double-down.svg";
    }
}

function handleFileSelect(evt) {
    evt.stopPropagation();
    evt.preventDefault();
    const file = evt.dataTransfer.files[0];
    document.forms["new-note"]["ext"].value = file.type;
    readFileAsArray(file);
}

const dropZone = document.getElementById('note-content');

function handleDragEnter(evt) {
    evt.stopPropagation();
    evt.preventDefault();
    dropZone.style.border = "dashed rgba(255,255,255,0.8) 3px";
    dropZone.style.backgroundColor = "rgba(255,255,255,0.3)";

}

function handleDragOver(evt) {
    evt.stopPropagation();
    evt.preventDefault();
    dropZone.style.border = "dashed white 3px";
    dropZone.style.backgroundColor = "rgba(255, 255, 255, 0.6)";
}

const body = document.getElementsByTagName("body")[0];
body.addEventListener('dragenter', handleDragEnter, false);
dropZone.addEventListener('dragover', handleDragOver, false);
dropZone.addEventListener('drop', handleFileSelect, false);
