function loadCompany() {
    const ticker = document.getElementById("ticker").value.trim();
    if(!ticker) {
        alert("Please enter a valid ticker symbol");
        return;
    }

    // fetch request to flask
    fetch(`/company?ticker=${ticker}`)
        .then(res => res.json())
        .then(data => {
            console.log(data);
        });
}