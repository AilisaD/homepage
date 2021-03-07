function weather() {
    let req = new XMLHttpRequest();
    req.onreadystatechange = function () {
        if (req.readyState === 4 && req.status === 200) {
            let res = JSON.parse(req.response)
            console.log(res)
            document.getElementById("temp").innerText = res['fact'][1];
            document.getElementById("temp_like").innerText = "("+res['fact'][2]+")";
            document.getElementById("cond").innerText = res['fact'][3];
            res['forecast'].forEach(
                function (item){
                    let str = item[0] + ": от " + item[1] + " до " + item[2] + " " + item[3] + " ";
                    let label = document.createElement('label');
                    label.id = "part"+item[0];
                    label.innerText = str;
                    document.getElementById("forecast").insertAdjacentElement('beforeend', label);
                    let br = document.createElement('br');
                    document.getElementById("part"+item[0]).insertAdjacentElement('beforeend', br);
                }
            )

        }
    }
    req.open('GET', '/weather', true);
    req.send();
    setTimeout(weather, 1000*60*30);
}
weather();
