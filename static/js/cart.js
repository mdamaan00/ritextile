var update = document.getElementsByClassName('prod-btn');
  var total = document.getElementsByClassName('item-total');
  var row = document.getElementsByClassName('prod-row');
  var grandTotal = document.getElementsByClassName("grand-total");
  var tax = document.getElementsByClassName("tax");
  const v = document.getElementById("total-items");
  const all_items = document.getElementById("cart-items");
  const quan = document.getElementsByClassName("item-quantity");
  const loading = document.getElementsByClassName("loading");
  for (var i = 0; i < update.length; i++) {
    update[i].addEventListener('click', function (e) {
      e.preventDefault()
      var productId = this.dataset.product;
      var action = this.dataset.action;
      console.log('productId:', productId)
      console.log('action:', action)
      console.log('USER:', user)
      if (user === "AnonymousUser") {
        console.log('Not logged in')
      }
      else {
        
        updateOrder(productId, action)
      }
      //AJAX
      function updateOrder(productId, action) {
        const mainCard = document.getElementById("main-card");
        for (var i = 0; i < loading.length; i++) {
          if (loading[i].dataset.product == productId) {
            loading[i].classList.remove("hidden");
          }
        }
        mainCard.classList.add('disabled');
        $.ajax({
          headers: { "X-CSRFToken": token },
          type: "POST",
          url: prodURL,
          data: { 'productId': productId, 'action': action },
          dataType: "json",
          success: function (data) {
            console.log(data.msg);
            console.log(data.quantity);
            if (action === "delete") {
              location.reload();
            }
            for (var i = 0; i < quan.length; i++) {
              if (quan[i].dataset.product == productId && data.quantity > 0) {
                for (var j = 0; j < loading.length; j++) {
                  if (loading[j].dataset.product == productId) {
                    loading[i].classList.add("hidden");
                  }
                }
                mainCard.classList.remove('disabled');
                quan[i].innerHTML = data.quantity;
                total[i].innerHTML = data.total;
                v.innerHTML = data.items;
                all_items.innerHTML = data.items;
                grandTotal[0].innerHTML = data.orderTotal;
                grandTotal[1].innerHTML = data.grandTotal;
                tax[0].innerHTML = data.tax;
              }
              else if (data.quantity <= 0) {
                location.reload();
              }
            }
          }
        })
      }
    })
  }












// var updateBtns = document.getElementsByClassName('update-cart')
// for (var i = 0; i<updateBtns.length;i++){
//     updateBtns[i].addEventListener('click',function(){
        
//         var productId = this.dataset.product
//         var action = this.dataset.action
//         console.log('productId:',productId,'action:',action)
//         console.log('USER:',user)
//         if (user==="AnonymousUser"){
//             console.log('Not logged in')
//         }else{
//             updateUserOrder(productId,action)
//         }
//     })
// }
// function updateUserOrder(productId,action){
//     console.log('Logged in, sending data....')
//     var url = '/update_item/'
//     fetch(url,{
//         method:'POST',
//         headers:{'Content-Type':'application/json',
//                 'X-CSRFToken':csrftoken},
//         body:JSON.stringify({'productId':productId,'action':action})
//     })
//     .then((response) =>{
//         return response.json()
//     })
//     .then((data) =>{
//          console.log('data',data)
//          location.reload()
//     })
    
// }
