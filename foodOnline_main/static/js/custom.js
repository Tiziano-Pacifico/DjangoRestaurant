
let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['it']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
        return
    }
    else{
        console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields

    var latitude = place.geometry.location.lat();
    var longitude = place.geometry.location.lng();
    var address = document.getElementById('id_address').value

    $('#id_latitude').val(latitude);
    $('#id_longitude').val(longitude);
    $('#id_address').val(address);

    for(var i=0; i<place.address_components.length; i++) {
        for(var j=0; j<place.address_components[i].types.length; j++) {
             // get state
             if(place.address_components[i].types[j] == 'administrative_area_level_1'){
                $('#id_state').val(place.address_components[i].long_name);
            }
            // get city
            if(place.address_components[i].types[j] == 'locality'){
                $('#id_city').val(place.address_components[i].long_name);
            }
            // get pincode
            if(place.address_components[i].types[j] == 'postal_code'){
                $('#id_pin_code').val(place.address_components[i].long_name);
            }else{
                $('#id_pin_code').val("");
            }
        }
    }

}

$(document).ready(function(){
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url')
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                if(response.status=='login_required') {
                    Swal.fire({
                        title: "Login required",
                        text: response.message,
                        icon: "error"
                      }).then(function(){
                        window.location = '/login'
                      });
                }else if(response.status=='Failed'){
                    Swal.fire({
                        title: "Request Failure",
                        text: response.message,
                        icon: "error"
                      })
                }else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty)
                }
            }
        })
    })

    $('.remove_from_cart').on('click', function(e){
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url')
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                if(response.status=='login_required') {
                    Swal.fire({
                        title: "Login required",
                        text: response.message,
                        icon: "error"
                      }).then(function(){
                        window.location = '/login'
                      });
                }else if(response.status=='Failed'){
                    Swal.fire({
                        title: "Request Failure",
                        text: response.message,
                        icon: "error"
                      })
                }else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty)
                }
            }
        })
    })

    //place the cart item quantity on load
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)
    })
});


