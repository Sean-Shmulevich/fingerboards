function makeCart()
{
  window.addEventListener("load", set);//wait for the

  function set()
  {
    let tab = document.getElementById("the div it should be in");
  }

}

function setup() {
  document.getElementById("goToCart").addEventListener("click", makeCart);
    //timeoutID = window.setTimeout(poller, timeout);
}
window.addEventListener("load", setup);
