/*
In this file we'll be making all requests to retireve and add cupcakes from the client side 
using axios.
*/

const BASE_URL = "http://localhost:5000/api"

//This function generates cupcake html

function generate_html(cupcake){

    return `
    <div data-cupcake-id=${cupcake.id}>
        <li>
            ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
            <button class="dlt-cupcake">X</button>
        </li>

        <img class="Cupcake-img" 
             src="${cupcake.image}" 
             alt="(no image provided)">
    </div>
    `
}

// Make an ajax request to get cupcake salready in the db on the page.

async function showInitialCupcakes(){

    const res = await axios.get(`${BASE_URL}/cupcakes`);

    for(let cupcakeData in res.data.cupcakes){
        let newCupcake = $(generate_html(cupcakeData));
        $('#cupcake-list').append(newCupcake);
    }
}

// Handle new cupcake form 

$('#cupcake-form').on("submit", addCupcake(evt) )

async function addCupcake(evt){
    evt.preventDefault()

    // We get all the values from the form and we make a post request via AJAX

    flavor = $('#cupcake-flavor').val()
    size = $('#cupcake-size').val()
    rating = $('#cupcake-rating').val()
    image = $('#cupcake-image').val()

    const res = await axios.post(`${BASE_URL}/cupcakes`, {
        params: {
            'flavor': flavor,
            'size': size,
            'rating': rating,
            'image': image
        }
    })

    let newCupcake = $(generate_html(res.data.cupcake));
    $('#cupcake-list').append(newCupcake);
    $('#cupcake-form').trigger("reset");
}

// Handle the delete button: delete cupcake

$('#cupcake-list').on("click", ".dlt-cupcake", async function(e){

    e.preventDefault();
    let $cupcake = $(e.target).closest("div");
    let cupcakeId = $cupcake.attr("data-cupcake-id");

    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`)
    $(this).parent().remove()


});

$(showInitialCupcakes);