const sendHttpRequest = (method, url, data) => {
    const promise = new Promise((resolve, reject) =>{
      const xhr = new XMLHttpRequest();
      xhr.open(method, url);
  
      xhr.responseType = 'string';
      if(data){
        xhr.setRequestHeader('Content-Type', 'text/json');
      }
      xhr.onload = () => {
        resolve(xhr.response);
      };
      xhr.send(JSON.stringify(data));
    });
    return promise;
  }

const sendData = () => {
    const data = Array.from(document.querySelectorAll('#registrationForm input')).reduce((acc, input) => ({...acc, [input.id]: input.value}), {});
    sendHttpRequest('POST', 'http://localhost:8080/create', data).then(responseData => {
        if(responseData != "GOOD")
          alert(responseData);
        else{
          alert("Student added");
          location.replace("allStudents.html");
        }
      })
      .catch(err => {
        console.log(err);
      });
}