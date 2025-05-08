function loadCompany(event) {
    // prevents reload
    event.preventDefault();

    // grabs ticker from input box
    const ticker = document.getElementById("ticker").value.trim();
    if(!ticker) {
        alert("Please enter a valid ticker symbol");
        return;
    }

    // fetch request to flask
    fetch(`/company?ticker=${ticker}`)
        .then(res => res.json())
        .then(data => {
            if(data.error) {
                alert(data.error);
                document.getElementById("output").innerHTML = "";
                return;
            }

        });
}