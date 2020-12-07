function getCookie(name) {
    // Split cookie string and get all individual name=value pairs in an array
    var cookieArr = document.cookie.split(";");
    
    // Loop through the array elements
    for(var i = 0; i < cookieArr.length; i++) {
        var cookiePair = cookieArr[i].split("=");
        
        /* Removing whitespace at the beginning of the cookie name
        and compare it with the given string */
        if(name == cookiePair[0].trim()) {
            // Decode the cookie value and return
            return decodeURIComponent(cookiePair[1]);
        }
    }
    
    // Return null if not found
    return null;
}

const getRecipientName = (accountNumber, bank) => {
    const url = $('#id_url').val();
    const headers = {'Content-Type': 'application/json'};
    const _key = getCookie('key');
  
    const data = {
        account_number: accountNumber,
        account_bank: bank,
        seckey: _key 
    };

    axios.post(url, data, {
        headers: headers
    })
    .then((response) => {
        if (response.status === 200) {
            const recipient = response.data.data;
            $("#progress").hide();
            $("#id_name").val(recipient['fullname']);
            $('#btnSubmit').removeAttr("disabled");
        } else {
            alert("Sorry, we couldn't find that account. Please check and retry.");
        }
    })
    .catch((error) => {
        console.log(error);
    });
}

const setProviderName = () => {
    const name = $("#id_provider_code").children('option:selected').text();
    $("#id_provider_name").val(name);
}

setProviderName();

$("#id_provider_code").change(() => {
    setProviderName();

    $("#id_number").keyup((e) => {
        const bank = $("#id_provider_code").val();
        if (bank) {
            const accountNumber = $(e.currentTarget).val();
            if (accountNumber.length == 10) {
                $("#progress").show();
                getRecipientName(accountNumber, bank);
            }
        }
    });
})