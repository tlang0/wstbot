function ready() {
  var dropper = document.getElementById('dropper');
  var fileInput = document.getElementById('fileInput');
  
  dropper.addEventListener('dragover', function (e) {              
    e.preventDefault();
  });
  dropper.addEventListener('drop', function (e) {   
    e.preventDefault();
    while (e.dataTransfer == null && e.originalEvent != null) {
      e = e.originalEvent;
    }
    var files = e.dataTransfer.files;
    if (files) {           
      send(files);
    }
    return false;
  });
  var token;
  dropper.addEventListener('click', function (e) {
    fileInput.click();
  });
  fileInput.onchange = function (e) {
    var files = fileInput.files;
    if (files) {           
      send(files);
    }
  }
      
  registerOnPaste(dropper, function (data){
    send([dataURItoBlob('data:text/plain,' + data)])
  },  function (data){
    send([dataURItoBlob(data)]);
  })
  .focus();
}

var dataURItoBlob = function (dataURI) {
console.log(dataURI);
  var data = dataURI.slice(dataURI.indexOf(',') + 1);
  var desc = dataURI.split(',')[0].split(':')[1].split(';');
  var mime = desc[0];  
  var encoding = desc.length > 1 ? desc[desc.length - 1] : null;
  if (encoding == 'base64') {
    data = atob(data);
  }
  var array = [];
  for(var i = 0; i < data.length; i++) {
      array.push(data.charCodeAt(i));
  }
  return new Blob([new Uint8Array(array)], {type: mime});
};

var mime2ext = function(mime) {
  switch(mime) {
  case 'image/png':
    return '.png';
  case 'image/jpeg':
    return '.jpg';
  case 'image/gif':
    return '.gif';
  case 'text/plain':
    return '.txt';
  }
  return '';
}

var send = function(files) {
  var counter = 0;
  for (var i=0; i < files.length; i++) {   
    var xhr = new XMLHttpRequest();
    xhr.file = files[i];
    xhr.onreadystatechange = function(e) {
      if ( 4 == this.readyState ) {
        var el = document.getElementById('results');
        el.innerHTML = this.responseText + el.innerHTML;
        counter--;
        if (counter == 0)
          document.getElementById('counter').innerHTML = "";
        else
          document.getElementById('counter').innerHTML = "Uploading " + counter + " file" + (counter == 1 ? "" : "s") + ".";
      }
    };                        
    xhr.open('post', url, true);
   
    var data = new FormData;
    data.append('file', files[i], files[i].name || ('unknown' + mime2ext(files[i].type)));
    counter++;
    document.getElementById('counter').innerHTML = "Uploading " + counter + " file" + (counter == 1 ? "" : "s") + ".";
    xhr.send(data);
  }
};

// adapted from https://github.com/Puffant/paste.js
var registerOnPaste = function(div, ontext, onimage) {
  div.contentEditable = true;
  var content = div.innerHTML;
  var retrieving = false;
  setInterval(function() {
    if (!retrieving) {
      div.innerHTML = content;
    }
  }, 1);
  div.addEventListener('paste', function(ev) {
    var clipboardData, item, text;
    if (clipboardData = ev.clipboardData) {
      // chrome
      if (clipboardData.items) {
        if (item = clipboardData.items[0]) {
          if (item.type.match(/^image\//)) {
            reader = new FileReader();
            reader.onload = function(event) {
              onimage(event.target.result);
            };
            reader.readAsDataURL(item.getAsFile());
          }
          item.getAsString(function(string) {
              console.log(string);
            });
          if (item.type === 'text/plain') {
            item.getAsString(function(string) {
              ontext(string);
            });
          }
        }
      } 
      // FF
      else {
        if (clipboardData.types.length) {
          clipboardData.getData(function() {console.log(arguments)});
          
          if (text = clipboardData.getData('Text')) {
            ontext(text);
          }
        } else {
          retrieving = true;
          setTimeout(function() {
            var imgs = div.getElementsByTagName('img');
            if (imgs.length > 0) {
              onimage(imgs[0].src);
              retrieving = false;
            }
          }, 1);
        }
      }
    }
    // IE
    if (clipboardData = window.clipboardData) {
      if (text = clipboardData.getData('Text')) {
        ontext(text);
      } else {        
        retrieving = true;
          setTimeout(function() {
            var imgs = div.getElementsByTagName('img');
            if (imgs.length > 0) {
              onimage(imgs[0].src);
              retrieving = false;
            }
          }, 1);
      }
    }
  });
  return div;
};
