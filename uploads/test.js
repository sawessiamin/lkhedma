function connectWifi  () {

    var thessid = 'TOPNET_2090'
    var thepass = 'sfqof9f8b9'
  
    const wifi = require('node-wifi');
  
    wifi.init({iface: null});
    
    wifi.connect({ ssid  : thessid, password  : thepass });
    
    
  
  }

  connectWifi() ;
  