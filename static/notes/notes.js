function set_cookie(name, value) {
    const now = new Date();
    const time = now.getTime();
    const expireTime = time + 3600 * 1000 * 24 * 365;
    now.setTime(expireTime);
    document.cookie = name + '=' + value + ';expires=' + now.toUTCString() + ';path=/';
}

function change_lang(lang) {
    set_cookie("lang", lang)
}

function hide_description() {
    let description = document.getElementById("description-banner");
    let do_not_show_again = document.getElementById("do-not-show-again-tick");
    if (do_not_show_again.checked) {
        set_cookie("showdescription", "false");
    } else {
        set_cookie("showdescription", "true");
    }
    description.innerHTML = "";
}