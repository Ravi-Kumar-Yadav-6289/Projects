var rect =  document.querySelector("#center");


//the eventlistners give us some details which can be captures in the variables and passed to the fuctions 
rect.addEventListener('mousemove',function(details){
    var box_loc = rect.getBoundingClientRect();
    console.log(box_loc);
})


