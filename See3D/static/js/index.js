function onSignIn(googleUser) {
  // Get ID token from successfully logged in user.
  var id_token = googleUser.getAuthResponse().id_token;

  // Send the ID token to backend with an HTTPS POST request.
  var xhr = new XMLHttpRequest();
  xhr.open('POST', 'https://127.0.0.1:5000/index');
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = function() {
    console.log('Signed in as: ' + xhr.responseText);
  }
  xhr.send('idtoken=' + id_token);
}

function signOut() {
  var auth2 = gapi.auth2.getAuthInstance();
  auth2.signOut().then(function () {
    console.log('User signed out.');
  });
}
