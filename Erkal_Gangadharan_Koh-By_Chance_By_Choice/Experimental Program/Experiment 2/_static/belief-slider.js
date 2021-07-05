//$(document).ready(function () {
//    $('input[type=range]').on('input change', function () {
//        $('input[type=range]').addClass('slider');
//    });
//
//});

var slider1 = document.getElementById("myRange1");
var output1 = document.getElementById("demo1");
output1.innerHTML = slider1.value;

var slider2 = document.getElementById("myRange2");
var output2 = document.getElementById("demo2");
output2.innerHTML = slider2.value;

var slider3 = document.getElementById("myRange3");
var output3 = document.getElementById("demo3");
output3.innerHTML = slider3.value;

var slider4 = document.getElementById("myRange4");
var output4 = document.getElementById("demo4");
output4.innerHTML = slider4.value;

slider1.oninput = function() {
  output1.innerHTML = this.value;
}

slider2.oninput = function() {
  output2.innerHTML = this.value;
}

slider3.oninput = function() {
  output3.innerHTML = this.value;
}

slider4.oninput = function() {
  output4.innerHTML = this.value;
}

$(function() {
  $('input[type=range]').change(getTotal);
  getTotal();
});

function getTotal() {
  var answer1 = parseInt(slider1.value) || 0;
  var answer2 = parseInt(slider2.value) || 0;
  var answer3 = parseInt(slider3.value) || 0;
  var answer4 = parseInt(slider4.value) || 0;
  document.getElementById("total").innerHTML = answer1 + answer2  + answer3 + answer4;
}

$(function() {
  $('input[type=range]').change(checkTotal);
  checkTotal();
});

function checkTotal() {
  var answer1 = parseInt(slider1.value) || 0;
  var answer2 = parseInt(slider2.value) || 0;
  var answer3 = parseInt(slider3.value) || 0;
  var answer4 = parseInt(slider4.value) || 0;
  if (answer1 + answer2  + answer3 + answer4 === 10) {
    document.getElementById("submit").style.display = "block";
  } else {
    document.getElementById("submit").style.display = "none";
  }
  }