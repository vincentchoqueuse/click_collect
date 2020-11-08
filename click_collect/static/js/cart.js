
function update_price_total()
{
    var elements = document.getElementsByClassName("product_row");
    var total = 0;
    for (var indice=0;indice<elements.length;indice++)
    {
        var element = elements[indice];
        var price = parseFloat(element.getElementsByClassName("price")[0].innerHTML);
        var quantity = parseFloat(element.getElementsByClassName("quantity")[0].value);
        var total_temp = quantity*price;
        element.getElementsByClassName("total_price")[0].innerHTML = total_temp.toFixed(2);
        total += total_temp;
    }
    document.getElementById("total").innerHTML = total.toFixed(2);
}