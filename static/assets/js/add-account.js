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

const showEmptyMessage = (elem) => {
    elem.html(
        `
        <p style="text-align: center; padding-top: 5px; padding-bottom: 5px" class=mb-0>
            No saved accounts contain that search term.
        </p>
        `
    )
}
  
const showAccounts = (elem, data) => {
    data.forEach((account) => {
        let li = document.createElement("li");
        let name = '';
        if (account.name)
            name = account.name;

        $(li).html(
            `
            <a href='#'>
                <span id='name'>${name}</span>
                <span id='number'><small>${account.number}</small></span>
                <span id='bank-code' style='display: none'>${account.provider_code}</span>
                <span id='bank-name' style='display: none'>${account.provider_name}</span>
            </a>
            `
        );
        elem.append(li);
    });
};

const showError = (elem) => {
    elem.html(
        `
        <p style="border: solid 1px #ddd; text-align: center; padding-top: 5px; padding-bottom: 5px" class=mb-0>
            Request failed.
        </p>
        `
    );
};

const getAccounts = (q, type) => {
    const site = $('#id_site').val();
    const url = `${site}/get-accounts`;
    const element = $("#accounts-list");

    element.fadeIn();

    axios.get(url, {
        params: {
          q: q,
          type: type
        }
    })
    .then((response) => {
        if (response.status === 200) {
            const data = response.data;
            element.empty();

            if (data.length === 0) {
                showEmptyMessage(element);
            } else {
                showAccounts(element, data);
            }
        }
    })
    .catch((error) => {
        showError(element);
    })
};

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

const CURRENCY_ACCOUNT_TYPE_MAP = {
    'NGN': 'bank',
    'GHS': 'wallet'
}

$("#id_search").keyup((e) => {
    const currency = $('#id_currency').val();
    const type = CURRENCY_ACCOUNT_TYPE_MAP[currency];
    const q = $(e.currentTarget).val();
    if (q.length >= 2) {
        getAccounts(q, type);
    } else {
        getAccounts('', type);
    }
});

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