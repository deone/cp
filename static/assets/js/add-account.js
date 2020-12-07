const getRecipientName = (accountNumber, bank) => {
    const url = $('#id_url').val();
    const secretKey = $('#id_secret_key').val();
  
    const data = {
        account_number: accountNumber,
        account_bank: bank,
        seckey: secretKey
    };
  
    const headers = {'Content-Type': 'application/json'};
  
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