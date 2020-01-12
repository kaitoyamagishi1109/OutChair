console.log("Test Change!\n");

function renderButton() {
    gapi.signin2.render('GoogleButton',
    {
       'onsuccess': () => {},
       'onfailure': () => {}
   });
}

function init() {
    gapi.load('auth2', function() {
        gapi.auth2.init({client_id : config.OAUTH_CLIENT_ID});
        renderButton();
    });
}