/*
                                      :%&*+*=.       .==*%@+.                                       
                                     =@+=%*%*#-.....=%=*++&%#-                                      
                                     #%▒@█▓*==#&&&&&= █+▒░██#%                                      
                                     -▒&++&&.  .. .. .▓░++*#▒:                                      
                                     *%+*+:.   :- =:  ::&▒▒▓█&                                      
                                     @=*+****%+*&&&%*%%%%**%▓█                                      
                                     :%%=::::..++.-*==%*::=%%:                                      
                                      *██▒%:  --%▒@+%&██#▒██&                                       
                             .===++: =█#&░:.:.:=====#@▓███░░█* :=*+++.                              
                             &:.*==█░@- @▓..         . =▒█: :░@█+:. :▒-                             
                             @ =░▓▓▓▒::@█░            ..+#▒-.:▒███░*=█=                             
                             +░:.&██* :&█▒-             -@█@- ░██* =░&.                             
                              -░#@▓█▒.  :█▒:           :░█+ .&███%▒▓+                               
                     :==%&&░▒▒▒@▒▓▒██@- .-▓█&-       :&█▓+.=*██████▓░░░#***::.                      
               =+##@░@@&%*--     .&████#: #███▒&&%%&▒██▓*.:#████▒+::::%&&%#@▒░▒@%%=:                
            #@█░#*-.         ==%%@#@▓████+.*▒█████████▒% .▒████░▓█▓▒▒░▓=     .-==+#@▒@*:            
             .+*%@#▓▓░@@%%%%&░%░@#▒█&▒██@*%=#+▓%░█▓%░&=@:&%▓█▓@█&&%░@*▒@:           :+@█#:          
                   --*&#▒█░░░▒░%███%*█▓-*██-▒█#+▒██░+@█#*█▓-#▓@██▓▓░%▓&:         .     :░█=         
         :-+*%%%&%%%+=::.      . .:=++@&##&&@@+%*-+%&&&@##░#@+-=-. .:.                  :█&         
       *░█░%:                                                                         .+▒█+         
        .-*░▓▓@%+--                .                                              :-%@▓█#-          
            :-=%@▒▓▓##&%+--:                                            :---*%##░▓▓░#%=             
                  .-:%%%░▒▒▓█▓░@@@@#&&%&*%%%%%%%%%%*%**%%%%%%%%&#@@░░▒███▒▒▒&%&--.                  
                           ....++++&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&++++::::                          
            

                                 ▜                 ▜ ▘▜        ▌
                                 ▐ ▀▌▛▌▛▌▌▌▀▌▛▌█▌  ▐ ▌▐ ▌▌▛▌▀▌▛▌
                                 ▐▖█▌▌▌▙▌▙▌█▌▙▌▙▖  ▐▖▌▐▖▙▌▙▌█▌▙▌
                                       ▄▌    ▄▌         ▄▌▌     
*/

// server.js
const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const definirRoutes = require("./src/routes/definir"); // Import the definir route

const app = express();

app.use(bodyParser.json());

const corsOptions = {
  origin: "http://localhost:3333", // replace with your client-side app's URL
  methods: "GET,HEAD,PUT,PATCH,POST,DELETE",
  credentials: true, // enable passing cookies, authorization headers, etc.
  optionsSuccessStatus: 204, // some legacy browsers (IE11, various SmartTVs) choke on 204
};

app.use(cors(corsOptions));
// app.use(cors()) // Use this after the variable declaration

// Use the definir route
app.use("/definir", definirRoutes);

// Define a route for GET requests to /api/boo
app.post("/api/ghoul", (req, res) => {
  console.log(req.body);
  console.log("@@@ GHOUL @@@");
  res.json({
    message: "Ghoul! This is the response from the /api/ghoul endpoint.",
  });
});

// Define a route for GET requests to /api/boo
app.get("/api/boo", (req, res) => {
  res.json({
    message: "Booz! This is the response from the /api/boo endpoint.",
  });
});

// // Custom error handling middleware
// app.use((err, req, res, next) => {
//   // Check if the error is CORS-related
//   if (err.name === 'CorsError') {
//     // Log the CORS error
//     console.error('CORS Error:', err.message);

//     // Optionally, you can send a custom response to the client
//     res.status(400).send('Bad Request - CORS Issue');
//   } else {
//     // For other errors, let the default error handler handle it
//     next(err);
//   }
// });

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

// SLOW AND STEADY

//curl -X GET -H "Content-Type: application/json" -d '{"palabra": "example"}' http://localhost:3001/definir
