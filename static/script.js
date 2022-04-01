


function makePost()
{
  console.log("Sending Post request");
  //const one = document.getElementById(/*item ID*/).value

  fetch(`${location.pathname}/addToCart`, {
    method: "post",
    headers: { "Content-type": "application/json" },
    body: JSON.stringify({"todo": `${1}`}),
  })
  .then(res => res.json())
  .then(
    (res) => {
      console.log(`Response: ${res}`);
    },
    (error) => {
      console.log(`Error sending item: ${error}`);
    }
  );
}

async function makeLocal()
{
    //cartLink = document.getElementById(/*the link button for the cart*/)
    //when the button is pressed add the item to localstorage and update properties of the CartLink

    itemId = (location.pathname.split('/shop/'))[1].replaceAll(",","");
    await fetch(`/fetchItem/${itemId}`)
         .then((response) => {
			return response.json();
		})
        .then((result) => {
            update(result,itemId)
        })
		.catch((error) => {
            console.error('Error:', error);
		});
    stored = sessionStorage.getItem('userCart')
    if (stored === '')
    {
        console.log("nothing added yet");
    }
    //will they stay updated idk tbh
    //when items are ordered and the order comes through then you need the item id and stuff
    //what about when the cart page is loaded just get item detail from local storage maybe i could get it from the db too
    //yeah def fetch('something i made') somehow pass in a list of items from local storage could be a string with id's thats parsed
    //show the cart from localstorage

    //need to post a list of items to the database so that order is appended.
    //more specificcally when the order is placed items are appended to order and order is appended to user but it doesnt have to.
}
function update(result,itemId)
{
    cart = sessionStorage.getItem('userCart');
    let cartJson;
    if(cart)
    {
        cartJson = JSON.parse(cart);
        //if item already exists then update quantity
        if(cartJson.hasOwnProperty(`item${itemId}`))
        {
            amt = cartJson[`item${itemId}`].quantity;
            if(amt)
            {
                amt = amt+1;
            }
            else
            {
                amt = 2;
            }
            cartJson[`item${itemId}`].quantity = amt;
            sessionStorage.setItem('userCart',JSON.stringify(cartJson));
        }
        else//item does not exist yet create item and set to input from fetch
        {
            cartJson[`item${itemId}`] = result[`item${itemId}`];
            sessionStorage.setItem('userCart',JSON.stringify(cartJson));
        }
    }
    else//user cart does not exist yet
    {
        sessionStorage.setItem('userCart',JSON.stringify(result));
    }
}

function setup() {
	document.getElementById("addCart").addEventListener("click", makeLocal);
    //timeoutID = window.setTimeout(poller, timeout);
}
window.addEventListener("load", setup);
//what does the flow look like here basically a user adds items to their cart
//if logged in it gets added to the user object but deleted when they log out or leave

//if not logged in a json cart list is used per session to keep the list of
//items in the cart all cart items are stored in the list
//dont rly need a poller when the user hits add cart the card should be updated
