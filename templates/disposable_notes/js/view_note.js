function get_doc(hex) {
    let input = hex.replace(/[^A-Fa-f0-9]/g, "");
    if (input.length % 2) {
        console.log("cleaned hex string length is odd.");
        return;
    }

    let binary = [];
    for (let i = 0; i < input.length / 2; i++) {
        let h = input.substr(i * 2, 2);
        binary[i] = parseInt(h, 16);
    }

    return new Uint8Array(binary);
}

function escapeHtml(unsafe) {
    return unsafe
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;")
        .replace(/&lt;a href=&quot;/g, "<a href=\"")
        .replace(/&quot;&gt;/g, "\">")
        .replace(/&lt;\/a&gt;/g, "</a>")
        .replace(/&lt;b&gt;/g, "<b>")
        .replace(/&lt;\/b&gt;/g, "</b>")
        .replace(/&lt;u&gt;/g, "<u>")
        .replace(/&lt;\/u&gt;/g, "</u>")
        .replace(/&lt;i&gt;/g, "<i>")
        .replace(/&lt;\/i&gt;/g, "</i>")
        .replace(/&lt;h1&gt;/g, "<h1>")
        .replace(/&lt;\/h1&gt;/g, "</h1>")
        .replace(/&lt;h2&gt;/g, "<h2>")
        .replace(/&lt;\/h2&gt;/g, "</h2>")
        .replace(/&lt;h3&gt;/g, "<h3>")
        .replace(/&lt;\/h3&gt;/g, "</h3>")
        .replace(/&lt;h4&gt;/g, "<h4>")
        .replace(/&lt;\/h4&gt;/g, "</h4>")
        .replace(/&lt;h5&gt;/g, "<h5>")
        .replace(/&lt;\/h5&gt;/g, "</h5>")
        .replace(/&lt;h6&gt;/g, "<h6>")
        .replace(/&lt;\/h6&gt;/g, "</h6>")
        .replace(/&lt;hr&gt;/g, "<hr style='height: 2px; color: black'>")
        .replace(/\n/g, "<br>")
        .replace(/&lt;br&gt;/g, "<br>")
        .replace(/&lt;rspan&gt;/g, "<span style='color: red'>")
        .replace(/&lt;gspan&gt;/g, "<span style='color: #09b809'>")
        .replace(/&lt;bspan&gt;/g, "<span style='color: blue'>")
        .replace(/&lt;\/span&gt;/g, "</span>")
        .replace(/&lt;lp&gt;/g, "<p style='text-align: left'>")
        .replace(/&lt;rp&gt;/g, "<p style='text-align: right'>")
        .replace(/&lt;\/p&gt;/g, "</p>")
        .replace(/&lt;ms&gt;/g, "<span class=\"user-select-all font-monospace\">")
        .replace(/&lt;\/ms&gt;/g, "</span>");
}

function view_note() {
    let btn = document.getElementById("sure");
    btn.style.backgroundColor = "transparent";
    btn.style.border = "transparent";
    btn.style.color = "transparent";
    btn.innerHTML = "<div class=\"spinner-border text-light\" style='width: 25px; height: 25px' role=\"status\">" +
        "<span class=\"visually-hidden\">Loading...</span>" +
        "</div>";

    let warning = document.getElementById("warning");
    let note_id = document.getElementById("note-id").value;
    const key = $(location).attr('hash').substr(1);
    $.ajax({
        url: "/api/note/" + note_id,
        method: "DELETE",
        success: function (data) {
            let enc = data["content"];
            let counter = data["counter"];
            let msg = decrypt(enc, counter, key);
            if (data['doc'] === false) {
                msg = escapeHtml(msg);
                warning.innerHTML = "<p class='muted'>{{ data['js save data'] }} " +
                    "</p>" +
                    "<div class=\"alert alert-light\" role=\"alert\" style=\"word-wrap: break-word\">" +
                    msg +
                    "</div>" +
                    "<a href='/' onclick=\"window.open('','_self').close();\" class=\"btn btn-secondary\" " +
                    "                    style=\"width: 100%; margin-top: 10px; color: white\">{{ data['Выйти'] }}</a>";
            } else {
                let byteArray = get_doc(textToHex(msg));
                let doc = window.URL.createObjectURL(new Blob([byteArray],
                    {type: data["ext"]}));
                let fext = data["ext"];
                if (fext === "") {
                    fext = "";
                } else {
                    fext = fext.split("/")[1];
                }
                warning.innerHTML = "<p class='muted'>{{ data['js save data'] }} " +
                    "</p>" +
                    "<div class=\"alert alert-light\" role=\"alert\" style=\"word-wrap: break-word\">" +
                    "<a href='" + doc + "' download='file." + fext + "'>" +
                    "{{ data['download file'] }}" +
                    "</a>" +
                    "</div>" +
                    "<a href='/' onclick=\"window.open('','_self').close();\" class=\"btn btn-secondary\" " +
                    "                    style=\"width: 100%; margin-top: 10px; color: white\">{{ data['Выйти'] }}</a>";
            }

        }, error: function (xhr, ajaxOptions, thrownError) {
            if (xhr.status === 500) {
                alert("{{ data['js 500 error'] }}");
            } else {
                if (xhr.status === 404) {
                    alert("{{ data['js already read'] }}");
                } else {
                    alert("{{ data['js unknown error'] }}");
                }
            }
        }
    });
}