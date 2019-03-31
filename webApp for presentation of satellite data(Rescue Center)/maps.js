// Initialize Firebase
var config = {
    apiKey: "AIzaSyAqdcKkj7n_HRkI513VPG0F6VxqykGDOS4",
    authDomain: "sih2019-f0d6c.firebaseapp.com",
    databaseURL: "https://sih2019-f0d6c.firebaseio.com",
    projectId: "sih2019-f0d6c",
    storageBucket: "sih2019-f0d6c.appspot.com",
    messagingSenderId: "209332515266"
};  firebase.initializeApp(config);

//pick latitudeand longitude from firebase

var ref= firebase.database().ref('latLong');

ref.on("value",getdata);

function getdata(data){
     
  var cordinates= data.val();
  

  var options={
    zoom:4.8,
    center:{lat:22.7196,lng:75.8577}
  }
  var map= new google.maps.Map(document.getElementById('map'),options);  
  if(Object!=null)
  {
    var keys= Object.keys(cordinates);
    for(var i=0;i<keys.length;i++)
    {
      var point=keys[i];
  
      var x=parseFloat(cordinates[point].latitude);
      var y=parseFloat(cordinates[point].longitude);
      addMarker({lat:x,lng:y});
    }
    function addMarker(cords){
      var marker= new google.maps.Marker({
          position:cords,
          map:map
      });
    }  
  }
    
}