function make_str_part(part){
    let str = part[0] + " ";
    if(part[1] !== part[2]){
        str = str + part[1] + " \u2026 " + part[2] + " " + part[3] + " "
    }
    else {
        str = str + part[1] + " " + part[3] + " "
    }
    return str;
}

function weather() {
    let req = new XMLHttpRequest();
    req.onreadystatechange = function () {
        if (req.readyState === 4 && req.status === 200) {
            let res = JSON.parse(req.response)
            document.getElementById("temp").innerText = res['fact'][1];
            document.getElementById("temp_like").innerText = "("+res['fact'][2]+")";
            document.getElementById("cond").innerText = res['fact'][3];

            document.getElementById("img").src = res['fact'][4];
            document.getElementById("img_part_one").src = res['forecast'][0][4];
            document.getElementById("part_one").innerText = make_str_part(res['forecast'][0]);
            document.getElementById("img_part_two").src = res['forecast'][1][4];
            document.getElementById("part_two").innerText = make_str_part(res['forecast'][1]);

        }
    }
    req.open('GET', '/weather', true);
    req.send();
    setTimeout(weather, 1000*60*30);
}
weather();
