// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');
//setup public folder
app.use(express.static('./public'));
// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: false }));
// parse application/json
app.use(bodyParser.json());
app.use(sessions({'secret': 'this is not a secret'}))


app.get('/',function (req, res) {
    let session = req.session;
    if(session.logged) {
        res.redirect('/trip')
    }    
    else {
        res.render('pages/login');
    }
});

app.post('/', (req, res) => {
    console.log(req.body.userid, req.body.password)
    if(req.body.userid == "Hello"  && req.body.password == "World") {
        let session = req.session;
        session.logged = true;
        res.redirect('/trip')
    }
    else {
        res.render('pages/login', {errors : 'invalid username or password'})
    }
})


app.get('/trip', function(req, res) {
    axios.get(`http://127.0.0.1:5000/api/trip`, )
    .then((response) => {
        var trip= response.data;
            res.render('pages/trip', {
            trip: trip

    });      
});
});

app.get('/destination', function(req, res) {
    /*let session = req.session;
    if(!session.logged) {
        res.redirect('/destination')
    }
    else {*/
        axios.get(`http://127.0.0.1:5000/api/destination`, )
        .then((response) => {
                var destination= response.data;
                console.log(destination);


                res.render('pages/destination', {
                    destination: destination

            });      
        });
/*}*/
});



// Create new trip
app.get('/createtrip', function(req, res) {
    axios.get(`http://127.0.0.1:5000/api/destination`, )
    .then((response) => {
            var destination= response.data;
            res.render('pages/createtrip', {
                destination: destination
        });      
    });
  
});


app.post('/createtrip', function(req, res) {
    var postTrip = req.body;
    console.log(postTrip)
    axios.post('http://127.0.0.1:5000/api/trip', postTrip).then(function(response){
        res.redirect("/");
    })     
});

app.get('/createtrip', function(req, res) {
    axios.get(`http://127.0.0.1:5000/api/destination`, )
    .then((response) => {
            var destination= response.data;
            res.render('pages/createtrip', {
                destination: destination
        });      
    });
  
});

// Create destination
app.post('/createdestination', function(req, res) {
    var postDestination = req.body;
    console.log(postDestination)
    axios.post('http://127.0.0.1:5000/api/destination', postDestination).then(function(response){
        res.redirect("/destination");
    })     
});

app.get('/createdestination', function(req, res) {
    axios.get(`http://127.0.0.1:5000/api/destination`, )
    .then((response) => {
            var destination= response.data;
            res.render('pages/createdestination', {
                destination: destination
        });      
    });
  
});

//Edit Trip
app.get('/edittrip/:id', function(req, res) {
    console.log(req.params)
    
    axios.get(`http://127.0.0.1:5000/api/trip/${req.params.id}`, )
    .then((response) => {
        var trip = response.data;
        console.log("TRIP " , trip)
        axios.get(`http://127.0.0.1:5000/api/destination`, )
        .then((response) => {
                var destination= response.data;
                res.render('pages/edittrip', {
                    destination: destination, trip: trip
            });      
        });
    });
});


app.post('/edittrip/:id', function(req, res) {
    var postTrip = req.body;
    console.log("POST ", postTrip)
    axios.put('http://127.0.0.1:5000/api/trip', postTrip).then(function(response){
        res.redirect("/trip");
    })   
});

// Edit Destination
app.get('/editdestination/:id', function(req, res) {
    console.log(req.params)
    
    axios.get(`http://127.0.0.1:5000/api/destination/${req.params.id}`, )
    .then((response) => {
        var destination = response.data;
        console.log("DESTINATION " , destination)
                var destination= response.data;
                res.render('pages/editdestination', {
                    destination: destination
            });      
        });
    });



app.post('/editdestination/:id', function(req, res) {
    var postDestination = req.body;
    console.log("POST ", postDestination)
    axios.put('http://127.0.0.1:5000/api/destination', postDestination).then(function(response){
        res.redirect("/destination");
    })   
});


app.delete('/deletetrip/:id', function(req, res) {
    axios.delete(`http://127.0.0.1:5000/api/trip/${req.params.id}`, function(resp){
        res.json({status: 'ok'});
    })
});

app.delete('/deletedestination/:id', function(req, res) {
    axios.delete(`http://127.0.0.1:5000/api/destination/${req.params.id}`, function(resp){
        res.json({status: 'ok'});
    })
});






app.listen(8080);
console.log('8080 is the port that leads to the Vacation Planner Website');
