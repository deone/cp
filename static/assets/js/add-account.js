const setProviderName = () => {
    const name = $("#id_provider_code").children('option:selected').text();
    $("#id_provider_name").val(name);
}

setProviderName();

$("#id_provider_code").change(() => {
    setProviderName();
})