function showDate(){
    let date = new Date();
    let d = date.getDate();
    let m = date.getMonth() + 1;
    let date_next = new Date(date.getFullYear(), m-1, d+1, 0, 0, 0);
    d = (d < 10) ? "0" + d : d;
    m = (m < 10) ? "0" + m : m;
    let dd = d + "." + m;
    document.getElementById("Date").innerText = dd;
    document.getElementById("Date").textContent = dd;
    let diff = date_next - date;
    setTimeout(showDate, diff);
}

showDate();