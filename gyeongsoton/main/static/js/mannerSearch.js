function filter() {
  var i, detail, searchBox, mannerBox;
  searchBox = document.querySelector(".search__box");
  mannerBox = document.querySelector(".manner__box");
  console.log(mannerBox.length);
  for(i = 0; i < mannerBox.length; i++) {
    detail = mannerBox[i].querySelector(".manner__hashtag--detail");
    if(detail[0].innerHTML.indexOf(searchBox) > -1) {
      mannerBox[i].style.display = "flex";
    }
    else {
      mannerBox[i].style.display = "none";
    }
  }
}




// function filter(){

//   var value, name, item, i;

//   value = document.getElementById("value").value.toUpperCase();
//   item = document.getElementsByClassName("item");

//   for(i=0;i<item.length;i++){
//     name = item[i].getElementsByClassName("name");
//     if(name[0].innerHTML.toUpperCase().indexOf(value) > -1){
//       item[i].style.display = "flex";
//     }else{
//       item[i].style.display = "none";
//     }
//   }
// }