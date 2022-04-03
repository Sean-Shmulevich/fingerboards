


async function makePost()
{
  console.log("Sending Post request");
  //const one = document.getElementById(/*item ID*/).value
  itemId = (location.pathname.split('/shop/'))[1];
  a = await fetch(`/${itemId}/addToCart`, {
    method: "post",
    headers: { "Content-type": "application/json" },
    body: JSON.stringify({"id": `${itemId}`}),
  });

}

async function makeLocal()
{
    //cartLink = document.getElementById(/*the link button for the cart*/)
    //when the button is pressed add the item to localstorage and update properties of the CartLink
    console.log("bro");
    itemId = (location.pathname.split('/shop/'))[1].replaceAll(",","");
    a = await fetch(`/fetchItem/${itemId}`)
    .then(res => res.json())
    .then(
      (res) => {
        update(res,itemId);
        console.log(`Response: ${res}`);
      },
      (error) => {
        console.log(`Error sending item: ${error}`);
      }
    );
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
    layoutPrice = document.querySelector("#layout-cart-total");
    layoutCount = document.querySelector("#layout-cart-count");
    console.log(layoutPrice);
}

function makeCart()
{
  window.addEventListener("load", updateCart);

  //document.createElement
}

function sendJson()
{
  console.log("Sending POST request");
  if(typeof sessionStorage.userCart === 'undefined')
  {
    return;
  }

fetch(`/cart`, {
    method: "post",
    headers: { "Content-type": "application/json" },
    body: sessionStorage.userCart
  })
}

function setup() {

  document.querySelector("#addCart").addEventListener("click", makePost);
  //timeoutID = window.setTimeout(sendJson, 1000);
}
window.addEventListener("load", setup);
//what does the flow look like here basically a user adds items to their cart
//if logged in it gets added to the user object but deleted when they log out or leave

//if not logged in a json cart list is used per session to keep the list of
//items in the cart all cart items are stored in the list
//dont rly need a poller when the user hits add cart the card should be updated
