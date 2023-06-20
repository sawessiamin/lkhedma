const express = require('express'); 
const app = express(); 
const port = 4000

app.listen(port, () => console.log(`Listening on port ${port}`)); //Line 6
const cors = require('cors');
app.use(cors({
    origin: '*'
}));
app.get('/wifi_connect', (req, res) => { 
    var thessid = 'TOPNET_2090'
    var thepass = 'sfqof9f8b9'
  
    const wifi = require('node-wifi');
  
    wifi.init({iface: null});
    
    wifi.connect({ ssid  : thessid, password  : thepass });
    
    
  res.send({ status: true }); //Line 10
});